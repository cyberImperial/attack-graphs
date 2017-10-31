from __future__ import absolute_import
from unittest import TestCase
from database.db_service import MemoryDB

class TestMemoryDB(TestCase):
    def setUp(self):
        self.DB = MemoryDB()

    def check_for_CVE(self, name, version, cve):
        for v in self.DB.query(name, version):
            if v["id"] == cve:
                return True
        return False

    def test_query_simple(self):
        self.assertTrue(self.check_for_CVE('libguestfs', '1.21.24', "CVE-2013-2124"))

    def test_query_2002(self):
        for version in ['1.0', '1.1', '2.1.5', '2.2.4']:
            self.assertTrue(self.check_for_CVE('freebsd', version, "CVE-1999-0001"))

    def test_query_2007(self):
        for version in ['3.0', '4.0']:
            self.assertTrue(self.check_for_CVE('metaframe', version, "CVE-2007-2850"))

    def test_query_2017(self):
        self.assertTrue(self.check_for_CVE('windows_10', '1511', "CVE-2017-0001"))

    def test_privileges_none(self):
        privs = self.DB.get_privileges('libguestfs', '1.21.24')
        self.assertFalse(privs["user"])
        self.assertFalse(privs["other"])
        self.assertFalse(privs["all"])

    def test_privileges_all(self):
        privs = self.DB.get_privileges('windows_2000', '*')
        self.assertTrue(privs["user"])
        self.assertTrue(privs["other"])
        self.assertTrue(privs["all"])
