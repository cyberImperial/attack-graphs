from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clint.textui import puts, indent, prompt
import argparse

from service.server import config

from inference.inference_service import InferenceClient

class CLI():
    """
    A command line interface that should use Clients to communicate
    with the servers.

    For the definition of a client, see client.py
    """
    def dispatch(self, args):
        dispatch_map = [{
                "input" : args.echo,
                "func" : lambda x: x
            }, {
                "no_args" : args.gen,
                "func" : lambda: InferenceClient(config["inference"]).get_attack_graph(),
                "wait" : True
            }, {
                "no_args" : args.exit
            }
        ]

        out_service = None
        for service in dispatch_map:
            if "no_arg" in service and service["no_arg"]:
                out_service      = service
                out_service[out] = service["func"]()
            if "input" in service and service["input"] is not None:
                out_service        = service
                out_service["out"] = service["func"](service["input"])
        return out_service

    def start(self):
        while True:
            line = prompt.query("> ")

            input_args = line.split(' ')
            keywords = ["echo", "gen", "exit", "quit"]
            for i in range(len(input_args)):
                if input_args[i] in keywords:
                    input_args[i] = "--" + input_args[i]

            parser = argparse.ArgumentParser()
            group  = parser.add_mutually_exclusive_group()
            group.add_argument("--echo", type=str, nargs='+',
                help="Usual echo command.")
            group.add_argument("--gen", action="store_true",
                help="Send a request to the inference engine.")
            group.add_argument("--exit", action="store_true",
                help="Send a request to the inference engine.")
            group.add_argument("--quit", dest="exit", action="store_true",
                help="Send a request to the inference engine.")
            group.set_defaults(
                exit = False,
                gen = False
            )

            exit = False
            try:
                args = parser.parse_args(input_args)
            except SystemExit:
                parser.print_help()
                exit = True

            if args.exit:
                puts("Bye..")
                sys.exit(0)

            if not exit:
                out_service = self.dispatch(args)
                print(out_service)

def cli():
    CLI().start()

if __name__ == "__main__":
    cli()
