from __future__ import absolute_import
from unittest import TestCase
from database.db_service import MemoryDB
from service.database_server import database_server
from service.cli import db_request
import threading, time, ast

""" Basically all tests are checking if making a query through the component DBPrivileges
    gives the same result as querying the database directly
"""


class TestComponentDBPrivileges(TestCase):

    def setUp(self):
        self.DB = MemoryDB()
    # a is the result of querying the DB directly ( type = dict)
    # b is the result of using the DBPrivileges component
    #       ( type = str, but has the structure of dict)
    def check_results_match(self, a, b):
        b = ast.literal_eval(b)
        k, v = b.popitem()
        return (a["user"] == v["user"] and a["other"] == v["other"]
                and a["all"] == v["all"])

    def test_privileges_none(self):
        a = self.DB.get_privileges('libguestfs', '1.21.24')
        b = db_request("query libguestfs 1.21.24", "database", "/privileges")
        self.assertTrue(self.check_results_match(a,b))

    def test_privileges_all(self):
        a = self.DB.get_privileges('windows_2000', '*')
        b = db_request("query windows_2000 *", "database", "/privileges")
        self.assertTrue(self.check_results_match(a,b))
