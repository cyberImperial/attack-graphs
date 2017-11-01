from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_service import MemoryDB
from service.components import DBQuery, DBPrivileges
from service.server import config, Server

def database_server():
    db = MemoryDB()
    server = Server("database", config["database"])

    server.add_component_post("/vulnerability", DBQuery(db))
    server.add_component_post("/privileges", DBPrivileges(db))

    server.run()
