import json
from pprint import pprint

file_name = 'nvdcve-1.0-2002.json'

def process_version(raw_data):
    return [entry["version_value"] for entry in raw_data]

def parse(nvdcve_json):
    with open(nvdcve_json) as data_file:
        data = json.load(data_file)
        ctr = 0
        for items in data["CVE_Items"]:
            details = items["cve"]["affects"]
            vendor_data = details["vendor"]["vendor_data"]
            for vendor in vendor_data:
                product_data = vendor["product"]["product_data"]

                for product in product_data:
                    product_name = product["product_name"]
                    product_versions = product["version"]["version_data"]
                    product_versions = process_version(product_versions)

                    print(product_name)
                    print(product_versions)
            exit(0)

parse(file_name)
