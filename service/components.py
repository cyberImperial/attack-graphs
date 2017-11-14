import abc
from flask import request

class Component():
    __metaclass__ = abc.ABCMeta
    """
    A component class that receives JSON requests and returns stringyfied jsons.

    To implement a new component, extend this class.
    """

    @abc.abstractmethod
    def process(self, json):
        pass

    def receive_post(self):
        if request.method == "POST":
            req = request.get_json()
            output = self.process(req)
            return str(output)

    def receive_get(self):
        if request.method == "GET":
            output = self.process("")
            return str(output)

class DBQuery(Component):
    def __init__(self, db):
        self.db = db

    def process(self, json):
        return [self.db.query(entry["product"], entry["version"]) for entry in json]


class DBPrivileges(Component):
    def __init__(self, db):
        self.db = db

    def process(self, json):
        outputs = {}
        for entry in json:
            key = str((entry["product"], entry["version"]))
            outputs[key] = self.db.get_privileges(entry["product"], entry["version"])
        return outputs
