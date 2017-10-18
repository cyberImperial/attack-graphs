#ifndef HOST_HPP
#define HOST_HPP

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/foreach.hpp>
#include <string>
#include <exception>
#include <iostream>
#include <unordered_map>

using namespace boost::property_tree;
using namespace std;

class Host {
public:
   Host(string);
   void print_vulnerabilities();
   void load();
private:
   string host_scan_file;
   // shared_ptr<Port>, shared_ptr<Service>
   unordered_map<string, string> open_port_assignment;
   string os;
};

#endif
