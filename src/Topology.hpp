#ifndef TOPOLOGY_HPP
#define TOPOLOGY_HPP

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/foreach.hpp>
#include <string>
#include <exception>
#include <iostream>

using namespace boost::property_tree;
using namespace std;

class Topology {
public:
  Topology(string);
  void load();
private:
  string topology_file;
};

#endif
