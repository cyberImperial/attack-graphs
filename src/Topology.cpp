#include "Topology.hpp"

Topology::Topology(string topology_file) {
  this->topology_file = topology_file;
}

void Topology::load() {
   // Create empty property tree object
    //ptree tree;

    // Parse the XML into the property tree.
    //read_xml(topology_file, tree);

    // Use the throwing version of get to find the debug filename.
    // If the path cannot be resolved, an exception is thrown.
  //  m_file = tree.get<std::string>(".....FIND XML DOM PATH..");

    // Use the default-value version of get to find the debug level.
    // Note that the default value is used to deduce the target type.
//    m_level = tree.get("debug.level", 0);

    // Use get_child to find the node containing the modules, and iterate over
    // its children. If the path cannot be resolved, get_child throws.
    // A C++11 for-range loop would also work.
  //  BOOST_FOREACH(pt::ptree::value_type &v, tree.get_child("debug.modules")) {
        // The data function is used to access the data stored in a node.
  //      m_modules.insert(v.second.data());
  
}
