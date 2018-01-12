from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.client import Client
from service.server import Server
from service.components import Component
from dissemination.util import get_host_ip
from clint.textui import colored


MASTER_DEFAULT_PORT = 5000

class MasterReceive(Component):
    def __init__(self, master):
        self.master = master

    def process(self, message):
        logger.info(colored.green("Received slave join request."))
        self.master.register(message)
        self.master.broadcast()

class Master():
    def __init__(self):
        self.membership_list = []

        self.server = Server("master", MASTER_DEFAULT_PORT)
        self.server.add_component_post("/register", MasterReceive(self))

    def register(self, registration, client_cls=Client):
        logger.info("Received register {}:{}".format(
            registration["ip"],
            registration["port"]
        ))

        # The servers are single threaded, one-connection at a time
        client = client_cls("http://" + registration["ip"], registration["port"])
        self.membership_list.append(client)

    def broadcast(self):
        logger.info(colored.yellow("Broadcasting membership...."))
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

def master_service():
    master = Master()
    logger.info("Master running on ip: {}".format(get_host_ip()))

    master.server.run()
