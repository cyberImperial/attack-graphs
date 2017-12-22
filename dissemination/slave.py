from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import sys
import os
import time
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.client import Client
from service.server import Server
from service.components import Component

from dissemination.graph_sharing import GraphSharing
from dissemination.util import get_host_ip

class SlaveMembership(Component):
    def __init__(self, slave):
        self.slave = slave

    def process(self, membership_list):
        logging.info("Received membership list.")
        self.slave.update_membership(membership_list)

class HealthCheck(Component):
    def process(self, _):
        return {
            "healty" : "true"
        }

class MessageReceiver(Component):
    def __init__(self, slave):
        self.slave = slave

    def process(self, message):
        logging.info("Received message: {}".format(str(message)))
        self.slave.graph_sharing.update(message["graph"])

class Slave():
    def __init__(self, slave_port, master_ip, master_port):
        self.slave_port = slave_port
        self.slave_ip = get_host_ip()

        self.master_client = Client("http://" + master_ip, master_port)
        self.membership_list = []

        self.server = Server("slave", slave_port)
        self.server.add_component_get("/healty", HealthCheck())
        self.server.add_component_post("/membership", SlaveMembership(self))
        self.server.add_component_post("/multicast", MessageReceiver(self))

        self.dissemination_constant = 2
        self.graph_sharing = GraphSharing()

    def join(self):
        self.master_client.post("/register", {
            "ip" : self.slave_ip,
            "port" : self.server.port
        })

    def update_membership(self, membership_list):
        logging.info("Updating membership....")
        if "members" not in membership_list:
            return
        membership_list = membership_list["members"]

        self.membership_list = []
        for member in membership_list:
            client = Client("http://" + member["ip"], member["port"])
            self.membership_list.append(client)

    def get_current_multicast(self):
        return self.membership_list

    def disseminate(self, multicast_list, message):
        for client in multicast_list:
            client.post("/multicast", message)

    def run(self):
        self.join()

        while True:
            time.sleep(5)
            multicast_list = self.get_current_multicast()
            multicast_message = {
                "ip" : self.slave_ip,
                "port" : self.slave_port,
                "graph" : self.graph_sharing.snapshoot()
            }
            self.disseminate(multicast_list, multicast_message)

if __name__ == "__main__":
    master_port = 5000

    # Need to give port as an argument
    master_ip = sys.argv[1]
    slave_port = sys.argv[2]

    slave = Slave(slave_port, master_ip, master_port)

    threading.Thread(target=slave.server.run).start()
    threading.Thread(target=slave.run).start()
