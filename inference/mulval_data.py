from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.client import LocalClient
from service.server import Server, config

def from_client_data_mock_default(mulval_translator):
    try:
        mulval_translator.data = LocalClient(config["graph"]).get("/graph")
    except Exception as e:
        mulval_translator = mock_data(mulval_translator)
        return mulval_translator
    if mulval_translator.data is None:
        mulval_translator = from_mock_data(mulval_translator)
    return mulval_translator

def from_client_data(mulval_translator):
    mulval_translator.data = LocalClient(config["graph"]).get("/graph")
    return mulval_translator

def from_mock_data(mulval_translator):
    mulval_translator.vulnerability = {
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
    mulval_translator.privileges = {
        "root" : True,
        "user" : False,
        "other" : False
    }


    mulval_translator.data = {
      "links" : [
              {
                "source":"127.0.0.1",
                "target":"127.0.0.2",
                "value":1
              },
              {
                "source":"127.0.0.1",
                "target":"127.0.0.3",
                "value":1
              },
              {
                "source":"127.0.0.2",
                "target":"127.0.0.4",
                "value":1
              }],
      "hosts":[
              {"ip":"127.0.0.1","running": {
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
                   "Vulnerability": mulval_translator.vulnerability,
                   "Port":{
                      "portid":"443",
                      "protocol":"tcp"
                    },
                   "Privileges": mulval_translator.privileges
                 }
                 ]
              }},
              {"ip":"127.0.0.2","running": {
                "scanned" : "true"
              }},
              {"ip":"127.0.0.3","running": {
                "scanned" : "true"
              }},
              {"ip":"127.0.0.4","running": {
                "scanned" : "true"
              }}
       ]
    }
    return mulval_translator
