from __future__ import absolute_import
from unittest import TestCase
from topology.fw.graph import Node
from topology.fw.graph import Graph

class TestNode(TestCase):
    def setUp(self):
        self.node = Node("192.82.21.5")
        #self.Node.running =  

    def test_get_ip_simple(self):
        self.assertEqual(self.node.ip, "192.82.21.5")

class TestGraph(TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_add_edge(self):
        self.node1 = Node("192.82.21.5")
        self.node2 = Node("192.82.21.6")

        self.graph.add_edge(self.node1, self.node2)

        self.assertEqual(len(self.graph.nodes), 2)
        self.assertTrue((self.node1, self.node2) in self.graph.edges)

    def test_add_duplicate_node(self):
        self.test_add_edge()

        self.node1 = Node("192.82.21.5")
        self.node2 = Node("190.80.20.0")
        self.graph.add_edge(self.node1, self.node2)

        self.assertEqual(len(self.graph.nodes), 3)

    def test_add_duplicate_edge(self):
        self.test_add_edge()
        self.test_add_edge()
        self.assertEqual(len(self.graph.edges), 1)

