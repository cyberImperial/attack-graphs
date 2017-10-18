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
           int portid = subtree.get<int>("<xmlattr>.portid");
           string protocol = subtree.get<std::string>("<xmlattr>.protocol");
           Port *port = new Port(portid, protocol);

           //Service
           string name;
           string product;
           string version;
           //Service state
           string state_open;
           string reason;
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
           Service *service = new Service(name, product, version, state_open, reason);
           running_services.insert({shared_ptr<Port>(port), shared_ptr<Service>(service)});
           std::cout << std::endl;
       }
   }
}

void Host::print_vulnerabilities() {
    cout << "--------Ports and services------------" << endl;
    for(unordered_map<shared_ptr<Port>, shared_ptr<Service>>::iterator it = running_services.begin();
       it != running_services.end(); ++it) {
         cout << *it->first.get() << "  " << *it->second.get() << endl;
    }
    cout << "Operating system version: " << os << endl;
}
