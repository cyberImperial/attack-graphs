from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import os, sys, time
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(PROJECT_ROOT)

import subprocess
import json

def discovery_ip(ip):
    """
    A wrapper over Nmap that does OS discovery and port mapping. The wrapper is
    written in C++ and interfaced in Python, thus allowing parallel scanning.

    :param ip: given IP to scan as a string
    :return: JSON of the scan or {} when a scan fails
    """
    default = {}

    # Getting host information for ip
    try:
        logger.info("Running port scan...")
        subprocess.getoutput("nmap -oX host.xml -O -sV -p 1-1023 " + ip)
        logger.info("Examining port scan results...")

        # Need to do make before...
        binary_location = PROJECT_ROOT + "/build_topology"
        host_json = subprocess.getoutput(binary_location + " host.xml")
        if "Aborted" in host_json:
            return default
        else:
            return json.loads(host_json)
    except Exception as e:
        return default
