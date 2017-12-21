from __future__ import absolute_import
from unittest import TestCase

from database.memory_db import MemoryDB
from database.database_service import database_service
from database.database_service import DBClient
from service.server import config
import time, ast, os, json, requests

from multiprocessing import Process

class TestDBComponents(TestCase):
    @classmethod
    def setUpClass(self):
        self.process = Process(target=database_service)
        self.process.start()
        time.sleep(2)

        self.client = DBClient(config["database"])
        self.DB = MemoryDB()

    @classmethod
    def tearDownClass(self):
        os.system("kill " + str(self.process.pid))
        time.sleep(2)

    # Basically all tests are checking if making a query through the component DBPrivileges
    # gives the same result as querying the database directly
    def test_privileges_none(self):
        a = self.DB.get_privileges('libguestfs', '1.21.24')
        b = self.client.db_request("/privileges", 'libguestfs', '1.21.24')
        self.assertEqual(a, b)

    def test_privileges_all(self):
        a = self.DB.get_privileges('windows_2000', '*')
        b = self.client.db_request("/privileges", 'windows_2000', '*')
        self.assertEqual(a, b)

    # Basically all tests are checking if making a query through the component DBQuery
    # gives the same result as querying the database directly
    def test_query_simple(self):
        a = self.DB.query('libguestfs', '1.21.24')
        b = self.client.db_request("/vulnerability", 'libguestfs', '1.21.24')
        self.assertEqual(a, b)

    def test_query_2002(self):
        for version in ['1.0', '1.1', '2.1.5', '2.2.4']:
            a = self.DB.query('freebsd', version)
            b = self.client.db_request("/vulnerability", 'freebsd', version)
            self.assertEqual(a, b)

    def test_query_2007(self):
        for version in ['3.0', '4.0']:
            a = self.DB.query('metaframe', version)
            b = self.client.db_request("/vulnerability", 'metaframe', version)
            self.assertEqual(a, b)
