from __future__ import absolute_import

import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import threading
from threading import Lock

from topology.sniffer.daemon import SniffingDaemon
from topology.sniffer.devices import open_connection

from service.components import Component
from service.server import Server
from service.server import config

class PacketExporter(Component):
    def __init__(self, shared_packets, lock):
        self.shared_packets = shared_packets
        self.lock = lock

    def process(self, unused=None):
        self.lock.acquire()

        packets = self.shared_packets[:]
        self.shared_packets[:] = []

        self.lock.release()
        return packets

class SniffingService():
    def __init__(self, device):
        shared_lock = Lock()
        shared_list = []

        self.server = Server("sniffer", config["sniffer"])
        self.server.add_component_get("/newpackets",
            PacketExporter(shared_list, shared_lock))

        if device is None:
            self.daemon = SniffingDaemon(shared_list, shared_lock)
        else:
            self.daemon = SniffingDaemon(shared_list, shared_lock, connections=open_connection(device))

def sniffing_service(device=None):
    service = SniffingService(device)

    threading.Thread(target=service.server.run).start()
    threading.Thread(target=service.daemon.run).start()
    while True:
        pass

if __name__ == "__main__":
    sniffing_service()
