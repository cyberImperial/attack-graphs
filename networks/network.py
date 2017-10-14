import os
import json
import subprocess
from pprint import pprint

def wait(command):
    print("> " + command)
    return subprocess.check_output(command, shell=True)

def build_image(component):
    out = wait("docker build components/" + component)
    iid = out.split(" ")[-1].split("\n")[0]
    return iid

def build_network(network):
    try:
        cid = wait("docker network create " + network).split("\n")
    except:
        print("Error occured during building network.")

def inspect_network(network):
    out = wait("docker network inspect " + network)
    return json.loads(out)

def create_container(build_id, command):
    out = wait("docker run -d " + str(build_id) + " " + command)
    cid = out.split("\n")[0]
    return cid

def connect_to_network(network_name, container_id):
    wait("docker network connect " + network_name + " " + container_id)

def stop_container(container_id):
    wait("docker stop " + container_id)
    wait("docker rm " + container_id)

network = "test_network"
print("Building containter...")
iid = build_image("metasploitable")

build_network(network)
pprint(inspect_network(network))

c1 = create_container(iid, "")
c2 = create_container(iid, "")
print(c1)
print(c2)

connect_to_network(network, c1)
pprint(inspect_network(network))
connect_to_network(network, c2)
pprint(inspect_network(network))

stop_container(c1)
stop_container(c2)
