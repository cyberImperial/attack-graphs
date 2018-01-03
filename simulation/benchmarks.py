from __future__ import absolute_import

import sys
import os
import subprocess
import time
import signal
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from topology.graph.graph import Graph
from topology.graph.graph import Node
from random import randint

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
app = os.path.join(ROOT, "service.py")
processes = []

def get_path(benchmark):
    PATH = os.path.dirname(os.path.realpath(__file__))
    PATH = os.path.join(PATH, "confs")
    PATH = os.path.join(PATH, "{}.json".format(benchmark))
    return PATH

def clear_processes():
    os.system("pkill -9 python")
    # print("Killing the running services.")
    # for process in processes:
    #     print("Killing process {}".format(process.pid))
    #     os.kill(process.pid, signal.SIGINT)

def add_process(command):
    global processes

    print("> {}".format(command))
    slave_proc = subprocess.Popen(command.split(" "),  shell=False)
    processes.append(slave_proc)

def generate_graph(nodes, edges):
    graph = Graph()
    while edges > 0:
        def int_to_ip(value):
            a = (value >> 24) & 15
            b = (value >> 16) & 15
            c = (value >> 8) & 15
            d = (value >> 0) & 15
            return "{}.{}.{}.{}".format(a, b, c, d)
        edges -= 1
        n1 = int_to_ip(randint(0, nodes))
        n2 = int_to_ip(randint(0, nodes))
        graph.add_edge(Node(n1), Node(n2))
    return graph

def export_graph(graph, benchmark):
    os.system("touch {}".format(get_path(benchmark)))
    with open(get_path(benchmark), "w") as config:
        config.write(str(graph.to_json()))

def delete_simulation_config(benchmark):
    os.remove(get_path(benchmark))

def create_simulation_config(nodes, edges, benchmark):
    export_graph(generate_graph(nodes, edges), benchmark)

def create_master(benchmark):
    add_process("sudo python3 {} master -s {}.json -b".format(app, benchmark))

def clear_backlog():
    try:
        os.remove(os.path.join(ROOT, "backlog.log"))
    except OSError:
        pass

def scenario1():
    name = "small_complete"
    clear_backlog()
    create_simulation_config(10, 100, name)
    create_master(name)
    time.sleep(10)
    delete_simulation_config(name)
    clear_processes()
    
if __name__ == "__main__":
    scenario1()
