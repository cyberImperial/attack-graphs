from __future__ import absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.components import Component
from service.server import Server, config
from service.client import LocalClient

from inference.mulval_translator import generate_attack_graph

class AttackGraphExporter(Component):
    def __init__(self, client):
        self.client = client

    def process(self, _):
        attack_graph = generate_attack_graph(self.client)
        return {
            "mulval_output" : attack_graph
        }

class InferenceClient(LocalClient):
    def get_attack_graph(self):
        return self.get("/attack_graph")

def inference_service():
    """
    The inference service provides an overlay over the Mulval service.
    """

    client = LocalClient(config["graph"])
    server = Server("inference", config["inference"])
    server.add_component_get("/attack_graph", AttackGraphExporter(client))
    server.run()

if __name__ == "__main__":
    inference_service()
