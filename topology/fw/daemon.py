from __future__ import absolute_import

import os, sys, time
from threading import Lock
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import requests
from topology.fw.sniffer import parse_packet
from service.components import Component
from service.server import Server, config

def do_post():
    full_url = "http://127.0.0.1:30001/newpackets"
    try:
        print("here")
        r = requests.get(full_url)
        print(r.text)
    except Exception as e:
        pass

def test_req():
    while True:
        do_post()
        time.sleep(2)

class Sniffer():
    def run():
        while True:
            pass

class SniffingDaemon(Component):
    def __init__(self, shared_packets, lock):
        self.shared_packets = shared_packets
        self.lock = lock

    def process(self, unused):
        print("arrived")
        self.lock.acquire()

        packets = self.shared_packets
        self.shared_packets = []

        self.lock.release()
        return packets

def run_server():
    server = Server("sniffer", 30001)
    print(server.add_component_post)
    print(server.add_component_get)

    server.add_component_get("/newpackets", SniffingDaemon(["dani mocanu"], Lock()))

    threading.Thread(target=server.run).start()
    threading.Thread(target=test_req).start()

if __name__ == "__main__":
    run_server()
