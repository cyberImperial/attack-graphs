from __future__ import absolute_import
from unittest import TestCase

from tests.mocks.client import use_mock_client
from tests.mocks.client import mock_client

from dissemination.master import Master

class MasterTest(TestCase):
    def setUp(self):
        use_mock_client(self)

        self.master = Master()

        self.ips = [{
            "ip" : ip,
            "port" : "5000"
        } for ip in ["10.1.1.1", "10.1.1.2", "10.1.1.3", "10.1.1.4"]]

    def set_membership_list(self):
        """Add mock clients to the membership list of the master."""
        for ip in self.ips:
            self.master.register(ip, client_cls=mock_client(self))

    def test_register_updates_membership_list(self):
        """Correct registration of membership list slave."""
        list_len = 0
        self.assertEqual(len(self.master.membership_list), 0)
        for ip in self.ips:
            list_len += 1
            self.master.register(ip, client_cls=mock_client(self))
            self.assertEqual(len(self.master.membership_list), list_len)

    def test_broadcast_sends_healthchecks_to_all_slaves(self):
        """"Check health packet is send between message exchange."""
        self.set_membership_list()
        self.master.broadcast()

        self.assertEqual(self.gets["/healty"], len(self.ips))

    def test_broadcast_membership_list_to_all_slaves(self):
        """Check broadcast updates slaves' membership lists."""
        self.set_membership_list()
        self.master.broadcast()

        self.assertEqual(self.posts["/membership"], len(self.ips))
        self.assertEqual(len(self.lastest_post["members"]), len(self.ips))
