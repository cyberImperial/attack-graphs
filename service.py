import sys
import threading
import os

from topology.graph.graph_service import graph_service
from topology.sniffer.sniffing_service import sniffing_service
from database.database_service import database_service

from multiprocessing import Process

def services():
    Process(target=database_service).start()
    Process(target=sniffing_service).start()
    Process(target=graph_service).start()

if __name__ == "__main__":
    if os.getuid() != 0:
        print("Must be run as root.")
        exit(1)

    services()
    if sys.argv[1] == "master":
        os.system("python3 dissemination/master.py")

    if sys.argv[1] == "master" or sys.argv[1] == "slave":
        argv = " ".join(sys.argv[2:])
        command = "python3 dissemination/slave.py " + argv
        os.system(command)
