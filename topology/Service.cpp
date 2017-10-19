#include "Service.hpp"

Service::Service(string name, string product, string version,
                 string state_open, string reason) {
  this->name = name;
  this->product = product;
  this->version = version;
  this->state_open = state_open;
  this->reason = reason;
}
string Service::getName() const {
  return name;
}

string Service::getProduct() const {
  return product;
}

string Service::getVersion() const {
  return version;
}

string Service::getStateOpen() const {
  return state_open;
}

string Service::getReason() const {
  return reason;
}
