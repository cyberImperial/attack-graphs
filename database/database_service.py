from __future__ import absolute_import

import logging
logger = logging.getLogger(__name__)

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.memory_db import MemoryDB
from service.server import config
from service.server import Server
from service.components import Component
from service.client import LocalClient

import ast

class DBQuery(Component):
    def __init__(self, db):
        self.db = db

    def process(self, json):
        output = {}
        try:
            output = self.db.query(json["product"], json["version"])
            logger.info("DB found: {} {}".format(json["product"], json["version"]))
        except Exception as e:
            logger.warn("DB miss: {} {}".format(json["product"], json["version"]))
        return output

class DBPrivileges(Component):
    def __init__(self, db):
        self.db = db

    def process(self, json):
        output = {}
        try:
            output = self.db.get_privileges(json["product"], json["version"])
            logger.info("DB found: {} {}".format(json["product"], json["version"]))
        except Exception as e:
            logger.warn("DB miss: {} {}".format(json["product"], json["version"]))
        return output

class DBClient(LocalClient):
    """
    The Database Client is a local client as we will only do
    request from the populator or from the CLI/front-end.
    """
    def db_request(self, resource, product, version):
        product = str(product)
        version = str(version)

        db_json = {
            "product" : product,
            "version" : version
        }

        output = self.post(resource, json=db_json)
        return output

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
