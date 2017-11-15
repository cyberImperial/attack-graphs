from __future__ import absolute_import

import os
import sys
import time
import pcapy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from threading import Lock

from topology.sniffer.devices import discover_devices
from topology.sniffer.sniffer import parse_packet

class SniffingDaemon():
    """
    A daemon that itertes through a series of device connections
    and gets sniffed devices.
    """
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
