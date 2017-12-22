from __future__ import absolute_import
from unittest import TestCase

from tests.mocks.client import use_mock_client
from tests.mocks.client import mock_client

from dissemination.slave import Slave

class SlaveTest(TestCase):
    def setUp(self):
        use_mock_client(self)

        self.master_port = 1001
        self.master_url  = "http://test"
        self.slave_port  = 1000

        self.slave = Slave(
            self.slave_port,
            self.master_url,
            self.master_port,
            client_cls=mock_client(self)
        )

        self.membership_list = {
            "members" : [{
                "ip"   : "1.1.1.1",
                "port" : "5000"
            },{
                "ip"   : "1.1.1.2",
                "port" : "5000"
            }
            ]
        }

    def test_join_sends_register_to_master(self):
        self.slave.join()
        self.assertEqual(self.posts["/register"], 1)
        self.assertEqual(self.lastest_post["port"], self.slave_port)

    def test_update_membership(self):
        self.slave.update_membership(self.membership_list)
        self.assertEqual(
            len(self.slave.get_current_broadcast()),
            len(self.membership_list["members"])
        )

    def test_disseminate_sends_correct_number_of_messages(self):
        self.slave.update_membership(self.membership_list)
        self.slave.disseminate(self.slave.get_current_broadcast(), {"test": "test"})
        self.assertEqual(
            len(self.membership_list["members"]),
            self.posts["/multicast"]
        )
        self.assertEqual(self.lastest_post, {"test": "test"})

    def test_current_multicast_is_made_to_different_recipients(self):
        self.slave.update_membership(self.membership_list)
        tries = 100
        while tries > 0:
            multicast = self.slave.get_current_multicast()
            self.assertEqual(len(multicast), len(list(set(multicast))))
            tries -= 1

    def test_current_multicast_sends_at_most_dissemination_constant_messages(self):
        self.slave.update_membership(self.membership_list)
        tries = 100
        while tries > 0:
            multicast = self.slave.get_current_multicast()
            self.assertTrue(len(multicast) < self.slave.dissemination_constant)
            tries -= 1

    def test_current_multicast__sends_at_least_one_message(self):
        self.slave.update_membership(self.membership_list)
        tries = 100
        while tries > 0:
            multicast = self.slave.get_current_multicast()
            self.assertTrue(len(multicast) > 1)
            tries -= 1
