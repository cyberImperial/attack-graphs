import sys
import threading
import os
import signal

from topology.graph.graph_service import graph_service
from topology.sniffer.sniffing_service import sniffing_service
from database.database_service import database_service

from multiprocessing import Process

def signal_handler(siganl, frames):
    print("Killing the running services.")
    for process in processes:
        print("Killing process {}".format(process.pid))
        os.system("kill -9 {}".format(process.pid))
    sys.exit(0)

def services():
    global processes
    processes = [
        Process(target=database_service),
        Process(target=sniffing_service),
        Process(target=graph_service)
    ]

    for process in processes:
        process.start()

if __name__ == "__main__":
    if os.getuid() != 0:
        print("Must be run as root.")
        exit(1)

    if len(sys.argv) < 2:
        print("Need to specify master or slave.")
        exit(1)

    services()
    signal.signal(signal.SIGINT, signal_handler)

    if sys.argv[1] == "master":
        os.system("python3 dissemination/master.py")

    if sys.argv[1] == "master" or sys.argv[1] == "slave":
        argv = " ".join(sys.argv[2:])
        command = "python3 dissemination/slave.py " + argv
        os.system(command)
