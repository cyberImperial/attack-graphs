from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from topology.graph.graph import Graph
from topology.graph.graph import Node
from clint.textui import colored

import json
import ast
import time

from random import randrange

class Simulation():
    """
    Class used to mock sniffer connections and ip discovery for running
    simulations.

    General description: The simulation module is lightweight and can easily
    handle overlay topologies of magnitude of thousands. The simulations are
    run on random overlay topologies with fixed number of nodes and edges.
    Random packets get generated whenever the simulation module connection gets
    a call within a fixed timeout of 0.5 seconds, whereas the scans are
    generated within a timeout of 3 seconds.
    """
    def __init__(self, conf_file, connection_timeout = 0.5, scan_timeout = 10):
        """
        Construct a new simulation object from a given configuartion file.

        :param conf_file: The configuration file must be a json that contains
            a graph. For an example see: `confs/simple.json`
        :param connection_timeout: packets get generated each
            connection_timeout seconds
        :param scan_timeout: the time to run a scan
        """
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
        """
        Return a Connection class. The internals of the topology module use
        only the next function from the `libpcap` Python wrapper.
        """
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
        """
        Function used as a seam instead of the original `discovery_ip` function.
        See sniffer module for more details.
        """
        logger.info(colored.cyan("Started scan."))
        time.sleep(self.scan_timeout)

        for node in self.graph.nodes:
            if Node(ip) == node:
                logger.info(colored.green("Successful scan."))
                return node.running

        logger.info("Failed scan.")
        return {}
