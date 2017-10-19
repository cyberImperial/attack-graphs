#include "Topology.hpp"
#include "Host.hpp"
#include "Hop.hpp"

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
  host.print_vulnerabilities();
  cout << host.toJSON() << endl;
  cout << hop.toJSON() << endl;
  return 0;
}
