import json
import os
import unicodedata

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

    def get_privileges(self, product, version):
        """ Returns a list of (CSV, admin)"""

        def filter_by_field(data, field):
            if not field in data:
                return None
            return data[field]

        def parse_metric_v2(impact):
            impact = filter_by_field(impact, "baseMetricV2")
            if impact is None:
                return None
            if not "userInteractionRequired" in impact:
                return None
            if impact["userInteractionRequired"]:
                return None
            return {
                "all" : impact["obtainAllPrivilege"],
                "user" : impact["obtainUserPrivilege"],
                "other" : impact["obtainOtherPrivilege"]
            }

        vulenerability_list = self.query(product, version)
        levels = []
        for vulnerability in vulenerability_list:
            if "impact" in vulnerability:
                v2_out = parse_metric_v2(vulnerability["impact"])
                if v2_out is not None:
                    levels.append(v2_out)
                else:
                    levels.append({"unknown" : True})
            else:
                levels.append({"unknown" : True})

        return levels
