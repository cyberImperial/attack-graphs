from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pprint import pprint
from clint.textui import puts, indent, prompt, colored, progress
import argparse

import threading
from random import random

from service.server import config
from inference.inference_service import InferenceClient
from database.database_service import DBClient
from service.client import LocalClient

def progress_bar(label, size=10):
    with progress.Bar(label=colored.yellow(label), expected_size=size) as bar:
        last_val = 0
        for val in range(size + 1):
            time.sleep(0.1 * (val - last_val))
            bar.show(val)
            last_val = val

class CLI():
    """
    A command line interface that should use Clients to communicate
    with the servers.

    For the definition of a client, see client.py
    """
    def __init__(self):
        self.packet_cache = []
        self.out = None

    def dispatch(self, args):
        def new_packet():
            if len(self.packet_cache) == 0:
                self.packet_cache += LocalClient(config["sniffer"]).get("/newpackets", default=[])
            if len(self.packet_cache) == 0:
                return None
            packet = self.packet_cache[0]
            self.packet_cache = list(self.packet_cache[1:])
            return packet

        dispatch_map = [{
                "input" : args.echo,
                "func" : lambda x: x
            }, {
                "no_args" : args.gen,
                "func" : lambda: InferenceClient(config["inference"]).get_attack_graph(),
                "wait" : "gen: "
            }, {
                "no_args" : args.exit
            }, {
                "input" : args.vul,
                "func" : lambda: DBClient(config["database"]).db_request("/vulnerability", args.vul[0], args.vul[1]),
                "wait" : "vul: "
            }, {
                "input" : args.priv,
                "func" : lambda: DBClient(config["database"]).db_request("/privileges", args.priv[0], args.priv[1]),
                "wait" : "priv: "
            }, {
                "no_args" : args.graph,
                "func" : lambda: LocalClient(config["graph"]).get("/graph"),
                "wait" : "graph: "
            }, {
                "no_args" : args.packet,
                "func" : new_packet
            }
        ]

        out_service = None
        for service in dispatch_map:
            if "no_args" in service and service["no_args"]:
                out_service      = service
                out_service["out"] = lambda: service["func"]()
                break
            if "input" in service and service["input"] is not None:
                out_service        = service
                out_service["out"] = lambda: service["func"]()
                break
        return out_service

    def start(self):
        while True:
            line = prompt.query("> ")

            input_args = line.split(' ')
            keywords = [
                "echo",
                "gen",
                "exit",
                "quit",
                "priv",
                "vul",
                "help",
                "graph",
                "packet"
            ]
            for i in range(len(input_args)):
                if input_args[i] in keywords:
                    input_args[i] = "--" + input_args[i]

            parser = argparse.ArgumentParser()
            group  = parser.add_mutually_exclusive_group()
            group.add_argument("--echo", type=str, nargs='+',
                help="Usual echo command.")
            group.add_argument("--exit", action="store_true",
                help="Exit.")
            group.add_argument("--quit", dest="exit", action="store_true",
                help="Exit.")
            group.add_argument("--gen", action="store_true",
                help="Send a request to the inference engine.")
            group.add_argument("--vul", type=str, nargs=2,
                help="""
                    Send a request to the database service for a vulnerability.
                    The first argument is the product.
                    The second argument is the version.
                """)
            group.add_argument("--priv", type=str, nargs=2,
                help="""
                    Send a request to the database service for privilege level
                        escalation for a vulnerability.
                    The first argument is the product.
                    The second argument is the version.
                """)
            group.add_argument("--graph", action="store_true",
                help="Send a request to the local graph service.")
            group.add_argument("--packet", action="store_true",
                help="Send a request to the local sniffer service.")

            group.set_defaults(
                exit = False,
                gen = False,
                graph = False,
                packet = False
            )

            exit = False
            args = None
            try:
                args = parser.parse_args(input_args)
            except SystemExit:
                puts(colored.yellow('WARN: {}'.format("Wrong arguments provided.")))
                parser.print_help()
                exit = True

            if not exit:
                if args.exit:
                    puts("Bye..")
                    sys.exit(0)

                out_service = self.dispatch(args)
                if out_service is None:
                    puts(colored.red('ERROR: {}'.format("No service matched.")))

                self.out = None

                def store_output():
                    self.out = out_service["out"]()

                task = threading.Thread(target=store_output)
                task.start()
                if "wait" in out_service:
                    progress_bar(out_service["wait"], 20)
                task.join()

                if self.out is None:
                    puts(colored.red('ERROR: {}'.format("The query encountered an error.")))
                else:
                    puts(colored.green('SUCCESS'))
                    print(self.out)

def cli():
    CLI().start()

if __name__ == "__main__":
    cli()
