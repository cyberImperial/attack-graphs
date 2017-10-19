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
