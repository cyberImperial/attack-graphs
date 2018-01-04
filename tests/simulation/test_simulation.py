from __future__ import absolute_import
from unittest import TestCase

from timeout_decorator import timeout
from simulation.simulation import Simulation

class TestSimuation(TestCase):
    def setUp(self):
        self.simulation = Simulation("test.json", connection_timeout=0, scan_timeout=0)
        self.connection = self.simulation.connection()

    @timeout(0.1)
    def test_connection_keeps_building_packets(self):
        packets = 10000
        while packets > 0:
            packet = self.connection.next()
            self.assertIsNotNone(packet)
            packets -= 1

    def test_discovery_ip_returns_nothing_for_missing_node(self):
        self.assertEqual(self.simulation.discovery_ip('10.1.3.8'), {})

    def test_discovery_ip_for_missing_configuration(self):
        self.assertEqual(self.simulation.discovery_ip('10.1.3.3'), {"scanned" : "false"})

    def test_discovery_ip_returns_correct_configuration(self):
        self.assertEqual(self.simulation.discovery_ip('10.1.3.1'), {"test1" : "test1"})
        self.assertEqual(self.simulation.discovery_ip('10.1.3.2'), {"test2" : "test2"})
