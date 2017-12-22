import sys
import threading
import os
import signal
import argparse
import random
import subprocess

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from multiprocessing import Process

def signal_handler(siganl, frames):
    logger.warn("Killing the running services.")
    for process in processes:
        logger.warn("Killing process {}".format(process.pid))
        os.system("kill -9 {}".format(process.pid))
    sys.exit(0)

def services(device_name=None, filter_mask=None):
    from topology.graph.graph_service import graph_service
    from topology.sniffer.sniffing_service import sniffing_service
    from database.database_service import database_service
    from inference.inference_service import inference_service

    global processes
    processes = [
        Process(target=database_service),
        Process(target=graph_service),
        Process(target=inference_service),
    ]

    processes.append(Process(target=sniffing_service, args=(device_name, filter_mask)))

    for process in processes:
        process.start()

def bind_simulation(simulation):
    # Overrides the default services with a simulation
    import topology.sniffer.devices as devices
    import topology.discovery.discovery as discovery

    devices.open_connection = lambda device_name: [simulation.connection()]
    discovery.discovery_ip  = lambda ip: simulation.discovery_ip(ip)

def set_ports(node_type):
    import service.server as config_keeper

    port_offset = 30000

    if node_type == "slave":
        config = {
            'inference' : port_offset + random.randint(0, port_offset),
            'database' : port_offset + random.randint(0, port_offset),
            'sniffer' : port_offset + random.randint(0, port_offset),
            'graph' : port_offset + random.randint(0, port_offset)
        }
    elif node_type == "master":
        config = config_keeper.config
    else:
        logger.error("Wrong type specified.")
        os.kill(os.getpid(), signal.SIGINT)

    setattr(config_keeper, 'config', config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", type=str,
        help="The type of node run: 'master' or 'slave'")
    parser.add_argument("-m", "--master", type=str, default=None,
        help="Specify master IP for connecting a slave.")
    parser.add_argument("-p", "--port", type=str, default=None,
        help="Specify port for runnning a slave.")
    parser.add_argument("-i", "--interface", type=str, default=None,
        help="The network interface listened to.")
    parser.add_argument("-s", "--simulation", type=str, default=None,
        help="To run a simulated network from a network configuration file use this flag.")
    parser.add_argument("-f", "--filter", type=str, default=None,
        help="Specify a mask for filtering the packets. (e.g. '10.1.1.1/16' would keep packets starting with '10.1')")

    args = parser.parse_args()

    if os.getuid() != 0:
        logger.error("Must be run as root.")
        exit(1)

    if args.simulation is not None:
        from simulation.simulation import Simulation
        args.interface = "virtual_interface"

        bind_simulation(Simulation(args.simulation))

    set_ports(args.type)
    services(args.interface, args.filter)
    signal.signal(signal.SIGINT, signal_handler)

    if args.type == "master":
        master_proc = subprocess.Popen(['python3', 'dissemination/master.py'], shell=False)
        processes.append(master_proc)

    if args.type == "slave":
        master_ip = args.master
        port      = args.port

        if master_ip is None or port is None:
            logger.error("Not enough arguments provided for slave mode.")
            os.kill(os.getpid(), signal.SIGINT)

        slave_proc = subprocess.Popen(['python3', 'dissemination/slave.py', master_ip, port],  shell=False)
        processes.append(slave_proc)
