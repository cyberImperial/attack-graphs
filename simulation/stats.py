from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulation.simulation import Simulation

class StatsEngine:
    stats = {
        "packets" : 0,
        "scans" : 0,
        "scan_set" : set(),
        "backlog" : []
    }
    backlog_threshold = 10

    @classmethod
    def update_backlog(cls):
        cls.stats["backlog"].append(cls.to_json())
        if len(cls.stats["backlog"]) > cls.backlog_threshold:
            logger.info("Backlog dumped to file.")
            with open("backlog.log", "a") as backlog:
                for entry in cls.stats["backlog"]:
                    backlog.write("{}, {}, {}".format(
                        entry["packets"],
                        entry["scans"],
                        entry["unique_scans"]
                    ))
                    backlog.write("\n")
            cls.stats["backlog"] = []

    @classmethod
    def post(cls, stat):
        stats = cls.stats
        if isinstance(stat, PacketStat):
            stats["packets"] += 1
        if isinstance(stat, ScanStat):
            stats["scans"] += 1
            stats["scan_set"].add(stat.ip)
        cls.update_backlog()

    @classmethod
    def to_json(cls):
        return {
            "packets" : cls.stats["packets"],
            "scans" : cls.stats["scans"],
            "unique_scans" : len(cls.stats["scan_set"])
        }

class Stat():
    pass

class ScanStat(Stat):
    def __init__(self, ip, scan):
        self.ip = ip

    def __str__(self):
        return "[scan: {}]".format(str(self.ip))

class PacketStat(Stat):
    def __init__(self, packet):
        self.packet = packet

    def __str__(self):
        return "[packet: {}]".format(str(self.packet))

class SimulationStat(Simulation):
    def __init__(self, simulation):
        self.simulation = simulation

    def connection(self):
        class Connection():
            def __init__(self, connection):
                self.connection = connection

            def next(self):
                packet = self.connection.next()
                StatsEngine.post(PacketStat(packet))
                return packet

        return Connection(self.simulation.connection())

    def discovery_ip(self, ip):
        scan = self.simulation.discovery_ip(ip)
        StatsEngine.post(ScanStat(ip, scan))
        return scan
