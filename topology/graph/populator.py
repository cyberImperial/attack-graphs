import time
import random

import logging
logger = logging.getLogger(__name__)

from service.server import config
from database.database_service import DBClient
from topology.discovery.discovery import discovery_ip
from topology.graph.graph import Node

from threading import Lock, Thread

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
    if isinstance(struct, str):
        formatted = ""
        for x in struct:
            if x != "\"":
                formatted += x
        return formatted
    return struct

class Populator():
    def __init__(self, graph, discovery_ip=discovery_ip, db_client=db_client, batch_threads=1):
        self.graph = graph
        self.batch_threads = batch_threads
        self.discovery_ip = discovery_ip
        self.db_client = db_client

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

        return not_scanned[:self.batch_threads]

    def get_ips(self, batch):
        if len(batch) == 1:
            return [self.discovery_ip(batch[0])]

        # Even though GIL prevents parallism in Python
        # the C++ module will run in parallel
        results = [None] * len(batch)
        threads = [None] * len(batch)
        for idx in range(len(batch)):
            def process(idx):
                idx = int(idx)
                results[idx] = self.discovery_ip(batch[idx])
            threads[idx] = Thread(target=process, args=(str(idx)))
            threads[idx].start()
        for idx in range(len(batch)):
            threads[idx].join()
        return results

    def update_graph(self, graph, results, batch):
        # Putting the results on the graph
        graph.lock.acquire()
        for i in range(0, len(batch)):
            ip = batch[i]
            if Node(ip) not in graph.unpopulated:
                # It might be that a merge happended since we got the batch
                logger.info("Node {} already populated".format(ip))
                continue

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
            graph.nodes.remove(Node(ip))
            graph.nodes.add(node)
        graph.lock.release()

    def populate_nodes(self):
        graph = self.graph
        batch = self.get_batch(graph)
        if len(batch) == 0:
            return False

        logger.info("Processing batch of size: {}.".format(len(batch)))
        results = self.get_ips(batch)

        logger.info("Getting vulnerabilities.")
        results = self.add_vulnerabilities(results)

        logger.info("Updating graph.")
        self.update_graph(graph, results, batch)
        return True

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
            if not self.populate_nodes():
                # If there are no new nodes avaiable, we don't want to take the lock uselessly
                time.sleep(2)
            else:
                logger.info("Graph populated.")
