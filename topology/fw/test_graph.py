import unittest
from unittest import TestCase
from graph import Node
from graph import Graph

class TestNode(TestCase):
    def setUp(self):
        self.node = Node("192.82.21.5")
        #self.Node.running =  

    def test_get_ip_simple(self):
        self.assertEqual(self.node.ip, "192.82.21.5")

class TestGraph(TestCase):
    def setUp(self):
        self.graph = Graph()

    def add_edge_test(self):
        self.node1 = Node("192.82.21.5")
        self.node2 = Node("192.82.21.6")

        self.graph.add_edge(self.node1, self.node2)

        self.assertEqual(len(self.graph.nodes), 2)
        self.assertTrue((self.node1, self.node2) in self.graph.edges)

    def add_duplicate_node(self):
        self.add_edge_test()

        self.node1 = Node("192.82.21.5")
        self.node2 = Node("190.80.20.0")
        self.graph.add_edge(self.node1, self.node2)

        self.assertEqual(len(self.graph.nodes), 3)

    def add_duplicate_edge(self):
        self.add_edge_test()
        self.add_edge_test()
        self.assertEqual(len(self.graph.edges), 1)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestNode('test_get_ip_simple'))
    suite.addTest(TestGraph('add_edge_test'))
    suite.addTest(TestGraph('add_duplicate_node'))
    suite.addTest(TestGraph('add_duplicate_edge'))        
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

