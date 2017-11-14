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
from service.database_server import database_server

def timeout_dispach(function, timeout, *args):
    t = threading.Thread(target=function, args=args)
    t.start()
    t.join(timeout=timeout)

def discover_devices():
    # WARN: Untested
    devices = pcapy.findalldevs()

    connections = []
    read_packets = {}
    received_eth_packets = {}
    for dev in devices:
        try:
            connection = pcapy.open_live(dev , 65536 , True , 100)
            connections.append(connection)

            # Decorate the objects with number of already read packets
            read_packets[connection] = 0
            received_eth_packets[connection] = 0

            if connection.getnonblock():
                # Set each connection to be blocking
                connection.setnonblock(False)
        except Exception as e:
            print("Device " + dev + " failed.")

    # Wait for a timeout capture and select only the interfaces that exchange packets
    print("Waiting to test interfaces...")
    time.sleep(5)

    # Set a number of iterations in which we decide which interfaces to listen at
    iterations = 10
    print("Checking for devices that have eth packets...")
    while iterations > 0:
        iterations -= 1
        for connection in connections:
            (received, dropped1, dropped2) = connection.stats()
            used = received - dropped1 - dropped2

            if used <= read_packets[connection] + 1:
                continue

            try:
                def next_packet():
                    (header, packet) = connection.next()
                    packet = parse_packet(packet)

                    # If we arrive here, then the packet is an eth packet
                    received_eth_packets[connection] += 1
                timeout_dispach(next_packet, 0.5)
            except Exception as e:
                # Ignore non-eth packets
                pass

    # Filter out the connection that did not receive any eth packet
    all_connections = [conn for conn in connections]
    print("Filtering devices...")
    connections = []
    for connection in all_connections:
        if received_eth_packets[connection] > 0:
            connections.append(connection)
        else:
            # This will call __exit__, so the unused connections get closed
            del connection

    print("Connections opened: " + str(len(connections)))
    return connections

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
    threading.Thread(target=graph_loop).start()
    threading.Thread(target=database_server).start()

if __name__ == "__main__":
    run_server()
