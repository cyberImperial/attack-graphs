from __future__ import absolute_import
from unittest import TestCase

from database.db_service import MemoryDB
from database.database_server import database_server
from service.server import config
import time, ast, os, json, requests

from multiprocessing import Process

# TODO: Replace with component...
def db_request(line, component, url):
    line = line.split("\n")[0]
    args = len(line.split(" "))
    if args != 3:
        return
    product, version = tuple(line.split(" ")[1:])
    # e.g. qemu 0.13.0
    request = json.loads("[{ \
        \"product\" : \"" + product + "\",\
        \"version\" : \"" + version + "\"\
    }]")
    try:
        full_url = "http://127.0.0.1:" + str(config[component]) + url
        r = requests.post(
            url = full_url,
            json = request)
        return(r.text)
    except Exception as e:
        pass
    print("")

class TestDBComponents(TestCase):
    @classmethod
    def setUpClass(self):
        self.process = Process(target=database_server)
        self.process.start()
        time.sleep(2)

        self.DB = MemoryDB()

    @classmethod
    def tearDownClass(self):
        os.system("kill " + str(self.process.pid))
        time.sleep(2)

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
