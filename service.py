import sys
import threading
import requests

from networks.network import Network
from networks.network import default_network
from database.db_service import MemoryDB
import os
import json
from pprint import pprint
import subprocess
import signal

from flask import Flask, request

app = Flask(__name__)

def get_port():
    port = 4242
    try:
        port = int(sys.argv[1])
    except Exception as e:
        pass
    return port

def run_server():
    DB = MemoryDB()

    @app.route('/', methods=['GET'])
    def healthy():
        if request.method == 'GET':
            return "healthy"

    @app.route("/v", methods=['POST'])
    def query():
        if request.method == 'POST':
            req = request.get_json()
            outputs = []
            pprint(req)
            for entry in req:
                outputs.append(DB.query(entry["product"], entry["version"]))
            return outputs

    app.run(host='0.0.0.0', port=get_port())

def cli():
    while True:
        sys.stdout.write('>')
        sys.stdout.flush()

        line = sys.stdin.readline()
        if "print" in line:
            for net in network.subnets:
                print(network.inspect_subnet(net))
        if "exit" in line:
            exit(0)
        if "delete" in line:
            network.stop_network()
        if "add node" in line:
            network.add_node(Network.metasploitable, "")
            network.connect_to_subnet(network.nodes[-1], network.subnets[0])
        if "request" in line:
            try:
                r = requests.get("http://127.0.0.1:" + str(get_port()) + "/")
                print(r.text)
            except Exception as e:
                print("Error: request failed.")
                print(e)
        if "query" in line:
            rq = json.loads("""[{
                "product" : "monkey_http_daemon",
                "version" : "0.7.0"
            }, {
                "product" : "qemu",
                "version" : "0.13.0"
            }]""")
            r = requests.post(
                url = "http://127.0.0.1:" + str(get_port()) + "/v",
                json = rq)
            print(r.text)
        if "discovery" in line:
            try:
                subnet_mask = line.split(" ")[1]
            except Exception as e:
                subnet_mask = "172.18.0.0/29"
            out = subprocess.getoutput("nmap -sP " + subnet_mask)

            ips = [line.split(" ")[-1] for line in out.split("\n")[2::3]]
            hosts = []
            for ip in ips:
                default = """{
                    {
                        "Host" : \"""" + ip + """\"
                    }
                }"""
                # Getting host information for ip
                try:
                    subprocess.getoutput("nmap -oX host.xml -O -sV " + ip)
                    subprocess.getoutput("nmap -oX trace.xml --traceroute " + ip)
                    host_json = subprocess.getoutput("./build_topology host.xml trace.xml")
                    if not "Aborted" in host_json:
                        hosts.append(host_json)
                    else:
                        hosts.append(default)
                except Exception as e:
                    hosts.append(default)
            pprint(hosts)


def signal_handler(signal, frame):
    os.system("docker rm -f $(docker ps -a -q)")
    os.system("docker network rm test_subnet")
    print("Docker network and containers removed.")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    network = default_network()

    # Starting a thread that runs the server
    threading.Thread(target=run_server).start()

    # Starting a thread that runs the command line interface
    threading.Thread(target=cli).start()
