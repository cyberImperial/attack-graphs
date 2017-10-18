#include "../frameworks/Catch.hpp"
#include "../../topology/Host.hpp"

TEST_CASE("Vulnerabilities get loaded", "[load]") {
  Host host("traceroute_all_subnet.xml");
  host.load();

  REQUIRE(1);
}

unsigned int Factorial( unsigned int number ) {
    return number <= 1 ? number : Factorial(number-1)*number;
}

TEST_CASE( "Factorials are computed", "[factorial]" ) {
    REQUIRE( Factorial(1) == 1 );
    REQUIRE( Factorial(2) == 2 );
    REQUIRE( Factorial(3) == 6 );
    REQUIRE( Factorial(10) == 3628800 );
}
