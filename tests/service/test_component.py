from __future__ import absolute_import
from unittest import TestCase
from database.db_service import MemoryDB
from service.database_server import database_server
from service.cli import db_request
import time, ast, os

from multiprocessing import Process
from service.database_server import database_server

class TestDBComponents(TestCase):
    @classmethod
    def setUpClass(self):
        self.process = Process(target=database_server)
        self.process.start()
        time.sleep(5)

        self.DB = MemoryDB()

    @classmethod
    def tearDownClass(self):
        os.system("kill " + str(self.process.pid))
        time.sleep(5)

    # a is the result of querying the DB directly ( type = dict)
    # b is the result of using the DBPrivileges component
    #       ( type = str, but has the structure of dict)
    def check_results_match(self, a, b):
        b = ast.literal_eval(b)
        k, v = b.popitem()
        return (a["user"] == v["user"] and a["other"] == v["other"]
                and a["all"] == v["all"])


    # Basically all tests are checking if making a query through the component DBPrivileges
    # gives the same result as querying the database directly
    def test_privileges_none(self):
        a = self.DB.get_privileges('libguestfs', '1.21.24')
        b = db_request("query libguestfs 1.21.24", "database", "/privileges")
        self.assertTrue(self.check_results_match(a,b))

    def test_privileges_all(self):
        a = self.DB.get_privileges('windows_2000', '*')
        b = db_request("query windows_2000 *", "database", "/privileges")
        self.assertTrue(self.check_results_match(a,b))

    def check_results_match2(self, a, b):
        b = ast.literal_eval(b)
        b = [item for sublist in b for item in sublist]
        if (len(a) != len(b)):
            return False
        for i in range (0, len(a)-1):
            if (a[i] != b[i]):
                 return False
        return True

    # Basically all tests are checking if making a query through the component DBQuery
    # gives the same result as querying the database directly
    def test_query_simple(self):
        a = self.DB.query('libguestfs', '1.21.24')
        b = db_request("query libguestfs 1.21.24", "database", "/vulnerability")
        self.assertTrue(self.check_results_match2(a,b))

    def test_query_2002(self):
        for version in ['1.0', '1.1', '2.1.5', '2.2.4']:
            a = self.DB.query('freebsd', version)
            b = db_request("query freebsd " + version, "database", "/vulnerability")
            self.assertTrue(self.check_results_match2(a,b))

    def test_query_2007(self):
        for version in ['3.0', '4.0']:
            a = self.DB.query('metaframe', version)
            b = db_request("query metaframe " + version, "database", "/vulnerability")
            self.assertTrue(self.check_results_match2(a,b))
