from __future__ import absolute_import
from unittest import TestCase

from topology.fw.daemon import SniffingDaemon

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

class TestSniffingDaemon(TestCase):
    def build_daemon(self, shared_list):
        lock = GiveUpLock()
        return SniffingDaemon(shared_list, lock)

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
        daemon = SniffingDaemon([1, 2, 3], lock)

        lock.acquire()
        self.assertRaises(Exception, daemon.process)

    def test_lock_used_and_released(self):
        lock = GiveUpLock()
        daemon = SniffingDaemon([1, 2, 3], lock)

        daemon.process()
        self.assertEqual(1, lock.acqs)
        self.assertEqual(1, lock.rels)
        self.assertFalse(lock.acqd)
