CXX = g++
CXXFLAGS += -std=c++11 -lboost_system -lboost_filesystem
LOADLIBES += -lstdc++ -I /usr/include/boost
HOST_SOURCES = topology/discovery/parser/Host.cpp
PORT_SOURCES = topology/discovery/parser/Port.cpp
SERVICE_SOURCES = topology/discovery/parser/Service.cpp
OBJECT_FILES = Service.o Port.o Host.o
CATCH_LINK=https://raw.githubusercontent.com/cyberImperial/Catch2/master/single_include/catch2/catch.hpp

all: Main.o $(OBJECT_FILES)
	$(CXX) Main.o $(OBJECT_FILES) $(CXXFLAGS) -o build_topology

test: catch.o $(OBJECT_FILES)
	$(CXX) tests/topology/discovery/parser/HostTest.cpp $(CXXFLAGS) catch.o -o HostTest.o $(OBJECT_FILES) && ./HostTest.o

catch.o:
	wget -O tests/topology/discovery/parser/Catch.hpp $(CATCH_LINK)
	$(CXX) $(CXXFLAGS) -c tests/topology/discovery/parser/Runner.cpp -o catch.o

Main.o: topology/discovery/parser/Main.cpp
	$(CXX) $(CXXFLAGS) -c topology/discovery/parser/Main.cpp -o Main.o

Host.o: topology/discovery/parser/Host.cpp
	 $(CXX) $(CXXFLAGS) -c $(HOST_SOURCES) -o Host.o

Port.o: topology/discovery/parser/Port.cpp
	 $(CXX) $(CXXFLAGS) -c $(PORT_SOURCES) -o Port.o

Service.o: topology/discovery/parser/Service.cpp
	 $(CXX) $(CXXFLAGS) -c $(SERVICE_SOURCES) -o Service.o

clean:
	rm -rf build_topology *.o

.PHONY: clean
