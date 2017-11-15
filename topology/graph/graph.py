from threading import Lock

class Node():
    def __init__(self, ip):
        self.ip = ip
        self.running = {}

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.ip == other.ip
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)

    def __str__(self):
        if self.running == {}:
            return str(self.ip)
        return str((self.ip, self.running))

class Graph():
    def __init__(self):
        self.edges = []
        self.nodes = []
        self.lock = Lock()

        # The index of the first node not populated yet
        self.populated_nodes = 0

    def add_edge(self, n1, n2):

        firstInside = False
        secondInside = False

        for n in self.nodes:
            if n == n1:
                firstInside = True
            if n == n2:
                secondInside = True

        if not firstInside:
            self.nodes.append(n1)

        if not secondInside:
            self.nodes.append(n2)

        for p1, p2 in self.edges:
            if p1 == n1 and p2 == n2:
                return
        self.edges.append((n1, n2))

    def merge(self, graph):
        pass

    def to_json(self):
        return {
            "hosts" : [{
                "ip" : node.ip,
                "running" : node.running
            } for node in self.nodes],
            "links" : [{
                "source" : n1.ip,
                "target" : n2.ip,
                "value"  : 1,
            } for n1, n2 in self.edges]
        }

    @staticmethod
    def from_json():
        return Graph()

    def __str__(self):
         return str([(str(n1), str(n2)) for (n1, n2) in self.edges])
