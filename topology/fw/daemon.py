from __future__ import absolute_import

import os, sys, time
from threading import Lock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from topology.fw.sniffer import parse_packet
from service.components import Component
from service.server import Server, config

class SniffingDaemon(Component):
    def __init__(self, shared_packets, lock):
        self.shared_packets = shared_packets
        self.lock = lock

    def process(self, json):
        self.lock.acquire()

        packets = self.shared_packets
        self.shared_packets = []

        self.lock.release()
        return packets

def run_server():
    server = Server("sniffer", 30001)

    server.add_component_post("/new_packets", SniffingDaemon(["dani mocanu"], Lock()))
    server.run()

    # threading.Thread(target=database_server).start()
    # threading.Thread(target=cli).start()

if __name__ == "__main__":
    run_server()
