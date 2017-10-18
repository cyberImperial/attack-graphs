#ifndef HOP_HPP
#define HOP_HPP

#include <string>
#include <memory>

using namespace std;

class Hop {
public:
   Hop(int ttl, string ipaddr, double rtt, string host);
   int getTTL();
   string getIPaddr();
   double getRTT();
   string getHost();
private:
   int ttl;
   string ipaddr;
   double rtt;
   string host;
};

#endif
