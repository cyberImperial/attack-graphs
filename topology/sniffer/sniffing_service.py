from __future__ import absolute_import

import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import threading
from threading import Lock

from topology.sniffer.daemon import SniffingDaemon

from topology.graph.graph_service import graph_service
from service.components import Component
from service.server import Server, config
from database.database_service import database_service

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

def run_server():
    shared_lock = Lock()
    shared_list = []

    server = Server("sniffer", 30001)
    server.add_component_get("/newpackets", PacketExporter(shared_list, shared_lock))

    sniffer = SniffingDaemon(shared_list, shared_lock)

    threading.Thread(target=server.run).start()
    threading.Thread(target=sniffer.run).start()
    threading.Thread(target=graph_service).start()
    threading.Thread(target=database_service).start()

if __name__ == "__main__":
    run_server()
