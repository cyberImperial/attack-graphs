from __future__ import absolute_import
from unittest import TestCase
from database.db_service import MemoryDB
from service.database_server import database_server
from service.cli import db_request
import threading, time, ast

""" Basically all tests are checking if making a query through the component DBQuery
    gives the same result as querying the database directly
"""


class TestComponentDBQuery(TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     threading.Thread(target=database_server).start()
    #     time.sleep(4)
    def setUp(self):
        self.DB = MemoryDB()
        
    # a is the result of querying the DB directly ( type = list[dict])
    # b is the result of using the DBQuery component
    #       ( type = str, but has the structure of list[list[dict]])
    def check_results_match(self, a, b):
        b = ast.literal_eval(b)
        b = [item for sublist in b for item in sublist]
        if (len(a) != len(b)):
            return False
        for i in range (0, len(a)-1):
            if (a[i] != b[i]):
                 return False
        return True

    def test_query_simple(self):
        a = self.DB.query('libguestfs', '1.21.24')
        b = db_request("query libguestfs 1.21.24", "database", "/vulnerability")
        self.assertTrue(self.check_results_match(a,b))

    def test_query_2002(self):
        for version in ['1.0', '1.1', '2.1.5', '2.2.4']:
            a = self.DB.query('freebsd', version)
            b = db_request("query freebsd " + version, "database", "/vulnerability")
            self.assertTrue(self.check_results_match(a,b))

    def test_query_2007(self):
        for version in ['3.0', '4.0']:
            a = self.DB.query('metaframe', version)
            b = db_request("query metaframe " + version, "database", "/vulnerability")
            self.assertTrue(self.check_results_match(a,b))

    #        def test_query_2017(self):
    #     a = self.DB.query('windows_10', '1551')
    #     b = db_request("query windows_10 1551", "database", "/vulnerability")
    #     self.assertTrue(self.check_results_match(a,b))
