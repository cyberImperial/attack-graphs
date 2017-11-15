from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.memory_db import MemoryDB
from service.server import config
from service.server import Server
from service.components import Component
from service.client import LocalClient

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

class DBClient(LocalClient):
    """
    The Database Client is a local client as we will only do
    request from the populator or from the CLI/front-end.
    """
    def db_request(self, resource, product, version):
        db_json = json.loads("[{ \
            \"product\" : \"" + product + "\",\
            \"version\" : \"" + version + "\"\
        }]")
        return self.post(resource, resource, db_json)

class DatabaseService():
    """
    The DatabaseService encapsulates all the dependecies of the
    database service:
      * the memorydb
      * the server
    """
    def __init__(self):
        self.server = Server("database", config["database"])
        self.database = MemoryDB()

        self.server.add_component_post("/vulnerability", DBQuery(self.database))
        self.server.add_component_post("/privileges", DBPrivileges(self.database))

def database_service():
    service = DatabaseService()
    service.server.run()

if __name__ == "__main__":
    database_service()
