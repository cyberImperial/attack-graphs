import json
import requests
import ast

class Client():
    """
    A wrapper for RESTful requests made to a server.
    """

    def __init__(self, url, port):
        self.url = url
        self.port = port

    def get(self, resource, default=None):
        full_url = self.url + ":" + str(self.port) + resource
        try:
            r = requests.get(url = full_url)
            data = json.dumps(ast.literal_eval(r.text))
            return json.loads(data)
        except Exception as e:
            return default

    def post(self, resource, json, default=None):
        full_url = self.url + ":" + str(self.port) + resource
        try:
            r = requests.post(
                url = full_url,
                json = json)
            data = json.dumps(ast.literal_eval(r.text))
            return json.loads(data)
        except Exception as e:
            return default

class LocalClient(Client):
    def __init__(self, port):
        self.url = "http://127.0.0.1"
        self.port = port
