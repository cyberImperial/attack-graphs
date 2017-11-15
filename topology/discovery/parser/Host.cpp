#include "Host.hpp"

Host::Host(string host_scan_file) {
  this->host_scan_file = host_scan_file;
}

string Host::toJSON() {
      ptree out;
      out.put("Host.os", this->os);
      out.put("Host.ip", this->ip);
      ptree running_services_tree;
      for(auto& it : running_services) {
          ptree running_service_tree;
          Port port = it.first;
          Service service = it.second;
          running_service_tree.put("Port.portid", port.getPortId());
          running_service_tree.put("Port.protocol", port.getProtocol());

          running_service_tree.put("Service.name", service.getName());
          running_service_tree.put("Service.product", service.getProduct());
          running_service_tree.put("Service.version", service.getVersion());
          running_service_tree.put("Service.state_open", service.getStateOpen());
          running_service_tree.put("Service.reason", service.getReason());
          running_services_tree.push_back(make_pair("", running_service_tree));
      }
      out.add_child("Host.RunningServices", running_services_tree);
      std::ostringstream oss;
      boost::property_tree::write_json(oss, out);
      return oss.str();
}


void Host::load() {
  // Create empty property tree object
   ptree tree;

   // Parse the XML into the property tree.
   read_xml(host_scan_file, tree);

   // Use the throwing version of get to find the debug filename.
   // If the path cannot be resolved, an exception is thrown.
   os = tree.get<std::string>("nmaprun.host.os.osmatch.<xmlattr>.name");
   ip = tree.get<std::string>("nmaprun.host.address.<xmlattr>.addr");

   BOOST_FOREACH( boost::property_tree::ptree::value_type const& node, tree.get_child("nmaprun.host.ports") )
   {
       boost::property_tree::ptree subtree = node.second;

       if( node.first == "port" )
       {
           // Port
           boost::optional<int> portid = subtree.get_optional<int>("<xmlattr>.portid");
           boost::optional<string> protocol = subtree.get_optional<string>("<xmlattr>.protocol");
           if (portid == boost::optional<int>()) {
             continue;
           }

           Port port(
             portid.get(),
             protocol.get_value_or("attributeMissing")
           );

           //Service
           boost::optional<string> name;
           boost::optional<string> product;
           boost::optional<string> version;
           //Service state
           boost::optional<string> state_open;
           boost::optional<string> reason;
           BOOST_FOREACH( boost::property_tree::ptree::value_type const& v, subtree)
           {
              string label = v.first;
              if(label == "state") {
                 state_open = v.second.get_optional<string>("<xmlattr>.state");
                 reason =  v.second.get_optional<string>("<xmlattr>.reason");
              }
              if(label == "service") {
                 name = v.second.get_optional<string>("<xmlattr>.name");
                 product = v.second.get_optional<string>("<xmlattr>.product");
                 version = v.second.get_optional<string>("<xmlattr>.version");
              }
           }
           Service service(
             name.get_value_or("attributeMissing"),
             product.get_value_or("attributeMissing"),
             version.get_value_or("attributeMissing"),
             state_open.get_value_or("attributeMissing"),
             reason.get_value_or("attributeMissing")
           );
           running_services.insert({port, service});
       }
   }
}

unordered_map<Port, Service> Host::get_vulnerabilities() {
  return running_services;
}

void Host::print_vulnerabilities() {
    cout << "--------Ports and services------------" << endl;
    for (auto it : running_services) {
         cout << it.first << "  " << it.second << endl;
    }
    cout << "Operating system version: " << os << endl;
}
