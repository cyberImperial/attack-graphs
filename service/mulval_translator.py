import json
from client import LocalClient
from server import Server, config

class MulvalTranslator():

    def __init__(self):
        #self.data = LocalClient(config["graph"]).get("/graph")
        self.data = json.loads("{ \
           \"links\":[ \
                  { \
                     \"source\":\"127.0.0.1\",\
                     \"target\":\"127.0.0.2\",\
                     \"value\":1\
                  },\
                  {\
                     \"source\":\"127.0.0.1\",\
                     \"target\":\"127.0.0.3\",\
                     \"value\":1\
                  },\
                  {\
                     \"source\":\"127.0.0.2\",\
                     \"target\":\"127.0.0.4\",\
                     \"value\":1\
                  }],\
           \"hosts\":[\
                  {\"ip\": \"127.0.0.1\", \"running\": {\
                  \"RunningServices\":[\
                     {\
                        \"Service\":{\
                           \"state_open\":\"open\",\
                           \"version\":\"3.1\",\
                           \"product\":\"GitHub.com\",\
                           \"name\":\"Demo\",\
                           \"reason\":\"syn-ack\"\
                        },\
                        \"Vulnerability\":{\
                           \"vul\":\"vul\"\
                        },\
                        \"Port\":{\
                           \"portid\":\"443\",\
                           \"protocol\":\"tcp\"\
                        },\
                        \"Privileges\":{\
                           \"pri\":\"pri\"\
                        }\
                     }\
                     ]\
                  }},\
                  {\"ip\": \"127.0.0.2\", \"running\": {}},\
                  {\"ip\": \"127.0.0.3\", \"running\": {}},\
                  {\"ip\": \"127.0.0.4\", \"running\": {}}\
           ]\
      }")
        self.f = open('mulval_input.P', 'w')
        self.s = set()
        self.makeTopology()
        self.addVulnerabilities()

    def makeTopology(self):
        self.f.write("attackerLocated(internet).\n")
        self.f.write("attackGoal(execCode(_, _)).\n")
        self.f.write("hacl(X, Y, _, _) :-\n "
                     + " inSubnet(X,S),\n"
                     + "  inSubnet(Y,S).\n\n" )

        self.f.write("hacl(internet, '" + self.data["links"][0]["source"] +
                     "', httpProtocol, httpPort).\n")
        for link in self.data["links"]:
            if not link["source"] in self.s:
                self.f.write(" inSubnet('" + link["source"] + "', subnet).\n")
                self.s.add(link["source"])
            if not link["target"] in self.s:
                self.f.write(" inSubnet('" + link["target"] + "', subnet).\n")
                self.s.add(link["target"])

    def addVulnerabilities(self):
        pass





mulval = MulvalTranslator();
