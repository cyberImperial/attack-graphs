import ast
import time
import requests
import json

class Node():
    def __init__(self, ip):
        self.ip = ip

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.ip == other.ip
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)

    def __str__(self):
         return str(self.ip)


class Graph():
    def __init__(self):
        self.edges = []

    def add_edge(self, n1, n2):
        for p1, p2 in self.edges:
            if p1 == n1 and p2 == n2:
                return
        self.edges.append((n1, n2))

    def __str__(self):
         return str([(str(n1), str(n2)) for (n1, n2) in self.edges])


def do_get():
    full_url = "http://127.0.0.1:30001/newpackets"
    try:
        print("Doing test request...")
        r = requests.get(full_url)
        data = json.dumps(ast.literal_eval(r.text))
        r = json.loads(data)
        return r
    except Exception as e:
        print(e)# -*- coding: utf-8 -*-
        return []

def graph_loop():
    graph = Graph()
    while True:
        out = do_get()
        for packet in out:
            src, dest = packet["src"], packet["dest"]
            graph.add_edge(Node(src), Node(dest))
        time.sleep(5)
        print(graph)
