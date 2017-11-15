from __future__ import absolute_import

import os, sys, time
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

import subprocess
import json
from pprint import pprint

def discovery_ip(ip):
    # 172.18.0.1
    default = {}

    # Getting host information for ip
    try:
        print("Running port scan...")
        subprocess.getoutput("nmap -oX host.xml -O -sV -p 1-1023 " + ip)
        print("Examining port scan results...")

        # Need to do make before...
        binary_location = PROJECT_ROOT + "/build_topology"
        host_json = subprocess.getoutput(binary_location + " host.xml")
        if "Aborted" in host_json:
            return default
        else:
            return json.loads(host_json)
    except Exception as e:
        return default
