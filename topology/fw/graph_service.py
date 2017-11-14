from __future__ import absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from service.components import Component
from service.server import Server, config
from service.client import Client

from topology.fw.populator import Populator
from topology.fw.graph import Graph
from topology.fw.graph import Node

import ast
import time
import requests
import json
import threading

from threading import Lock

class GraphExporter(Component):
    def __init__(self, graph):
        self.graph = graph

    def process(self, unused):
        self.graph.lock.acquire()
        export = self.graph.to_json()
        self.graph.lock.release()

        return export

def start_graph_server(graph):
    server = Server("graph", config["graph"])
    server.add_component_get("/graph", GraphExporter(graph))
    threading.Thread(target=server.run).start()

def graph_loop():
    graph = Graph()
    populator = Populator(graph)

    start_graph_server(graph)
    threading.Thread(target=populator.populate_loop).start()
    while True:
        out = Client("http://127.0.0.1", 30001).get("/newpackets", default=[])

        graph.lock.acquire()
        for packet in out:
            src, dest = packet["src"], packet["dest"]

            if "255" in src or "255" in dest:
                continue

            graph.add_edge(Node(src), Node(dest))
        graph.lock.release()

        time.sleep(5)
        print(Client("http://127.0.0.1", 30002).get("/graph"))
