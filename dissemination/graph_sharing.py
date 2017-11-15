from __future__ import absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.client import LocalClient
from service.server import Server
from service.components import Component

from service.server import config

class GraphSharing():
    def __init__(self, graph_client=LocalClient(config["graph"])):
        self.graph_client = graph_client

    def snapshoot(self):
        """
        Takes a snapshoot of the graph to multicast.
        """
        graph = self.graph_client.get("/graph")
        return graph

    def update(self, graph):
        """
        Relays the graph merge to the graph_service.
        """
        self.graph_client.post("/merge", graph)
