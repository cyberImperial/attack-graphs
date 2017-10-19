#include "../frameworks/Catch.hpp"
#include "../../topology/Host.hpp"
#include <boost/filesystem.hpp>
using namespace boost::filesystem;

static string project_path() {
  boost::filesystem::path path = boost::filesystem::current_path();
  return path.string() + "/tests/topology/";
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

  host.print_vulnerabilities();
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
}
