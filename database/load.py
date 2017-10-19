from __future__ import print_function

import json
from pprint import pprint

file_name = 'nvdcve-1.0-2002.json'

def process_version(raw_data):
    return [entry["version_value"] for entry in raw_data]

def get_impact(json):
    return json["impact"]

def get_id(json):
    return json["cve"]["CVE_data_meta"]["ID"]

def get_description(json):
    for entry in json["cve"]["description"]["description_data"]:
        if entry["lang"] == "en":
            return entry["value"]
    return "No English description."

def exportable_json(id, impact, description):
    return {
        "id" : id,
        "impact" : impact,
        "description" : description
    }

indexed_products = {}
export_list = []

def parse(nvdcve_json):
    export_ctr = 0
    with open(nvdcve_json) as data_file:
        data = json.load(data_file)
        for items in data["CVE_Items"]:
            export = exportable_json(
                get_id(items),
                get_impact(items),
                get_description(items))
            export_list.append(export)

            details = items["cve"]["affects"]
            vendor_data = details["vendor"]["vendor_data"]
            for vendor in vendor_data:
                product_data = vendor["product"]["product_data"]

                for product in product_data:
                    product_name = product["product_name"]
                    product_versions = product["version"]["version_data"]
                    product_versions = process_version(product_versions)

                    for version in product_versions:
                        index = str((product_name, version))
                        if not index in indexed_products:
                             indexed_products[index] = []
                        indexed_products[index].append(export_ctr)

            export_ctr += 1

parse(file_name)
with open('indexed.idx', 'w') as outfile:
    json.dump(indexed_products, outfile)
with open('exports.idx', 'w') as outfile:
    json.dump(export_list, outfile)
