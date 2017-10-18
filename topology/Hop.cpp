#include "Hop.hpp"

Hop::Hop(int ttl, string ipaddr, double rtt, string host) {
  this->ttl = ttl;
  this->ipaddr = ipaddr;
  this->rtt = rtt;
  this->host = host;
}

int Hop::getTTL() {
  return ttl;
}
string Hop::getIPaddr() {
  return ipaddr;
}
double Hop::getRTT() {
  return rtt;
}
string Hop::getHost() {
   return host;
}
