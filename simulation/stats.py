from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simulation.simulation import Simulation

class StatsEngine():
    def post(self, stat):
        logger.info(stat)
        pass

class Stat():
    pass

class ScanStat(Stat):
    def __init__(self, scan):
        self.scan = scan

class PacketStat(Stat):
    def __init__(self, packet):
        self.packet = packet

class SimulationStat(Simulation):
    def __init__(self, simulation, stats_engine=StatsEngine()):
        self.simulation   = simulation
        self.stats_engine = stats_engine

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
        scan = self.connection.discovery_ip(ip)
        self.stats_engine.post(ScanStat(scan))
        return scan
