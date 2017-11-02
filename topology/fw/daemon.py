from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from topology.fw.sniffer import parse_packet
from service.components import Component
from service.server import Server

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
    # threading.Thread(target=database_server).start()
    # threading.Thread(target=cli).start()
    pass    

if __name__ == "__main__":
    run_server()
