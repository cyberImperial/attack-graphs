import json
import os
import unicodedata
from pprint import pprint

class MemoryDB():
    def __init__(self):
        with open('database/indexed.idx', 'r') as index_file:
            self.indexes = json.load(index_file)
        with open('database/exports.idx', 'r') as export_file:
            self.data = json.load(export_file)

    def query(self, product, version):
        index = str((product, version))
        output = []
        for idx in self.indexes[index]:
            output.append(self.data[idx])
        return output

DB = MemoryDB()
print(DB.query("monkey_http_daemon", "0.7.0"))
