from __future__ import absolute_import

import os, sys, time
from threading import Lock
import threading
import pcapy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import requests
from topology.fw.sniffer import parse_packet
from topology.fw.graph_service import graph_loop
from service.components import Component
from service.server import Server, config

class Sniffer():
    def __init__(self, shared_packets, lock):
        self.packets = shared_packets
        self.lock = lock

    def run(self):
        devices = pcapy.findalldevs()
        print("Starting to listen on decived:" + str(devices))

        # connections = []
        # for dev in devices:
        #     try:
        #         connection = pcapy.open_live(dev , 65536 , True , 0)
        #         connections.append(connection)
        #     except Exception as e:
        #         print("Device " + dev + " failed.")

        connections = [pcapy.open_live("wlp8s0" , 65536 , True , 0)]

        while True:
            new_packets = []
            for cap in connections:
                (header, packet) = cap.next()
                packet = parse_packet(packet)
                if packet is not None:
                    new_packets.append(packet)

            self.lock.acquire()

            for packet in new_packets:
                self.packets.append(packet)

            self.lock.release()

class SniffingDaemon(Component):
    def __init__(self, shared_packets, lock):
        self.shared_packets = shared_packets
        self.lock = lock

    def process(self, unused):
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
    threading.Thread(target=graph_loop).start()

if __name__ == "__main__":
    run_server()
