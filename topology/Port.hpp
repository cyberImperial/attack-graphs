#ifndef PORT_HPP
#define PORT_HPP

#include <string>
#include <iostream>

using namespace std;

class Port {
public:
  Port(int, string);
  int getPortId() const;
  string getProtocol() const;

  bool operator == (Port const& port) const {
    return portid == port.portid;
  }
private:
  int portid;
  string protocol;
};

inline ostream & operator<<(ostream & stream, Port const & v) {
  stream << "Port: {" << v.getPortId() << ", " << v.getProtocol() << "}" << endl;
  return stream;
}

namespace std {
  template<> struct hash<Port> {
    size_t operator()(Port const& p) const {
      return p.getPortId();
    }
  };
}

#endif
