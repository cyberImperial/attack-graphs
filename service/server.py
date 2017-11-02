import threading
from flask import Blueprint, Flask, request

config = {
    'database' : 4242,
    'sniffer' : 30001
}

class Server():
    def __init__(self, name, port):
        self.app = Flask(name)
        self.name = name
        self.port = port
        self.components = []

    def add_component_post(self, route, component):
        self.components.append(component)

        def binder():
            def binded():
                return component.receive_post()
            binded.__name__ = self.name + route.replace("/", "_")

            return binded

        self.app.route(route, methods=['POST'])(binder())

    def add_component_get(self, route, component):
        self.components.append(component)

        def binder():
            def binded():
                return component.receive_get()
            binded.__name__ = self.name + route.replace("/", "_")

            return binded

        self.app.route(route, methods=['GET'])(binder())

    def run(self):
        self.app.run(host='0.0.0.0', port=self.port)
