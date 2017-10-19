#ifndef HOST_HPP
#define HOST_HPP

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/foreach.hpp>
#include <string>
#include <exception>
#include <iostream>
#include <unordered_map>
#include <memory>

#include "Service.hpp"
#include "Port.hpp"

using namespace boost::property_tree;
using namespace std;

class Host {
public:
  Host(string);
  void print_vulnerabilities();
  unordered_map<shared_ptr<Port>, shared_ptr<Service>> get_vulnerabilities();
  void load();
private:
  string host_scan_file;
  unordered_map<shared_ptr<Port>, shared_ptr<Service>> running_services;
  string os;
};

#endif
