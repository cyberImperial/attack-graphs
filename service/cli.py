from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from networks.network import Network
from networks.network import default_network
from service.server import config

import json, requests

class CLI():
    def __init__(self):
        def init_network():
            self.network = default_network()

        def add_node():
            self.network.add_node(Network.metasploitable, "")
            self.network.connect_to_subnet(network.nodes[-1], network.subnets[0])

        def request(line, component, url):
            line = line.split("\n")[0]
            args = len(line.split(" "))
            if args != 3:
                return
            product, version = tuple(line.split(" ")[1:])
            # e.g. qemu 0.13.0
            request = json.loads("[{ \
                \"product\" : \"" + product + "\",\
                \"version\" : \"" + version + "\"\
            }]")

            try:
                r = requests.post(
                    url = "http://127.0.0.1:" + str(config[component]) + url,
                    json = request)
                print(r.text)
            except Exception as e:
                pass

        self.functions = {
            "echo" : lambda x: print(x[4:]),
            "start" : lambda x: init_network(),
            "delete" : lambda x: self.network.stop_network(),
            "add node" : lambda x: add_node(),
            "query" : lambda x: request(x, "database", "vulnerability"),
            "privileges" : lambda x: request(x, "database", "privileges")
        }

    def dispatch(self, line):
        for function in self.functions:
            if function in line:
                self.functions[function](line)

    def start(self):
        while True:
            sys.stdout.write('>')
            sys.stdout.write(' ')
            sys.stdout.flush()

            line = sys.stdin.readline()
            self.dispatch(line)

if __name__ == "__main__":
    CLI().start()
