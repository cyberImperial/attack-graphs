CXX = g++
CXXFLAGS += -std=c++11 -lboost_system -lboost_filesystem
LOADLIBES += -lstdc++ -I /usr/include/boost
HOP_SOURCES = topology/Hop.cpp
HOST_SOURCES = topology/Host.cpp
PORT_SOURCES = topology/Port.cpp
SERVICE_SOURCES = topology/Service.cpp
OBJECT_FILES = Service.o Port.o Host.o Hop.o Topology.o

all: Main.o $(OBJECT_FILES)
	$(CXX) Main.o $(OBJECT_FILES) $(CXXFLAGS) -o build_topology

test: catch.o $(OBJECT_FILES)
	$(CXX) tests/topology/HostTest.cpp $(CXXFLAGS) catch.o -o HostTest.o $(OBJECT_FILES) && ./HostTest.o

catch.o:
	$(CXX) $(CXXFLAGS) -c tests/frameworks/Runner.cpp -o catch.o

Main.o: topology/Main.cpp
	 $(CXX) $(CXXFLAGS) -c topology/Main.cpp -o Main.o

Hop.o: topology/Hop.cpp
	 $(CXX) $(CXXFLAGS) -c $(HOP_SOURCES) -o Hop.o

Host.o: topology/Host.cpp
	 $(CXX) $(CXXFLAGS) -c $(HOST_SOURCES) -o Host.o

Port.o: topology/Port.cpp
	 $(CXX) $(CXXFLAGS) -c $(PORT_SOURCES) -o Port.o

Service.o: topology/Service.cpp
	 $(CXX) $(CXXFLAGS) -c $(SERVICE_SOURCES) -o Service.o

clean:
	rm -rf build_topology *.o

.PHONY: clean
