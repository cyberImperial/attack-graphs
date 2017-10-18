CXX = g++
CXXFLAGS += -std=c++11
LOADLIBES += -lstdc++ -I /usr/include/boost
TOPOLOGY_SOURCES = Topology.cpp
HOP_SOURCES = Hop.cpp
HOST_SOURCES = Host.cpp
OBJECT_FILES = Host.o Hop.o Topology.o Main.o

all: $(OBJECT_FILES)
	 $(CXX) $(OBJECT_FILES) $(CXXFLAGS) -o build_topology

Main.o: Main.cpp
	$(CXX) $(CXXFLAGS) -c Main.cpp -o Main.o

Topology.o: Topology.cpp
	$(CXX) $(CXXFLAGS) -c $(TOPOLOGY_SOURCES) -o Topology.o

Hop.o: Hop.cpp
	$(CXX) $(CXXFLAGS) -c $(HOP_SOURCES) -o Hop.o

Host.o: Host.cpp
		$(CXX) $(CXXFLAGS) -c $(HOST_SOURCES) -o Host.o


clean:
	rm -rf build_topology *.o

.PHONY: clean
