from __future__ import absolute_import

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_service import MemoryDB
from service.components import DBQuery

import threading
from flask import Blueprint, Flask, request

def get_port():
    port = 4242
    try:
        port = int(sys.argv[1])
    except Exception as e:
        pass
    return port

class Server():
    def __init__(self, name):
        self.app = Flask(name)
        self.name = name
        self.components = []

    def add_component_post(self, route, component):
        self.components.append(component)
        self.app.route(route, methods=['POST'])(component.receive_post)

    def run(self):
        self.app.run(host='0.0.0.0', port=get_port())

DB = MemoryDB()
server = Server("server")
component = DBQuery(DB)
server.add_component_post("/test", component)
threading.Thread(target=server.run).start()

import json, requests

default_request = json.loads("""[{
    "product" : "monkey_http_daemon",
    "version" : "0.7.0"
}, {
    "product" : "qemu",
    "version" : "0.13.0"
}]""")
r = requests.post(
    url = "http://127.0.0.1:" + str(get_port()) + "/test",
    json = default_request)
print(r.text)
