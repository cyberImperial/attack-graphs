import json
from client import LocalClient
from server import Server, config

from mock_data import mock_data

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
    mulval = mock_data(MulvalTranslator())

    mulval.makeTopology()
    mulval.addVulnerabilities()
