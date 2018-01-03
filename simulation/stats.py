from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import sys
import os
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

MONITOR_PORT = 3200

from simulation.singleton import singleton
from simulation.simulation import Simulation
from service.server import Server
from service.components import Component

class Monitor(Component):
    def __init__(self, engine):
        self.engine = engine

    def process(self, unused):
        return {
            "state" : self.engine.to_json()
        }

class StatsEngine():
    def __init__(self):
        self.packets = 0
        self.scans = 0
        self.scan_set = set()

    def post(self, stat):
        if isinstance(stat, PacketStat):
            self.packets += 1
        if isinstance(stat, ScanStat):
            self.scans += 1
            self.scan_set.add(stat.ip)

    def to_json(self):
        return {
            "packets" : self.packets,
            "scans" : self.scans,
            "unique_scans" : len(self.scan_set)
        }

    def __str__(self):
        return "[packets: {}, scans: {}, unique_scans: {}]".format(
            self.packets,
            self.scans,
            len(self.scan_set)
        )

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
    def __init__(self, simulation, stats_engine=StatsEngine()):
        self.simulation   = simulation
        self.stats_engine = stats_engine

        # We don't expose the engine server from the application interface
        server = Server("monitor", MONITOR_PORT)
        server.add_component_get("/stats", Monitor(stats_engine))
        threading.Thread(target=server.run).start()

    def connection(self):
        class Connection():
            def __init__(self, connection, stats_engine):
                self.connection = connection
                self.stats_engine = stats_engine

            def next(self):
                packet = self.connection.next()
                self.stats_engine.post(PacketStat(packet))
                return packet

        return Connection(self.simulation.connection(), self.stats_engine)

    def discovery_ip(self, ip):
        scan = self.simulation.discovery_ip(ip)
        self.stats_engine.post(ScanStat(ip, scan))
        return scan