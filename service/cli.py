from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from networks.network import Network
from networks.network import default_network
import operator

class CLI():
    def __init__(self):
        def init_network():
            self.network = default_network()

        self.functions = {
            "echo" : lambda x: print(x[4:]),
            "start" : lambda x: init_network(),
            "stop" : lambda x: self.network.stop_network()
        }

    def dispatch(self, line):
        for function in self.functions:
            if function in line:
                self.functions[function](line)

    def start(self):
        while True:
            sys.stdout.write('>')
            sys.stdout.write(' ')
            sys.stdout.flush()

            line = sys.stdin.readline()
            self.dispatch(line)

if __name__ == "__main__":
    CLI().start()
