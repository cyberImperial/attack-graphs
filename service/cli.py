from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.server import config

class CLI():
    """
    A command line interface that should use Clients to communicate
    with the servers.

    For the definition of a client, see client.py
    """
    def __init__(self):
        self.functions = {
            "echo" : lambda x: print(x[4:])
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

def cli():
    CLI().start()

if __name__ == "__main__":
    cli()
