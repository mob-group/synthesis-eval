#!/bin/zsh

set -eu

source utils.sh

help() {
	echo "This script runs Makespeare, L2 and Simpl on a specified example."
	echo "It puts the results in each directory"
	echo "Specify tests with --test <name>, or run all with --all"
	echo "Or, specify a file with test names using --test-file <filename>, using space separated test names"
}

if [[ $# -eq 0 ]]; then
	help
	exit 0
fi

typeset -a run_all run_tests test_files
zparseopts -D -E -- -all=run_all -test+:=run_tests -test-file+:=test_files

if [[ $# -ne 0 ]]; then
	help
	exit 0
fi

typeset -a tests
if [[ ${#run_all} -gt 1 ]]; then
	# Get all the tests in examples.
	tests=( $(find -wholename "*examples/*" -type d) )
else
	for arg in ${run_tests[@]}; do
		if [[ $arg != "--test" ]]; then
			tests+=( "$arg" )
		fi
	done
fi

if [[ ${#test_files} -gt 0 ]]; then
	for arg in ${test_files[@]}; do
		if [[ $arg != "--test-file" ]]; then
			file_tests=( $(cat $arg) )
			for file_test in ${file_tests[@]}; do
				tests+=( $file_test )
			done
		fi
	done
fi

echo "Running ${#tests} tests: "
echo ${tests[@]}

# We won't run any tests without a gen.py file.  Go through and make sure that each
# gen.py file exists.
typeset -a tests_to_run
for test in ${tests[@]}; do
	if [[ -f examples/$test/gen.py ]]; then
		tests_to_run+=( $test )
	else
		echo "Skipping test $test because there is no gen.py file"
	fi
done

if [[ ${#tests_to_run} -gt 0 ]]; then
	parallel --line-buffer -j100% "echo 'starting test {}'; ./__run.sh {}; echo 'test {} done'" ::: ${tests_to_run[@]}
else
	help
	exit 0
fi
