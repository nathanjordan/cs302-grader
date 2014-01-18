#define CATCH_CONFIG_MAIN
#include "../../catch/catch.hpp"
#include "reference.hpp"
#include <stack>


///////////////////////////////////////////////////////////////////////////////
//
//  Test Cases for Assignment 1
//
///////////////////////////////////////////////////////////////////////////////
TEST_CASE("CS302 Assignment 1") {

    ///////////////////////////////////////////////////////////////////////////
    //  Test 1
    ///////////////////////////////////////////////////////////////////////////
    SECTION("Test 1") {

        // Reference Stack Operations
        std::stack<int> standard_stack;

        standard_stack.push(1);
        standard_stack.push(2);

        int reference = standard_stack.top();

        // Student Stack Case
        stack<int> user_stack;

        user_stack.push(1);
        user_stack.push(2);

        int student = user_stack.pop();

        // Reference vs. Actual
        REQUIRE( reference == student );

    }

    ///////////////////////////////////////////////////////////////////////////
    //  Test 2
    ///////////////////////////////////////////////////////////////////////////
    SECTION("Test 2") {

        // Reference Stack Operations
        std::stack<int> standard_stack;

        standard_stack.push(1);
        standard_stack.push(1);

        int reference = standard_stack.top();

        // Student Stack Case
        stack<int> user_stack;

        user_stack.push(1);
        user_stack.push(2);

        int student = user_stack.pop();

        // Reference vs. Actual
        REQUIRE( reference == student );

    }
}
