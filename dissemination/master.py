from __future__ import absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
        self.server.add_component_get("/register", MasterReceive(self))

    def receive(self, registration):
        pass

    def broadcast(self):
        pass

if __name__ == "__main__":
    master = Master()
    master.server.run()
