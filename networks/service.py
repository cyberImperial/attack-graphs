import sys
import threading
import requests

from network import Network
from network import default_network
import sys

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
    @app.route('/', methods=['GET'])
    def healthy():
        if request.method == 'GET':
            return "healthy"

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
            network.stop_network()
            exit(0)
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

if __name__ == "__main__":
    network = None
    # network = default_network()

    # Starting a thread that runs the server
    threading.Thread(target=run_server).start()

    # Starting a thread that runs the command line interface
    threading.Thread(target=cli).start()
