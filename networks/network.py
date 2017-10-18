from pprint import pprint
import json
import sys

from docker import build_image
from docker import build_network
from docker import inspect_network
from docker import create_container
from docker import connect_to_network
from docker import stop_container
from docker import create_gateway

class Network():
    metasploitable = build_image("metasploitable")
    gateway = build_image("nginx")

    def __init__(self):
        self.nodes = []
        self.subnets = []
        self.connections = []

    def add_subnet(self, subnet_name):
        build_network(subnet_name)
        self.subnets.append(subnet_name)
        return self

    def add_node(self, node, command=""):
        self.nodes.append(create_container(node, command))
        return self

    def add_gateway(self, node, external_port, internal_port, command="nginx -g \"daemon off;\""):
        self.nodes.append(create_gateway(node, external_port, internal_port, command))
        return self

    def connect_to_subnet(self, node, subnet):
        self.connections.append((node, subnet))
        connect_to_network(subnet, node)
        return self

    def inspect_subnet(self, subnet):
        if subnet in self.subnets:
            pprint(inspect_network(subnet))
        else:
            print("Subnet not connected.")
        return self

    def stop_network(self):
        for node in self.nodes:
            stop_container(node)
        return self

    def export(self):
        return json.dumps({
            "nodes" : self.nodes,
            "subnets" : self.subnets,
            "connections" : self.connections
        })

def default_network():
    network = Network()
    return network \
        .add_node(Network.metasploitable) \
        .add_node(Network.metasploitable) \
        .add_gateway(Network.gateway, 3000, 80) \
        .add_subnet("test_subnet") \
        .connect_to_subnet(network.nodes[0], network.subnets[0]) \
        .connect_to_subnet(network.nodes[1], network.subnets[0]) \
        .connect_to_subnet(network.nodes[2], network.subnets[0])
