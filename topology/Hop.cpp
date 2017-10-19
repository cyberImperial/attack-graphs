#include "Hop.hpp"

Hop::Hop(int ttl, string ipaddr, double rtt, string host) {
  this->ttl = ttl;
  this->ipaddr = ipaddr;
  this->rtt = rtt;
  this->host = host;
}
Hop::Hop(string hop_scan_file) {
  this-> hop_scan_file = hop_scan_file;
}

string Hop::toJSON() {

      ptree out;
      ptree IPs_tree;

      for(auto& it : IPs) {
        ptree IP_tree;
        string IP = it.first;
        string hostname = it.second;
        IP_tree.put("IP", IP);
        IP_tree.put("Hostname", hostname);

        IPs_tree.push_back(make_pair("", IP_tree));
      }

      out.add_child("IPs", IPs_tree);
      ostringstream oss;
      boost::property_tree::write_json(oss, out);
      return oss.str();
}

void Hop::load() {
  // Create empty property tree object
   ptree tree;

   // Parse the XML into the property tree.
   read_xml(hop_scan_file, tree);

   BOOST_FOREACH( boost::property_tree::ptree::value_type const& node, tree.get_child("nmaprun.host.trace") )
   {
     if (node.first == "hop") {
       boost::property_tree::ptree subtree = node.second;
       boost::optional<string> ip = subtree.get_optional<string>("<xmlattr>.ipaddr");
       boost::optional<string> hostname = subtree.get_optional<string>("<xmlattr>.host");
       IPs.insert({ip.get_value_or("IPMissing"), hostname.get_value_or("HostMissing")});
     }
   }
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
