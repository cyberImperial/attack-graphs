import time
import random

import logging
logger = logging.getLogger(__name__)

from service.server import config
from database.database_service import DBClient
from topology.discovery.discovery import discovery_ip
from topology.graph.graph import Node

from threading import Lock

db_client = DBClient(config["database"])

def format_out(struct):
    if isinstance(struct, dict):
        for key in struct:
            struct[key] = format_out(struct[key])
        return struct
    if isinstance(struct, list):
        return [format_out(v) for v in struct]
    if isinstance(struct, bool):
        return str(struct).lower()
    return struct

class Populator():
    def __init__(self, graph, discovery_ip=discovery_ip, db_client=db_client):
        self.graph = graph
        self.threads = 1
        self.discovery_ip = discovery_ip
        self.db_client = db_client
        self.updated = False

    def get_batch(self, graph, shuffle=random.shuffle):
        # Create the batch
        not_scanned = []

        if len(graph.nodes) == 0:
            return not_scanned

        graph.lock.acquire()
        for node in graph.unpopulated:
            not_scanned.append(node.ip)
        graph.lock.release()

        # Seam that does not break tests
        shuffle(not_scanned)

        return not_scanned[:self.threads]

    def get_ips(self, batch):
        results = []
        for task in batch:
            results.append(self.discovery_ip(task))
        return results

    def update_graph(self, graph, results, batch):
        self.updated = False

        # Putting the results on the graph
        graph.lock.acquire()
        for i in range(0, len(batch)):
            ip = batch[i]

            # updating unpopulated
            graph.unpopulated.remove(Node(ip))

            # updating populated
            logger.info("Node {} scanned.".format(ip))
            node = Node(ip)
            node.running = results[i]
            node.running["scanned"] = "true"

            if node not in graph.populated:
                self.updated = True
            graph.populated.add(node)

            #update nodes
            graph.nodes.remove(Node(batch[i]))
            graph.nodes.add(node)
        graph.lock.release()

    def populate_nodes(self):
        graph = self.graph
        batch = self.get_batch(graph)

        logger.info("Processing batch of size: {}.".format(len(batch)))
        results = self.get_ips(batch)

        logger.info("Getting vulnerabilities.")
        results = self.add_vulnerabilities(results)

        logger.info("Updating graph.")
        self.update_graph(graph, results, batch)

    def add_vulnerabilities(self, results):
        for j in results:
            json = j
            if "Host" in json:
                json = json["Host"]
                if "RunningServices" in json:
                    json = json["RunningServices"]
                    for entry in json:
                        name = entry["Service"]["name"]
                        version = entry["Service"]["version"]

                        vulnerabilities = self.db_client.db_request("/vulnerability", name, version)
                        privileges = self.db_client.db_request("/privileges", name, version)

                        if vulnerabilities is not None:
                           entry["Vulnerability"] = format_out(vulnerabilities)
                        if privileges is not None:
                            entry["Privileges"] = format_out(privileges)
        return results

    def populate_loop(self):
        time.sleep(10)
        while True:
            logger.info("Started populating nodes.")
            self.populate_nodes()
            if self.updated:
               logger.info("Graph populated.")
