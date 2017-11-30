from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json, subprocess
from service.client import LocalClient
from service.server import Server, config

from inference.mock_data import mock_data

class MulvalTranslator():
    def __init__(self):
        self.f = open('mulval_input.P', 'w')
        self.s = set()

    def makeTopology(self):
        self.f.write("attackerLocated(internet).\n")
        self.f.write("attackGoal(execCode(_, _)).\n")
        self.f.write("hacl(X, Y, _, _) :-\n "
                     + " inSubnet(X,S),\n"
                     + "  inSubnet(Y,S).\n\n" )

        self.f.write("hacl(internet, '" + self.data["links"][0]["source"] +
                     "', _, _).\n")
        for link in self.data["links"]:
            if not link["source"] in self.s:
                self.f.write(" inSubnet('" + link["source"] + "', subnet).\n")
                self.s.add(link["source"])
            if not link["target"] in self.s:
                self.f.write(" inSubnet('" + link["target"] + "', subnet).\n")
                self.s.add(link["target"])

    def addVulnerabilities(self):
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

                    self.f.write("networkServiceInfo('%s', '%s', '%s', '%s', '%s').\n" % (ip, application, protocol, port, privileges))
                    self.f.write("vulExists('%s', '%s', '%s').\n" % (ip, vulnerability, application))
                    self.f.write("vulProperty('%s', %s, %s).\n" % (vulnerability, access, 'privEscalation'))

if __name__ == "__main__":
    mulval = None
    try:
        mulval = MulvalTranslator()
        mulval.data = LocalClient(config["graph"]).get("/graph")
    except Exception as e:
        mulval = mock_data(MulvalTranslator())
    if mulval.data is None:
        mulval = mock_data(MulvalTranslator())

    mulval.makeTopology()
    mulval.addVulnerabilities()
    mulval.f.close()

    os.system("export MULVALROOT=/home/ad5915/mulval")
    os.system("PATH=$PATH:$MULVALROOT/bin")
    os.system("PATH=$PATH:$MULVALROOT/utils")
    os.system("export XSB_DIR=/home/ad5915/mulval/XSB")
    os.system("PATH=$PATH:$XSB_DIR/bin")
    subprocess.Popen(['graph_gen.sh mulval_input.P -v -p'],  shell=True).wait()
    os.system("evince AttackGraph.pdf")
