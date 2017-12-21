from __future__ import absolute_import

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

    def make_topology(self):
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

    def add_vulnerabilities(self):
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

if __name__ == "__main__":
    mulval = TranslatorBuilder() \
        .from_client_data() \
        .from_mock_data_if_empty() \
        .build(MulvalTranslator())

    mulval.make_topology()
    mulval.add_vulnerabilities()
    mulval.mulval_file.close()

    os.system("export MULVALROOT=/home/ad5915/mulval")
    os.system("PATH=$PATH:$MULVALROOT/bin")
    os.system("PATH=$PATH:$MULVALROOT/utils")
    os.system("export XSB_DIR=/home/ad5915/mulval/XSB")
    os.system("PATH=$PATH:$XSB_DIR/bin")
    subprocess.Popen(['graph_gen.sh mulval_input.P -v -p'],  shell=True).wait()
    os.system("evince AttackGraph.pdf")
