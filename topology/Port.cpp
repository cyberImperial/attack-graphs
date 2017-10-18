#include "Port.hpp"


Port::Port(int id, string protocol) {
  this->portid = id;
  this->protocol = protocol;
}

int Port::getPortId() const {
  return portid;
}
string Port::getProtocol() const {
  return protocol;
}
