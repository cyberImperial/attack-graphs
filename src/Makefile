CXX = g++
CXXFLAGS += -std=c++11
LOADLIBES += -lstdc++
TOPOLOGY_SOURCES = Topology.cpp
HOP_SOURCES = Hop.cpp
OBJECT_FILES = Hop.o Topology.o Main.o

all: $(OBJECT_FILES)
	 $(CXX) $(OBJECT_FILES) $(CXXFLAGS) -o build_topology

Main.o: Main.cpp
	$(CXX) $(CXXFLAGS) -c Main.cpp -o Main.o

Topology.o: Topology.cpp
	$(CXX) $(CXXFLAGS) -c $(TOPOLOGY_SOURCES) -o Topology.o

Hop.o: $(ENIGMA_SOURCES)
	$(CXX) $(CXXFLAGS) -c $(HOP_SOURCES) -o Hop.o

clean:
	rm -rf build_topology *.o

.PHONY: clean
