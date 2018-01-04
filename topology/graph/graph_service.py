from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from service.components import Component
from service.server import Server, config
from service.client import LocalClient

from topology.graph.populator import Populator
from topology.graph.graph import Graph
from topology.graph.graph import Node

import ast
import time
import requests
import json
import threading

from threading import Lock

class GraphExporter(Component):
    """
    A component that allows exporting a graph.
    """
    def __init__(self, graph):
        self.graph = graph

    def process(self, unused):
        self.graph.lock.acquire()
        export = self.graph.to_json()
        self.graph.lock.release()

        return export

class GraphMerge(Component):
    """
    A component that allows exporting a graph.
    """
    def __init__(self, graph):
        self.graph = graph

    def process(self, graph):
        self.graph.lock.acquire()
        self.graph.merge(Graph.from_json(graph))
        self.graph.lock.release()
        return {
            "success" : "true"
        }

class GraphService():
    """
    The GraphService encapsulates all the dependecies of the
    graph service:
      * a local client to the sniffer
      * a server
      * a populator
    """
    def __init__(self, graph, sniffer_client=LocalClient(config["sniffer"])):
        self.graph = graph
        self.populator = Populator(self.graph)

        self.server = Server("graph", config["graph"])
        self.server.add_component_get("/graph", GraphExporter(graph))
        self.server.add_component_post("/merge", GraphMerge(graph))

        self.sniffer_client = sniffer_client

    def get_edge(self, packet):
        src, dest = packet["src"], packet["dest"]
        if "255" in src or "255" in dest:
            return None
        return Node(src), Node(dest)

    def update(self):
        new_packets = self.sniffer_client.get("/newpackets", default=[])

        self.graph.lock.acquire()
        for packet in new_packets:
            edge = self.get_edge(packet)
            if edge is not None:
                self.graph.add_edge(*edge)
        self.graph.lock.release()

def graph_service():
    """
    The graph_service method represents the runtime of the GraphService class.
    """
    graph = Graph()
    service = GraphService(graph)

    threading.Thread(target=service.server.run).start()
    threading.Thread(target=service.populator.populate_loop).start()
    while True:
        service.update()

        time.sleep(5)
        logger.debug(LocalClient(config["graph"]).get("/graph"))

if __name__ == "__main__":
    graph_service()
