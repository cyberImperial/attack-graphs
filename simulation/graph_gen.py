from __future__ import absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from topology.graph.graph import Graph
from topology.graph.graph import Node
from random import randint, random, shuffle

from clint.textui import colored

def generate_graph(nodes, max_edges, decorate=False):
    graph = Graph()

    def int_to_ip(value):
        if decorate:
            if random() > 0.5:
               a = int(random() * 255)
            else:
               a = (value >> 24) & 255
        else:
            a = (value >> 24) & 255
        b = (value >> 16) & 255
        c = (value >> 8) & 255
        d = (value >> 0) & 255
        return "{}.{}.{}.{}".format(a, b, c, d)

    nodes = [Node(int_to_ip(i)) for i in range(0, nodes)]
    for n in nodes:
        r = random()
        if r < 0.25:
            n.running = {
                "scanned" : "false",
                "Host": {
                  "os" : "ACER RT-N56U WAP (Linux 3.2)",
                  "ip" : n.ip,
                  "RunningServices": [{
        "Port":{
        "portid":"443",
        "protocol":"tcp"
      },
      "Service" : {
        "name":"libguestfs",
        "product":"libguestfs",
        "version":"1.21.24",
        "state_open":"open",
        "reason":"syn-ack"
      }}]
              }
            }
        elif r < 0.5:
            n.running = {
                "scanned" : "false",
                "Host": {
                  "os" : "ASUS K570 (Linux 3.4)",
                  "ip" : n.ip,
                  "RunningServices": []
              }
            }
        elif r < 0.75:
            n.running = {
                "scanned" : "false",
                "Host": {
                  "os" : "windows_server",
                  "ip" : n.ip,
                  "RunningServices": [{
        "Port":{
        "portid":"80",
        "protocol":"tcp"
      },
      "Service" : {
        "name":" nginx",
        "product":"lb",
        "version":"2.5",
        "state_open":"open",
        "reason":"syn-ack"
      }}]
              }
            }
        else:
            n.running = {
                "scanned" : "false",
                "Host": {
                  "os" : "ACER RT-N56U WAP (Linux 3.2)",
                  "ip" : n.ip,
                  "RunningServices": []
              }
            }

    edges = [(n1, n2) for n1 in nodes for n2 in nodes]
    shuffle(edges)

    for n1, n2 in edges:
        if max_edges == 0:
            break
        before = len(graph.edges)
        graph.add_edge(n1, n2)
        if len(graph.edges) > before:
            max_edges -= 1
    return graph

if __name__ == "__main__":
    """
    Arguments must be number of nodes and number of edges.
    """

    if len(sys.argv) != 4:
        print("Please provide 3 arguments: [nodes] [edges] [file]")
        sys.exit(0)

    nodes     = int(sys.argv[1])
    edges     = int(sys.argv[2])
    file_name = sys.argv[3]

    # print("Generating a graph with {} nodes and {} edges in file {}".format(
    #     nodes,
    #     edges,
    #     file_name
    # ))

    graph = generate_graph(nodes, edges, decorate=True)

    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, "confs")
    path = os.path.join(path, "{}.json".format(file_name))

    # print("Saving graph to file.")
    os.system("touch {}".format(path))
    with open(path, "w") as output_file:
        output_file.write(str(graph.to_json()))
    # print("Graph saved to file.")
