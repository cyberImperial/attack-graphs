from __future__ import absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.client import Client
from service.server import Server
from service.components import Component

class MasterReceive(Component):
    def __init__(self, master):
        self.master = master

    def process(self, message):
        self.master.register(message)
        self.master.broadcast()

class Master():
    def __init__(self):
        self.membership_list = []

        self.server = Server("master", 5000)
        self.server.add_component_post("/register", MasterReceive(self))

    def register(self, registration):
        print("Received register...")
        # For the moment the servers are single threaded, one-connection at a time
        # We need to make them concurrent
        client = Client("http://" + registration["ip"], registration["port"])
        self.membership_list.append(client)

    def broadcast(self):
        print("Broadcasting membership....")
        broadcast = {
            "members" : [{
                "ip" : client.url.split("/")[2],
                "port" : client.port,
            } for client in self.membership_list]
        }

        # Send the broadcast to each client
        for client in self.membership_list:
            client.get("/healty")
            client.post("/membership", broadcast)

if __name__ == "__main__":
    master = Master()
    master.server.run()
