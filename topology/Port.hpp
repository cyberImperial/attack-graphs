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
private:
  int portid;
  string protocol;
};

inline ostream & operator<<(ostream & stream, Port const & v) {
  stream << "Port: {" << v.getPortId() << ", " << v.getProtocol() << "}" << endl;
  return stream;
}

#endif
