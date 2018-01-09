from __future__ import absolute_import

class TranslatorBuilder():
    def __init__(self, client):
        self.data = None
        self.client = client

    def from_client_data(self):
        try:
            self.data = client.get("/graph")
        except Exception as e:
            return self
        return self

    def from_mock_data_if_empty(self):
        if self.data is not None:
            return self

        self.vulnerability = {
           'impact':{
              'baseMetricV2':{
                 'impactScore':10.0,
                 'obtainUserPrivilege':False,
                 'severity':'HIGH',
                 'userInteractionRequired':False,
                 'obtainOtherPrivilege':False,
                 'exploitabilityScore':3.9,
                 'obtainAllPrivilege':False,
                 'cvssV2':{
                    'confidentialityImpact':'COMPLETE',
                    'accessVector':'NETWORK',
                    'integrityImpact':'COMPLETE',
                    'authentication':'NONE',
                    'availabilityImpact':'COMPLETE',
                    'accessComplexity':'LOW',
                    'vectorString':'(AV:L/AC:L/Au:N/C:C/I:C/A:C)',
                    'baseScore':7.2
                 }
              }
           },
           'id':'CVE-2015-2478',
           'description':'Microsoft Windows Vista SP2, Windows Server 2008 SP2 and R2 SP1, Windows 7 SP1, Windows 8, Windows 8.1, Windows Server 2012 Gold and R2, Windows RT Gold and 8.1, and Windows 10 Gold and 1511 allow local users to gain privileges via a crafted application that triggers a Winsock call referencing an invalid address, aka "Winsock Elevation of Privilege Vulnerability."'
        }
        self.privileges = {
            "root" : True,
            "user" : False,
            "other" : False
        }


        self.data = {
          "links" : [
                  {
                    "source":"10.1.3.1",
                    "target":"10.1.3.2",
                    "value":1
                  },
                  {
                    "source":"10.1.3.1",
                    "target":"10.1.3.3",
                    "value":1
                  },
                  {
                    "source":"10.1.3.2",
                    "target":"10.1.3.4",
                    "value":1
                  }],
          "hosts":[
                  {"ip":"10.1.3.1","running": {
                 "scanned" : "true",
                 "RunningServices":[
                     {
                       "Service":{
                          "state_open":"open",
                          "version":"3.1",
                          "product":"GitHub.com",
                          "name":"Demo",
                          "reason":"syn-ack"
                        },
                       "Vulnerability": self.vulnerability,
                       "Port":{
                          "portid":"443",
                          "protocol":"tcp"
                        },
                       "Privileges": self.privileges
                     }
                     ]
                  }},
                  {"ip":"10.1.3.2","running": {
                    "scanned" : "true"
                  }},
                  {"ip":"10.1.3.3","running": {
                    "scanned" : "true"
                  }},
                  {"ip":"10.1.3.4","running": {
                    "scanned" : "true"
                  }}
           ]
        }
        return self

    def build(self, mulval_translator):
        mulval_translator.data = self.data
        return mulval_translator
