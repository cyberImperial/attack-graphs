from __future__ import absolute_import

import sys
import os
import subprocess
import time
import signal
import psutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.server import config
from topology.graph.graph import Graph
from topology.graph.graph import Node
from service.client import LocalClient
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
    this_proc = os.getpid()
    for proc in psutil.process_iter():
        procd = proc.as_dict(attrs=['pid', 'name'])
        if "python" in str(procd['name']) and procd['pid'] != this_proc:
            proc.kill()

def add_process(command):
    global processes

    print("> {}".format(command))
    slave_proc = subprocess.Popen(command.split(" "),  shell=False)
    processes.append(slave_proc)

def generate_graph(nodes, edges):
    graph = Graph()
    while edges > 0:
        def int_to_ip(value):
            a = (value >> 24) & 255
            b = (value >> 16) & 255
            c = (value >> 8) & 255
            d = (value >> 0) & 255
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

def create_master(benchmark):
    add_process("sudo python3 {} master -s {}.json".format(app, benchmark))

def create_slave(benchmark, port):
    add_process("sudo python3 {} slave -m 127.0.0.1 -p {} -s {}.json".format(app, port, benchmark))

def take_snapshot():
    graph = LocalClient(config["graph"]).get("/graph")
    return Graph.from_json(graph)

def process_snapshots(snapshots, processor):
    return [processor(s) for s in snapshots]

def build_scenario(name, nodes, edges, slaves, snaps, pause, processor):
    graph = generate_graph(nodes, edges)
    export_graph(graph, name)

    create_master(name)
    for i in range(slaves):
        create_slave(name, 1000 + i)

    snapshots = [graph]
    for i in range(0, snaps):
        time.sleep(pause)
        snapshots.append(take_snapshot())
    delete_simulation_config(name)
    nodes = process_snapshots(snapshots, processor)

    clear_processes()
    return nodes

def nbr_service(graph):
    return len([s for s in graph.nodes if s.running["scanned"] is not "false"])

def scenario_stats(name, nodes, edges, snaps, pause):
    all_stats = []
    for slaves in range(0, 2):
        all_stats.append(build_scenario(
            name=name,
            nodes=nodes,
            edges=edges,
            slaves=slaves,
            snaps=snaps,
            pause=pause,
            processor=lambda graph: (len(graph.nodes), len(graph.edges), nbr_service(graph))
        ))
    print(all_stats)

if __name__ == "__main__":
    scenario_stats("small_scenario", 30, 100, 10, 1)
# [301, 0, 76, 76, 130, 130, 171, 205, 205, 223, 223, 237, 254, 254, 262, 262, 271, 275, 275, 278, 278]
# [301, 2, 81, 81, 139, 139, 184, 217, 217, 234, 234, 246, 259, 259, 264, 264, 271, 275, 275, 280, 281]

# [300, 0, 77, 135, 170, 196, 219, 239, 253, 259, 268]
# [301, 0, 80, 135, 170, 203, 225, 245, 258, 267, 272]
