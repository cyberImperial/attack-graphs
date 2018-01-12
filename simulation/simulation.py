from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from topology.graph.graph import Graph
from topology.graph.graph import Node

import json
import ast
import time

from random import randrange

class Simulation():
    def __init__(self, conf_file, connection_timeout = 0.5, scan_timeout = 10):
        self.connection_timeout = connection_timeout
        self.scan_timeout = scan_timeout

        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.join(dir_path, "confs")

        with open(os.path.join(dir_path, conf_file), 'r') as f:
            data = json.dumps(ast.literal_eval(f.read()))
            self.conf = json.loads(data)
            logger.info("Configuration successfully parsed...")

        self.graph = Graph.from_json(self.conf)
        logger.info("Graph successfully loaded...")

    def connection(self):
        def build_packet(src, dest):
            time.sleep(self.connection_timeout)
            return "header", {
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

                logger.error("Simulated connection crashed.")
                raise Exception("Malformed simulation graph!")

        return Connection(self.graph)

    def discovery_ip(self, ip):
        # simulate scan timeout
        logger.info("Started scan.")
        time.sleep(self.scan_timeout)

        for node in self.graph.nodes:
            if Node(ip) == node:
                logger.info("Succesful scan.")
                return node.running

        logger.info("Failed scan.")
        return {}

if __name__ == "__main__":
    simulation = Simulation("simple.json")
    logger.debug(simulation.discovery_ip("10.1.3.1"))
    connection = simulation.connection()
    packets = 10
    while packets > 0:
        logger.debug(connection.next())
        packets -= 1
