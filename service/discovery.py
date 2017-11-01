from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import subprocess
import json
from pprint import pprint

def discovery(line):
    # TODO: refactor and get rid of bulaneli

    try:
        subnet_mask = line.split(" ")[1]
    except Exception as e:
        subnet_mask = "172.18.0.0/29"
    out = subprocess.getoutput("nmap -sP " + subnet_mask)

    ips = []
    hosts = []
    for word in out.split(" "):
        if len(word.split(".")) == 4:
            ips.append(word.split("\n")[0])
    print(ips)
    for ip in ips:
        default = {"Host" : ip }

        # Getting host information for ip
        try:
            subprocess.getoutput("nmap -oX host.xml -O -sV " + ip)
            subprocess.getoutput("nmap -oX trace.xml --traceroute " + ip)
            host_json = subprocess.getoutput("./build_topology host.xml trace.xml")
            if "Aborted" in host_json:
                hosts.append(default)
            else:
                hosts.append(json.loads(host_json))
        except Exception as e:
            hosts.append(default)
    with open("frontend_data.json", "w") as output:
         json.dump(hosts, output)
    pprint(hosts)
