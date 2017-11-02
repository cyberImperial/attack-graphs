import time

from service.discovery import discovery_ip
from threading import Lock

class Populator():
    def __init__(self, graph):
        self.graph = graph
        self.threads = 1

    def populate_nodes(self):
        graph = self.graph
        # Create the batch
        i1 = graph.populated_nodes
        i2 = min(i1 + self.threads, len(graph.nodes))

        graph.lock.acquire()
        batch = []
        for i in range(i1, i2):
            batch.append(graph.nodes[i].ip)
        graph.populated_nodes = i2
        graph.lock.release()

        # Getting the process results

        # results_lock = Lock()
        #
        # results = []
        # pool = []
        # for task in batch:
        #     def wrapper(results, lock, task):
        #         time.sleep(random())
        #
        #         ans = discovery_ip(task)
        #
        #         lock.acquire()
        #         results.append(ans)
        #         lock.release()
        #
        #     pool.append(threading.Thread(
        #         target = wrapper,
        #         args = (results, results_lock, task)
        #     ))
        #
        # for thread in pool:
        #     thread.start()
        # for thread in pool:
        #     thread.join()

        results = []
        for task in batch:
            results.append(discovery_ip(task))

        # Puting the results on the graph
        graph.lock.acquire()
        idx = 0
        for i in range(i1, i2):
            graph.nodes[i].running = results[idx]
            idx += 1
        graph.lock.release()

    def populate_loop(self):
        time.sleep(10)
        while True:
            self.populate_nodes()
            print("Graph populated:")
            print(self.graph)
