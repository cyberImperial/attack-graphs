from __future__ import absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from topology.graph.graph import Graph
from topology.graph.graph import Node

import json
import ast

from random import randrange

class Simulation():
    def __init__(self, conf_file):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.join(dir_path, "confs")
        with open(os.path.join(dir_path, conf_file), 'r') as f:
            data = json.dumps(ast.literal_eval(f.read()))
            self.conf = json.loads(data)
            print("Configuration successfully parsed...")
        self.graph = Graph.from_json(self.conf)
        print("Graph successfully loaded...")

    def connection(self):
        def build_packet(src, dest):
            return {
                "src" : str(src),
                "dest" : str(dest)
            }

        class Connection():
            def __init__(self, graph):
                self.graph = graph

            def next(self):
                # return a new random packet sent between 2 nodes of the graph
                link_idx = randrange(len(self.graph.edges))
                for (n1, n2) in self.graph.edges:
                    if link_idx == 0:
                        return build_packet(n1.ip, n2.ip)
                    link_idx -= 1

                raise Exception("Malformed simulation graph!")

        return Connection(self.graph)

    def discovery_ip(self, ip):
        for node in self.graph.nodes:
            if Node(ip) == node:
                return node.running
        return {}

simulation = Simulation("simple.json")
print(simulation.discovery_ip("10.1.3.1"))
connection = simulation.connection()
packets = 10
while packets > 0:
    print(connection.next())
    packets -= 1
