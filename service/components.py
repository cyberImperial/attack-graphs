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
