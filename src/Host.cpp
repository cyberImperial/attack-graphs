#include "Host.hpp"

Host::Host(string host_scan_file) {
  this->host_scan_file = host_scan_file;
}

static string* tryGet(boost::property_tree::ptree::value_type const& v, string attr){
  try {
    return new string(v.second.get<string>("<xmlattr>." + attr));
  }catch (...){
    return nullptr;
  }
}

void Host::load() {
  // Create empty property tree object
   ptree tree;

   // Parse the XML into the property tree.
   read_xml(host_scan_file, tree);

   // Use the throwing version of get to find the debug filename.
   // If the path cannot be resolved, an exception is thrown.
   os = tree.get<std::string>("nmaprun.host.os.osmatch.<xmlattr>.name");

   BOOST_FOREACH( boost::property_tree::ptree::value_type const& node, tree.get_child("nmaprun.host.ports") )
   {
     boost::property_tree::ptree subtree = node.second;

       if( node.first == "port" )
       {
           // Port
           Port port;
           Service service;
           
           port.portid = tryGet(node, "portid");
           port.protocol = tryGet(node, "protocol");

     BOOST_FOREACH( boost::property_tree::ptree::value_type const& v, subtree)
           {
              string label = v.first;
              if(label == "state") {
                 service.state_open = tryGet(v, "state");
                 service.reason =  tryGet(v, "reason");
              }
              if(label == "service") {
                 service.name = tryGet(v, "name");
                 service.product = tryGet(v, "product");
                 service.version = tryGet(v, "version");
                 service.servicepf = tryGet(v, "servicepf");
                 service.extrainfo = tryGet(v, "extrainfo");
                 service.tunnel = tryGet(v, "tunnel");
                 service.method = tryGet(v, "method");
                 service.conf = tryGet(v, "conf");
              }
           }
           std::cout <<  std::endl;
       }
   }
}


void Host::print_vulnerabilities() {
    cout << "--------Ports and services------------" << endl;
    for(unordered_map<string, string>::iterator it = open_port_assignment.begin();
       it != open_port_assignment.end(); ++it) {
         cout << it->first << "  " << it->second << endl;
       }
    cout << "Operating system version: " << os << endl;
}
