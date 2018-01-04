from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import os
import sys
import time
import pcapy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from threading import Lock

from topology.sniffer.devices import discover_devices
from topology.sniffer.sniffer import parse_packet

def filter_packet(packet, mask):
    if packet is None:
        return None
    src = packet["src"]
    dst = packet["dest"]

    mask_ip, mask_bits = mask.split("/")[0], int(mask.split("/")[1])
    def bitmask(ip):
        int_ip = [int(x) for x in ip.split(".")]
        return (int_ip[0] << 24) + (int_ip[1] << 16) + (int_ip[2] << 8) + int_ip[3]
    def check_ip(ip):
        check_mask = (1 << 32 - 1) - (1 << mask_bits - 1)
        ip_bits    = bitmask(ip)      & check_mask
        check_bits = bitmask(mask_ip) & check_mask
        # logger.debug("{0:b}".format(ip_bits))
        # logger.debug("{0:b}".format(check_bits))
        return ip_bits == check_bits

    if not check_ip(src) and not check_ip(dst):
        return None
    if not check_ip(src):
        packet["dest"] = "255.255.255.255"
    if not check_ip(dst):
        packet["src"] = "255.255.255.255"

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

    def get_new_packets(self, filter_mask="10.1.1.1/32"):
        # For the moment we ask each device for a packet. If this proves to
        # be a problem, we need to group the reads.
        new_packets = []
        for connection in self.connections:
            try:
                (header, packet) = connection.next()
                packet = parse_packet(packet)
                packet = filter_packet(packet, filter_mask)
                if packet is not None:
                    new_packets.append(packet)
                    logger.debug(packet)
            except Exception as e:
                # Non-eth packets received
                pass

        self.lock.acquire()

        for packet in new_packets:
            self.packets.append(packet)

        self.lock.release()

    def run(self, filter_mask="10.1.1.1/32"):
        while True:
            self.get_new_packets(filter_mask)
