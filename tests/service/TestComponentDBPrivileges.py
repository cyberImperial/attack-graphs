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
    # a is the result of querying the DB directly ( type = list[dict])
    # b is the result of using the DBQuery component
    #       ( type = str, but has the structure of list[list[dict]])
    def check_results_match(self, a, b):
        print(b)

    def test_query_simple(self):
        a = self.DB.query('libguestfs', '1.21.24')
        b = db_request("query libguestfs 1.21.24", "database", "/vulnerability")
        self.assertTrue(self.check_results_match(a,b))

    def test_privileges_none(self):
        privs = self.DB.get_privileges('libguestfs', '1.21.24')
        b = db_request("query libguestfs 1.21.24", "database", "/privileges")
        print(b)
        print("\n||||||||")
        print(b["('libguestfs', '1.21.24')"])
        print("STOPPPP")
        self.assertTrue(self.check_results_match(privs,b['(\'libguestfs\', \'1.21.24\')']))
