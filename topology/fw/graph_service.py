from populator import Populator

import ast
import time
import requests
import json
import threading

from threading import Lock
from graph import Graph
from graph import Node

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
