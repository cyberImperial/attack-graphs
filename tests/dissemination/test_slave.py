from __future__ import absolute_import
from unittest import TestCase

# mock_client decorated test class with gets, ports and lastest_post
from tests.mocks.client import mock_client

from dissemination.slave import Slave

class SlaveTest(TestCase):
    def setUp(self):
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
            len(self.slave.get_current_multicast()),
            len(self.membership_list["members"])
        )

    def test_disseminate_sends_messages_to_different_recipients(self):
        pass

    def test_disseminate_sends_at_most_dissemination_constant_messages(self):
        pass

    def test_disseminate_sends_at_least_one_message(self):
        pass
