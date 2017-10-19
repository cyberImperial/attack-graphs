#ifndef HOP_HPP
#define HOP_HPP

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/foreach.hpp>
#include <map>
#include <string>
#include <memory>
#include <iostream>
using namespace boost::property_tree;
using namespace std;

class Hop {
public:
   Hop(int ttl, string ipaddr, double rtt, string host);
   Hop(string hop_scan_file);
   int getTTL();
   void load();
   string getIPaddr();
   double getRTT();
   string getHost();
   string toJSON();
private:
   int ttl;
   string ipaddr;
   double rtt;
   string host;
   string hop_scan_file;
   map<string, string> IPs;
};

#endif
