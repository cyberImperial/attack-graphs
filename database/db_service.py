import json
import os
import unicodedata
from pprint import pprint

class MemoryDB():
    def __init__(self):
        path = os.path.dirname(__file__)

        indexed_path = os.path.join(path, "indexed.idx")
        exports_path = os.path.join(path, "exports.idx")
        with open(indexed_path, 'r') as index_file:
            self.indexes = json.load(index_file)
        with open(exports_path, 'r') as export_file:
            self.data = json.load(export_file)

    def query(self, product, version):
        index = str((product, version))
        output = []
        for idx in self.indexes[index]:
            output.append(self.data[idx])
        return output
