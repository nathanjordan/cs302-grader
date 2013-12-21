#define CATCH_CONFIG_MAIN
#include "../../catch/catch.hpp"

int i = 0;
int j = 1;

TEST_CASE( "lolerskates") {
    REQUIRE( i == j );
}
