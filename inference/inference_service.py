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

    def process(self):
        return {
            "mulval_output" : generate_attack_graph(client)
        }

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
