import sys
import zerorpc
import threading
import requests

from network import Network
from network import default_network
import sys

def get_addr():
    port = 4242
    try:
        port = int(sys.argv[1])
    except Exception as e:
        pass
    addr = 'tcp://127.0.0.1:' + str(port)
    return addr

class ServerApi(object):
    def echo(self, text):
        """echo any text"""
        return text

def run_server():
    s = zerorpc.Server(ServerApi())
    addr = get_addr()

    s.bind(addr)
    print('$ Server started running on {}'.format(addr))
    s.run()

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
                c = zerorpc.Client()
                c.connect(get_addr())
                print(c.echo("echo"))
            except Exception as e:
                print("Error: request failed.")
                pass

if __name__ == "__main__":
    network = default_network()

    # Starting a thread that runs the server
    threading.Thread(target=run_server).start()

    # Starting a thread that runs the command line interface
    threading.Thread(target=cli).start()
