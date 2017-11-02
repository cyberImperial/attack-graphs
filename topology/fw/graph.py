import ast
import time
import requests
import json
import threading
import timeit

from random import random
from service.discovery import discovery_ip
from threading import Lock

class Node():
    def __init__(self, ip):
        self.ip = ip
        self.running = None

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.ip == other.ip
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)

    def __str__(self):
        if self.running == None:
            return str(self.ip)
        return str((self.ip, self.running))

class Graph():
    def __init__(self):
        self.edges = []
        self.nodes = []
        self.lock = Lock()

        # The index of the first node not populated yet
        self.populated_nodes = 0

    def add_edge(self, n1, n2):

        firstInside = False
        secondInside = False

        for n in self.nodes:
            if n == n1:
                firstInside = True
            if n == n2:
                secondInside = True

        if not firstInside:
            self.nodes.append(n1)

        if not secondInside:
            self.nodes.append(n2)

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
        print(e)
        return []

class Populator():
    def __init__(self, graph):
        self.graph = graph
        self.threads = 1

    def populate_nodes(self):
        graph = self.graph
        # Create the batch
        i1 = graph.populated_nodes
        i2 = min(i1 + self.threads, len(graph.nodes))

        graph.lock.acquire()
        batch = []
        for i in range(i1, i2):
            batch.append(graph.nodes[i].ip)
        graph.populated_nodes = i2
        graph.lock.release()

        # Getting the process results

        # results_lock = Lock()
        #
        # results = []
        # pool = []
        # for task in batch:
        #     def wrapper(results, lock, task):
        #         time.sleep(random())
        #
        #         ans = discovery_ip(task)
        #
        #         lock.acquire()
        #         results.append(ans)
        #         lock.release()
        #
        #     pool.append(threading.Thread(
        #         target = wrapper,
        #         args = (results, results_lock, task)
        #     ))
        #
        # for thread in pool:
        #     thread.start()
        # for thread in pool:
        #     thread.join()

        results = []
        for task in batch:
            results.append(discovery_ip(task))

        # Puting the results on the graph
        graph.lock.acquire()
        idx = 0
        for i in range(i1, i2):
            graph.nodes[i].running = results[idx]
            idx += 1
        graph.lock.release()

    def populate_loop(self):
        time.sleep(10)
        while True:
            self.populate_nodes()
            print("Graph populated:")
            print(self.graph)

def graph_loop():
    graph = Graph()
    populator = Populator(graph)

    threading.Thread(target=populator.populate_loop).start()
    while True:
        out = do_get()

        graph.lock.acquire()
        for packet in out:
            src, dest = packet["src"], packet["dest"]

            if "255" in src or "255" in dest:
                continue

            graph.add_edge(Node(src), Node(dest))
        graph.lock.release()

        time.sleep(5)
        print(len(graph.nodes))
