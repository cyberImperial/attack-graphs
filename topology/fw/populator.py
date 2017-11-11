import time

from service.discovery import discovery_ip
from threading import Lock

import json
import requests

# TODO: remove duplication
def db_request(line, component, url):
    line = line.split("\n")[0]
    args = len(line.split(" "))
    if args != 3:
        return
    product, version = tuple(line.split(" ")[1:])
    # e.g. qemu 0.13.0
    request = json.loads("[{ \
        \"product\" : \"" + product + "\",\
        \"version\" : \"" + version + "\"\
    }]")

    try:
        full_url = "http://127.0.0.1:" + str(config[component]) + url
        r = requests.post(
            url = full_url,
            json = request)
        print(r.text)
    except Exception as e:
        pass
    print("")


class Populator():
    def __init__(self, graph, discovery_ip=discovery_ip, db_request=db_request):
        self.graph = graph
        self.threads = 1
        self.discovery_ip = discovery_ip
        self.db_request = db_request

    def get_batch(self, graph):
        # Create the batch
        i1 = graph.populated_nodes
        i2 = min(i1 + self.threads, len(graph.nodes))

        graph.lock.acquire()
        batch = []
        for i in range(i1, i2):
            batch.append(graph.nodes[i].ip)
        graph.populated_nodes = i2
        graph.lock.release()

        return i1, i2, batch

    def get_ips(self, batch):
        results = []
        for task in batch:
            results.append(self.discovery_ip(task))
        return results

    def update_graph(self, graph, results, i1, i2):
        # Putting the results on the graph
        graph.lock.acquire()
        idx = 0
        for i in range(i1, i2):
            graph.nodes[i].running = results[idx]
            idx += 1
        graph.lock.release()

    def populate_nodes(self):
        graph = self.graph
        i1, i2, batch = self.get_batch(graph)

        results = get_ips(batch)
        results = add_vulnerabilities(results)
        update_graph(self, graph, results, i1, i2)

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

                        query = "query " + name + " " + version
                        vulnerabilities = self.db_request(query, "database", "/vulnerability")

                        query = "privileges " + name + " " + version
                        privileges = self.db_request(query, "database", "/privileges")

                        if vulnerabilities is not None:
                            entry["Vulnerability"] = vulnerabilities
                        if privileges is not None:
                            entry["Privileges"] = privileges
        return results

    def populate_loop(self):
        time.sleep(10)
        while True:
            self.populate_nodes()
            print("Graph populated:")
            print(self.graph)
