#include "Topology.hpp"

using namespace std;

int main(int argc, char **argv)
{
  if(argc < 1)
   {
     cout << "Invalid number of program arguments: ";
     cout << "Usage ./build_topology <traceroute_file.xml>" << endl;
     exit(EXIT_FAILURE);
    }
    Topology topology(argv[1]);
    topology.load();
    return 0;
}
