from __future__ import absolute_import

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.db_service import MemoryDB
from service.components import DBQuery, DBPrivileges
from service.server import config, Server

def database_server():
    db = MemoryDB()
    server = Server("database", config["database"])

    server.add_component_post("/test", DBQuery(db))
    server.add_component_post("/test2", DBPrivileges(db))

    server.run()

# import threading
#
# threading.Thread(target=database_server).start()
#
# time.sleep(10)
# import json, requests
#
# default_request = json.loads("""[{
#     "product" : "monkey_http_daemon",
#     "version" : "0.7.0"
# }, {
#     "product" : "qemu",
#     "version" : "0.13.0"
# }]""")
# r = requests.post(
#     url = "http://127.0.0.1:" + str(config["database"]) + "/test",
#     json = default_request)
# print(r.text)
# r = requests.post(
#     url = "http://127.0.0.1:" + str(config["database"]) + "/test2",
#     json = default_request)
# print(r.text)
