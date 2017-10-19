#ifndef SERVICE_HPP
#define SERVICE_HPP

#include <string>
#include <iostream>

using namespace std;

class Service {
public:
  Service(string, string, string, string, string);
  string getName() const;
  string getProduct() const;
  string getVersion() const;
  string getStateOpen() const;
  string getReason() const;

  bool operator == (Service const& service) const {
    return name == service.name
        && product == service.product
        && version == service.version
        && state_open == service.state_open
        && reason == service.reason;
  }
private:
  string name;
  string product;
  string version;
  //Service state
  string state_open;
  string reason;
};

inline ostream & operator<<(ostream & stream, Service const & v) {
  stream << "Service: {" << v.getName() << ", " << v.getProduct() << ", " << v.getVersion() << "}" << endl;
  return stream;
}

#endif
