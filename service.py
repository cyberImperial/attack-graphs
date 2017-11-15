import sys
import threading
import os

from topology.graph.graph_service import graph_service
from topology.sniffer.sniffing_service import sniffing_service
from database.database_service import database_service

if __name__ == "__main__":
    if os.getuid() != 0:
        print("Must be run as root.")
        exit(1)

    threading.Thread(target=database_service).start()
    threading.Thread(target=sniffing_service).start()
    threading.Thread(target=graph_service).start()
