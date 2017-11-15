from __future__ import absolute_import
import unittest
from unittest import TestCase
from topology.graph.populator import Populator
from database.memory_db import MemoryDB
from topology.graph.graph import Graph
from topology.graph.graph import Node
import json

class TestPopulator(TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.add_edge(Node("190.80.50.0"), Node("190.80.50.1"))
        self.graph.add_edge(Node("190.80.50.1"), Node("190.80.50.2"))

        self.json1 = {
           "Host":{
              "os":"ASUS RT-N56U WAP (Linux 3.4)",
              "ip":"192.30.252.154",
              "RunningServices":[
                 {
                    "Port":{
                       "portid":"443",
                       "protocol":"tcp"
                    },
                    "Service":{
                       "name":"https",
                       "product":"GitHub.com",
                       "version":"attributeMissing",
                       "state_open":"open",
                       "reason":"syn-ack"
                    }
                 },
                 {
                    "Port":{
                       "portid":"80",
                       "protocol":"tcp"
                    },
                    "Service":{
                       "name":"http",
                       "product":"GitHub.com",
                       "version":"attributeMissing",
                       "state_open":"open",
                       "reason":"syn-ack"
                    }
                 }
              ]
           }
        }

        self.json2 = {
           "Host":{
              "os":"ASUS ROG WAP (Linux 3.4)",
              "ip":"192.30.250.155",
              "RunningServices":[
                 {
                    "Port":{
                       "portid":"443",
                       "protocol":"tcp"
                    },
                    "Service":{
                       "name":"Demo",
                       "product":"GitHub.com",
                       "version":"3.1",
                       "state_open":"open",
                       "reason":"syn-ack"
                    }
                 },
                 {
                    "Port":{
                       "portid":"80",
                       "protocol":"tcp"
                    },
                    "Service":{
                       "name":"Demo2",
                       "product":"GitHub.com",
                       "version":"3.0",
                       "state_open":"open",
                       "reason":"syn-ack"
                    }
                 }
              ]
           }
        }

    def test_get_batch(self):
        populator = Populator(self.graph)
        populator.threads = 3

        i1, i2, mybatch = populator.get_batch(self.graph)

        self.assertEqual(mybatch[0], '190.80.50.0')
        self.assertEqual(mybatch[1], "190.80.50.1")
        self.assertEqual(mybatch[2], "190.80.50.2")

    def test_get_ips(self):
        def discovery_ip2(ip):
            return {
                "ip" : ip
            }

        populator = Populator(self.graph, discovery_ip2)
        results = populator.get_ips(["190.80.50.0", "190.80.50.1"])

        self.assertDictEqual(results[0], {"ip" : "190.80.50.0"})
        self.assertDictEqual(results[1], {"ip" : "190.80.50.1"})

    def test_good_formatted_vulnerabilities_are_added(self):
        class MockDBClient():
            def db_request(self, resource, product, version):
                if "vulnerability" in resource:
                    return {"vul" : "vul"}
                if "privileges" in resource:
                    return {"pri" : "pri"}
                return None
        populator = Populator(self.graph, db_client=MockDBClient())

        init_results = [self.json1, self.json2]
        final_results = populator.add_vulnerabilities(init_results)

        for result in final_results:
            self.assertDictEqual(result["Host"]["RunningServices"][0]["Vulnerability"], {"vul" : "vul"})
            self.assertDictEqual(result["Host"]["RunningServices"][0]["Privileges"], {"pri" : "pri"})

    def test_update_graph(self):

        populator = Populator(self.graph)
        res = [self.json1, self.json2]

        populator.update_graph(self.graph, res, 0, 2)

        for i in range(0, 2):
            self.assertDictEqual(self.graph.nodes[i].running, res[i])
