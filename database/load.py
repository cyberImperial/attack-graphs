from __future__ import print_function

import json
import os
import sys
import subprocess

import logging
logger = logging.getLogger(__name__)

DIRECTORY = os.path.abspath(os.path.dirname(__file__))

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
export_ctr = 0

def parse(nvdcve_json):
    global export_ctr
    global DIRECTORY

    with open(os.path.join(DIRECTORY, nvdcve_json)) as data_file:
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

def call(command):
    return subprocess.check_output(command, shell=True)

if __name__=="__main__":
    if "-r" in sys.argv:
        # Remove old index files
        log.warn("Removing old index files...")
        for f in os.listdir(DIRECTORY):
            if ".idx" in f:
                log.warn("Removing " + f)
                os.remove(f)

    # Check all files exist:
    need_download = False
    for r in range(2002, 2018):
        file_name = "nvdcve-1.0-{}.json".format(r)
        if not os.path.exists(os.path.join(DIRECTORY, file_name)):
            need_download = True

    if need_download:
        logger.info("Downloading NVD JSON files...")
        if "-d" in sys.argv:
            os.system(os.path.join(DIRECTORY, "dw_nvd_json.sh", "database"))
        else:
            os.system(os.path.join(DIRECTORY, "dw_nvd_json.sh"))

    # Create new index files
    logger.info("Indexing NVD files...")
    for r in range(2002, 2018):
        file_name = "nvdcve-1.0-{}.json".format(r)
        logger.info("Parsing file:" + file_name)
        parse(file_name)

    with open(os.path.join(DIRECTORY, 'indexed.idx'), 'w') as outfile:
        json.dump(indexed_products, outfile)
    with open(os.path.join(DIRECTORY, 'exports.idx'), 'w') as outfile:
        json.dump(export_list, outfile)
