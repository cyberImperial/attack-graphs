#include "Topology.hpp"
#include "Host.hpp"
#include "Hop.hpp"
#include <fstream>

using namespace std;

/*nmap -oX traceroute_all_subnet.xml -O -sV localhost*/
int main(int argc, char **argv)
{
  if(argc < 1)
  {
    cout << "Invalid number of program arguments: ";
    cout << "Usage ./build_topology <traceroute_file.xml>" << endl;
    exit(EXIT_FAILURE);
  }
  Host host(argv[1]);
  Hop hop(argv[2]);
  host.load();
  hop.load();
  ofstream services, topology;
  services.open("services.json");
  topology.open("topology.json");
  //host.print_vulnerabilities();
  services << host.toJSON() << endl;
  topology << hop.toJSON() << endl;
  services.close();
  topology.close();
  return 0;
}
