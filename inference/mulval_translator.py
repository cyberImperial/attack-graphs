from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json, subprocess
from service.client import LocalClient
from service.server import Server, config

from inference.mulval_data import TranslatorBuilder

class MulvalTranslator():
    def __init__(self):
        self.mulval_file = open('mulval_input.P', 'w')
        self.active_set = set()

    def _make_topology(self):
        self.mulval_file.write("attackerLocated(internet).\n")
        self.mulval_file.write("attackGoal(execCode(_, _)).\n")

        # Hardcoded...
        self.mulval_file.write("hacl(internet, '{}', _, _).\n".format(self.data["links"][0]["source"]))

        def add_edge(edge_from, edge_to):
            if not (edge_from, edge_to) in self.active_set:
                self.mulval_file.write("hacl('{}', '{}', _, _).\n".format(edge_from, edge_to))
                self.active_set.add((edge_from, edge_to))

        for link in self.data["links"]:
            add_edge(link["source"], link["target"])

    def _add_vulnerabilities(self):
        for host in self.data["hosts"]:
            if host["running"]["scanned"] == "false":
                continue
            running = host["running"]
            if running != {"scanned" : "true"}:
                for service in running["RunningServices"]:
                    ip = host["ip"]
                    application = service["Service"]["product"]
                    port = service["Port"]["portid"]
                    protocol = service["Port"]["protocol"]

                    if service["Privileges"]["user"]:
                        privileges = "user"
                    if service["Privileges"]["root"]:
                        privileges = "root"
                    vulnerability = service["Vulnerability"]["id"]
                    access = service["Vulnerability"]["impact"]["baseMetricV2"]["cvssV2"]["accessVector"]

                    if access == "LOCAL": access = "localExploit"
                    if access == "NETWORK": access = "remoteExploit"

                    self.mulval_file.write("networkServiceInfo('%s', '%s', '%s', '%s', '%s').\n" % (ip, application, protocol, port, privileges))
                    self.mulval_file.write("vulExists('%s', '%s', '%s').\n" % (ip, vulnerability, application))
                    self.mulval_file.write("vulProperty('%s', %s, %s).\n" % (vulnerability, access, 'privEscalation'))

    def _cleanup(self, files_before):
        # clean all the files produced by mulval
        to_clean = list(set(os.listdir()) - set(files_before))
        logger.info("Files cleaned: {}".format(to_clean))
        for f in to_clean:
            os.system("rm {}".format(f))

    def _save_output(self):
        with open('AttackGraph.txt', 'r') as output:
            return output.read()

    def generate_attack_graph(self):
        logger.info("Generating attack graph.")
        files_before = os.listdir()

        self._make_topology()
        self._add_vulnerabilities()
        self.mulval_file.close()

        env = os.environ.copy()

        if "MULVALROOT" not in env:
            env["MULVALROOT"] = os.path.join(env["HOME"], "mulval")
        if "XSB_DIR" not in env:
            env["XSB_DIR"] = os.path.join(env["HOME"], "mulval", "XSB")

        env["PATH"] = "{}:{}".format(env["PATH"], os.path.join(env["MULVALROOT"], "bin"))
        env["PATH"] = "{}:{}".format(env["PATH"], os.path.join(env["MULVALROOT"], "utils"))
        env["PATH"] = "{}:{}".format(env["PATH"], os.path.join(env["XSB_DIR"], "bin"))

        subprocess.Popen(['graph_gen.sh mulval_input.P -v -p'], shell=True, env=env).wait()
        output = self._save_output()

        self._cleanup(files_before)

        return output

def generate_attack_graph(client):
    return TranslatorBuilder(client) \
        .from_client_data() \
        .from_mock_data_if_empty() \
        .build(MulvalTranslator()) \
        .generate_attack_graph()

if __name__ == "__main__":
    logger.info(generate_attack_graph(LocalClient(config["graph"])))
