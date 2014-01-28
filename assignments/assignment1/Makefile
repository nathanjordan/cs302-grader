all: unit_tests_public unit_tests_private diff_test_1 diff_test_2 diff_test_1_reference diff_test_2_reference

unit_tests_public:
	clang++ unit_tests_public.cpp -o unit_tests_public

unit_tests_private:
	clang++ unit_tests_private.cpp -o unit_tests_private

diff_test_1_reference:
	clang++ diff_test_1_reference.cpp -o diff_test_1_reference

diff_test_2_reference:
	clang++ diff_test_2_reference.cpp -o diff_test_2_reference

diff_test_1:
	clang++ diff_test_1.cpp -o diff_test_1

diff_test_2:
	clang++ diff_test_2.cpp -o diff_test_2
