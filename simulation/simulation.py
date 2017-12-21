from __future__ import absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from topology.graph.graph import Graph

import json
import ast

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

    def get_packet(self):
        pass

    def discovery_ip(self):
        pass

simulation = Simulation("simple.json")
