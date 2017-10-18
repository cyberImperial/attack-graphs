CXX = g++
CXXFLAGS += -std=c++11
LOADLIBES += -lstdc++ -I /usr/include/boost
TOPOLOGY_SOURCES = Topology.cpp
HOP_SOURCES = Hop.cpp
HOST_SOURCES = Host.cpp
PORT_SOURCES = Port.cpp
SERVICE_SOURCES = Service.cpp
OBJECT_FILES = Service.o Port.o Host.o Hop.o Topology.o Main.o

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

Port.o: Port.cpp
	 $(CXX) $(CXXFLAGS) -c $(PORT_SOURCES) -o Port.o

Service.o: Service.cpp
	 $(CXX) $(CXXFLAGS) -c $(SERVICE_SOURCES) -o Service.o


clean:
	rm -rf build_topology *.o

.PHONY: clean
