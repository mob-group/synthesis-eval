#!/bin/zsh

set -eu

source utils.sh
zmodload zsh/mathfunc

help() {
	echo "This script runs Makespeare, L2, sketchadapt and Simpl on a specified example."
	echo "It puts the results in each directory"
	echo "Specify tests with --test <name>, or run all with --all"
	echo "Or, specify a file with test names using --test-file <filename>, using space separated test names"
	echo "Use the --no-help flag to run the synthesizers with reduced input (e.g. empty program sketches in Simpl"
}

if [[ $# -eq 0 ]]; then
	help
	exit 0
fi

typeset -a run_all run_tests test_files no_help
zparseopts -D -E -- -all=run_all -test+:=run_tests -test-file+:=test_files -no-help=no_help

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

# Calculate the number of threads that each test needs, and make sure that the cores
# are not overutilized.  L2 and Simpl both need 1 CPU.  Makespeare needs one for each
# thread.
makespeare_threads=$(get_config_value makespeare_seeds )
total_threads=$(( $makespeare_threads + 1 + 1 ))
# Each job will use $total_threads CPUS.  We want NumberJobs * NumberPerJob = Total,
# so NumberJobs = Total / NumberPerJob.  Then, FractionRunning = 1 / NumberPerJob.
percent=$(( 100.0 / $total_threads ))

typeset -a flags
if [[ ${#no_help} -gt 0 ]]; then
	flags+=(--no-help)
fi

if [[ ${#tests_to_run} -gt 0 ]]; then
	set -x
	parallel --line-buffer -j${percent%.*}% "echo 'starting test {}'; ./__run.sh ${flags[@]} {}; echo 'test {} done'" ::: ${tests_to_run[@]}
else
	help
	exit 0
fi
