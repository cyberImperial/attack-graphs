import sys
import threading
import os

from pprint import pprint
import subprocess
import signal

from database.database_service import database_service
from service.cli import cli

def signal_handler(signal, frame):
    os.system("docker rm -f $(docker ps -a -q)")
    os.system("docker network rm test_subnet")
    print("Docker network and containers removed.")
    sys.exit(0)

if __name__ == "__main__":
    if os.getuid() != 0:
        print("Must be run as root.")
        exit(1)
    signal.signal(signal.SIGINT, signal_handler)

    threading.Thread(target=database_service).start()
    threading.Thread(target=cli).start()
