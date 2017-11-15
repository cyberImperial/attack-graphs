from __future__ import absolute_import

import sys
import os
import time
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.client import Client
from service.server import Server
from service.components import Component

class SlaveMembership(Component):
    def __init__(self, slave):
        self.slave = slave

    def process(self, membership_list):
        print("Received....")
        self.slave.update_membership(membership_list)

class HealthCheck(Component):
    def process(self, _):
        return {
            "healty" : "true"
        }

class Slave():
    def __init__(self, slave_port, master_ip, master_port):
        self.master_client = Client("http://" + master_ip, master_port)
        self.membership_list = []

        self.server = Server("slave", slave_port)
        self.server.add_component_get("/healty", HealthCheck())
        self.server.add_component_post("/membership", SlaveMembership(self))

    def join(self):
        self.master_client.post("/register", {
            "ip" : "127.0.0.1",
            "port" : self.server.port
        })

    def update_membership(self, membership_list):
        print("Updating membership....")
        if "members" not in membership_list:
            return
        membership_list = membership_list["members"]

        self.membership_list = []
        for member in membership_list:
            client = Client("http://" + member["ip"], member["port"])
            self.membership_list.append(client)

    def dissemination(self):
        self.join()

if __name__ == "__main__":
    master_ip = "127.0.0.1"
    master_port = 5000

    # Need to give port as an argument
    slave_port = sys.argv[1]

    slave = Slave(slave_port, master_ip, master_port)

    threading.Thread(target=slave.server.run).start()
    threading.Thread(target=slave.dissemination).start()
