from __future__ import absolute_import
from unittest import TestCase

from topology.sniffer.sniffing_service import PacketExporter
from topology.sniffer.daemon import SniffingDaemon
from unittest.mock import MagicMock

class GiveUpLock():
    def __init__(self):
        self.acqd = False
        self.acqs = 0
        self.rels = 0

    def acquire(self):
        if self.acqd:
            raise Exception('GiveUpLock acquired while kept.')
        else:
            self.acqs += 1
            self.acqd = True

    def release(self):
        if self.acqd:
            self.acqd = False
        self.rels += 1

class TestPacketExporter(TestCase):
    def build_daemon(self, shared_list):
        lock = GiveUpLock()
        return PacketExporter(shared_list, lock)

    def test_no_new_packets(self):
        self.assertListEqual([], self.build_daemon([]).process())

    def test_all_packets_are_retreived(self):
        lst = [1, {"x" : "y"}]
        self.assertListEqual(lst[:], self.build_daemon(lst).process())

    def test_shared_list_becomes_empty(self):
        lst = [1, 2, 3]
        self.build_daemon(lst).process()
        self.assertListEqual(lst, [])

    def test_daemon_waits_for_lock_release(self):
        lock = GiveUpLock()
        daemon = PacketExporter([1, 2, 3], lock)

        lock.acquire()
        self.assertRaises(Exception, daemon.process)

    def test_lock_used_and_released(self):
        lock = GiveUpLock()
        daemon = PacketExporter([1, 2, 3], lock)

        daemon.process()
        self.assertEqual(1, lock.acqs)
        self.assertEqual(1, lock.rels)
        self.assertFalse(lock.acqd)

class TestSniffingDaemon(TestCase):
    RAW_TCP_PACKET = b'\\\x93\xa2\xf4\xf7\xf6\xf0\x9f\xc2\x18\xa2\xdf\x08\x00E\x00\x004x\x98@\x00:\x06\x84Yh\x10\x19\xeb\xc0\xa8\x01/\x01\xbb\xb0\xf0v\xb1j.\xc2^L\xe3\x80\x10\x00 t\x99\x00\x00\x01\x01\x05\n\xc2^L\xc3\xc2^L\xe3'
    RES_TCP_PACKET = {'dest': '192.168.1.47', 'src': '104.16.25.235', 'version': '4', 'ip_header_length': '5', 'ttl': '58', 'transport': { 'src_port': '443', 'ack': '3260959971', 'dest_port': '45296', 'seq': '1991338542'}, 'transport_type': 'TCP'}

    def good_connection(self):
        connection = lambda: None
        connection.next = MagicMock(return_value = ("", self.RAW_TCP_PACKET))
        return connection

    def bad_connection(self):
        connection = lambda: None
        connection.next = MagicMock(return_value = ("", b'sarmale'))
        return connection

    def test_single_connection_gets_good_packet(self):
        packets, lock = [], GiveUpLock()
        sniffer = SniffingDaemon(packets, lock, [self.good_connection()])
        sniffer.get_new_packets()

        self.assertListEqual(packets, [self.RES_TCP_PACKET])

    def test_malformated_packets_are_dropped(self):
        packets, lock = [], GiveUpLock()
        sniffer = SniffingDaemon(packets, lock, [self.bad_connection()])
        sniffer.get_new_packets()

        self.assertListEqual(packets, [])

    def test_packets_from_all_connections_are_fetched(self):
        packets, lock = [], GiveUpLock()
        sniffer = SniffingDaemon(packets, lock, [self.good_connection()] * 10 + [self.bad_connection] * 5)
        sniffer.get_new_packets()

        self.assertListEqual(packets, [self.RES_TCP_PACKET] * 10)

    def test_daemon_waits_for_lock_release(self):
        packets, lock = [], GiveUpLock()
        sniffer = SniffingDaemon(packets, lock, [self.good_connection()] * 10 + [self.bad_connection] * 5)

        lock.acquire()
        self.assertRaises(Exception, sniffer.get_new_packets)

    def test_lock_used_and_released(self):
        packets, lock = [], GiveUpLock()
        sniffer = SniffingDaemon(packets, lock, [self.good_connection()] * 10 + [self.bad_connection] * 5)
        sniffer.get_new_packets()

        self.assertEqual(1, lock.acqs)
        self.assertEqual(1, lock.rels)
        self.assertFalse(lock.acqd)
