from __future__ import absolute_import

import os
import sys
import time
import pcapy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from threading import Lock

from topology.sniffer.devices import discover_devices
from topology.sniffer.sniffer import parse_packet

def filter_packet(packet, ip="10.1.1.1"):
    if packet is None:
        return None
    src = packet["src"]
    dst = packet["dest"]

    if src in ["10.1.5.4", "10.1.6.4", "10.1.8.4"]:
        return None
    if dst in ["10.1.5.4", "10.1.6.4", "10.1.8.4"]:
        return None

    src = [int(x) for x in src.split(".")]
    dst = [int(x) for x in dst.split(".")]
    ip =  [int(x) for x in ip.split(".")]

    if src[0] != ip[0] or src[1] != ip[1]:
        return None
    if dst[0] != ip[0] or dst[1] != ip[1]:
        return None

    return packet

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

    def get_new_packets(self, filter_packet=filter_packet):
        # For the moment we ask each device for a packet. If this proves to
        # be a problem, we need to group the reads.
        new_packets = []
        for connection in self.connections:
            try:
                (header, packet) = connection.next()
                packet = parse_packet(packet)
                # packet = filter_packet(packet)
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
