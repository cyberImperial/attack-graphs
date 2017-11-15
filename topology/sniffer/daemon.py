from __future__ import absolute_import

import os, sys, time
from threading import Lock
import threading
import pcapy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import requests
from topology.sniffer.sniffer import parse_packet
from topology.graph.graph_service import graph_service
from service.components import Component
from service.server import Server, config
from database.database_service import database_service

from topology.sniffer.devices import discover_devices

class Sniffer():
    def __init__(self, shared_packets, lock, connections=discover_devices):
        self.packets = shared_packets
        self.lock = lock

        # If the default argument was given, then we call discover_devices
        if connections == discover_devices:
            self.connections = discover_devices()
        else:
            self.connections = connections

    def get_new_packets(self):
        # For the moment we ask each device for a packet. If this proves to
        # be a problem, we need to group the reads.
        new_packets = []
        for connection in self.connections:
            try:
                (header, packet) = connection.next()
                packet = parse_packet(packet)
                if packet is not None:
                    new_packets.append(packet)
                    print(packet)
            except Exception as e:
                # Non-eth packets received
                pass

        self.lock.acquire()

        for packet in new_packets:
            self.packets.append(packet)

        self.lock.release()

    def run(self):
        while True:
            self.get_new_packets()

class SniffingDaemon(Component):
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
    server.add_component_get("/newpackets", SniffingDaemon(shared_list, shared_lock))

    sniffer = Sniffer(shared_list, shared_lock)

    threading.Thread(target=server.run).start()
    threading.Thread(target=sniffer.run).start()
    threading.Thread(target=graph_service).start()
    threading.Thread(target=database_service).start()

if __name__ == "__main__":
    run_server()
