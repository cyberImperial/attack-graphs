#include "Catch.hpp"
#include "../../../../topology/discovery/parser/Host.hpp"
#include <boost/filesystem.hpp>
using namespace boost::filesystem;

static string project_path() {
  boost::filesystem::path path = boost::filesystem::current_path();
  return path.string() + "/tests/topology/discovery/parser/";
}

TEST_CASE("Can't open missing file", "[load]") {
  try {
    Host host("missing file");
  } catch (const runtime_error& error) {
    REQUIRE(true);
  }
}

TEST_CASE("Correct number of vulenerabilities", "[load]") {
  Host host(project_path() + "sample_scan.xml");
  host.load();

  auto vulenerabilities = host.get_vulnerabilities();
  REQUIRE(vulenerabilities.size() == 2);
}

TEST_CASE("Host loads the correct ports", "[load]") {
  Host host(project_path() + "sample_scan.xml");
  host.load();

  auto vulenerabilities = host.get_vulnerabilities();
  REQUIRE(vulenerabilities.find(Port(3000, "")) != vulenerabilities.end());
  REQUIRE(vulenerabilities.find(Port(902, "")) != vulenerabilities.end());
  REQUIRE(vulenerabilities.find(Port(5000, "")) == vulenerabilities.end());
  REQUIRE(vulenerabilities.find(Port(1000, "")) == vulenerabilities.end());
}

TEST_CASE("Host contain correct information", "[load]") {
  Host host(project_path() + "sample_scan.xml");
  host.load();

  auto vulenerabilities = host.get_vulnerabilities();
  REQUIRE(vulenerabilities.find(Port(3000, ""))->first.getProtocol() == "tcp");
  REQUIRE(vulenerabilities.find(Port(902, ""))->first.getProtocol() == "tcp");
  REQUIRE(vulenerabilities.find(Port(3000, ""))->second == Service("http", "nginx", "1.13.5", "open", "syn-ack"));
  REQUIRE(vulenerabilities.find(Port(902, ""))->second == Service("vmware-auth", "VMware Authentication Daemon", "1.10", "open", "syn-ack"));
}

TEST_CASE("Missing arguments error handling works", "[load]") {
  Host host(project_path() + "sample_scan2.xml");
  host.load();

  auto vulenerabilities = host.get_vulnerabilities();
  REQUIRE(vulenerabilities.find(Port(902, "")) != vulenerabilities.end());
  REQUIRE(vulenerabilities.find(Port(3000, "")) == vulenerabilities.end());

  REQUIRE(vulenerabilities.find(Port(902, ""))->first.getProtocol() == "attributeMissing");
  REQUIRE(vulenerabilities.find(Port(902, ""))->second == Service("attributeMissing", "VMware Authentication Daemon", "1.10", "open", "syn-ack"));
}
