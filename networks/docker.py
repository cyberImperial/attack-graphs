import os
import json
import subprocess
from pprint import pprint

def wait(command):
    print("> " + command)
    return str(subprocess.getoutput(command))

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
    out = wait("docker run -d " + build_id + " " + command)
    cid = out.split("\n")[0]
    return cid

def connect_to_network(network_name, container_id):
    wait("docker network connect " + network_name + " " + container_id)

def stop_container(container_id):
    wait("docker stop " + container_id)
    wait("docker rm " + container_id)

def create_gateway(build_id, my_port, docker_port, command):
    bind = str(my_port) + ":" + str(docker_port)
    out = wait("docker run -d -p "
        + bind + " "
        + build_id + " "
        + command)
    cid = out.split("\n")[0]
    return cid
