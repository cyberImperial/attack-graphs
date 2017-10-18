#include "Host.hpp"

Host::Host(string host_scan_file) {
  this->host_scan_file = host_scan_file;
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
           string portid = subtree.get<std::string>("<xmlattr>.portid");
           string protocol = subtree.get<std::string>("<xmlattr>.protocol");
           
           cout << portid << " " << protocol << endl;

           //State
           string state_open;
           string reason;

           //Service
           string name;
           string product;
           string version;
           BOOST_FOREACH( boost::property_tree::ptree::value_type const& v, subtree)
           {
              std::string label = v.first;
              if(label == "state") {
                 state_open = v.second.get<string>("<xmlattr>.state");
                 reason =  v.second.get<string>("<xmlattr>.reason");
              }
              if(label == "service") {
                 name = v.second.get<string>("<xmlattr>.name");
                 product = v.second.get<string>("<xmlattr>.product");
                 version = v.second.get<string>("<xmlattr>.version");
              }
           }
           std::cout << std::endl;
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
