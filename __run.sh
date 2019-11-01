#!/bin/zsh

set -eu

typeset -a check
zparseopts -D -E -- -check=check
if [[ $# -ne 1 ]]; then
	echo "Usage: $0 <test name>"
	echo "Optional: --check (only run for 5 seconds to make sure input formats are OK)"
	echo "SHOULD NOT BE USED DIRECTLY: Use run-all.sh instead!"
fi
source utils.sh

test=$1

# Run the gen file.
if [[ ! -f examples/$test/gen.py ]]; then
	echo "Expected a gen.py file to exist for test $test"
	exit 1
fi

pushd examples/$test
python3 gen.py
popd

if [[ ${#check} -eq 0 ]]; then
	makespeare_timeout=$(get_config_value makespeare_timeout)
	l2_timeout=$(get_config_value l2_timeout)
	simpl_timeout=$(get_config_value simpl_timeout)
else
	makespeare_timeout=5
	l2_timeout=5
	simpl_timeout=5
fi

makespeare_out=examples/$test/makespeare_out
l2_out=examples/$test/L2_out
simpl_out=examples/$test/simpl_out

tmp_makespeare_file=$(mktemp /tmp/syntheval.XXXXXX)
tmp_l2_file=$(mktemp /tmp/syntheval.XXXXXX)
tmp_simpl_timeout_file=$(mktemp /tmp/syntheval.XXXXXX)

start_time=$( date '+%s')
( timeout -s TERM $makespeare_timeout ./run-makespeare.sh $test &> $makespeare_out || true; echo $(date '+%s') > $tmp_makespeare_file) &
(timeout -s TERM $l2_timeout ./run-L2.sh $test &> $l2_out || true; echo $( date '+%s') > $tmp_l2_file ) &
(timeout -s TERM $simpl_timeout ./run-simpl.sh $test &> $simpl_out || true; echo $( date '+%s') > $tmp_simpl_timeout_file) &

wait

makespeare_end=$(cat $tmp_makespeare_file)
l2_end=$(cat $tmp_l2_file)
simpl_end=$(cat $tmp_simpl_timeout_file)

# rm $tmp_makespeare_file $tmp_l2_file $tmp_simpl_timeout_file

# Go through and attempt to determine whether the synthesis program succeeded.  Note
# that for Makespeare, we cannot be sure that it succeeded when it claims success,
# because it can also claim that on programs where it doesn't get the right one.

check_l2() {
	local output_file=$1
	local results_file=$2
	local timed_out=$3

	count=$(grep -e 'Found solution:' $output_file -c || true)
	if [[ $count -ne 0 ]]; then
		echo "L2: success" >> $results_file
	elif [[ $timed_out == 1 ]]; then
		echo "L2: timeout" >> $results_file
	else
		echo "L2: failed" >> $results_file
	fi
}

check_makespeare() {
	local output_file=$1
	local results_file=$2
	local timed_out=$3

	count=$(grep -e 'Fully correct on training set' $output_file -c || true)

	if [[ $count -ne 0 ]]; then
		echo "makespeare: success" >> $results_file
	elif [[ $timed_out == 1 ]]; then
		echo "makespeare: timeout" >> $results_file
	else
		echo "makespeare: failed" >> $results_file
	fi
}

check_simpl() {
	local output_file=$1
	local results_file=$2
	local timed_out=$3

	count=$(grep -e ' COMPLETE PROGRAM' $output_file -c || true)

	if [[ $count -ne 0 ]]; then
		echo "simpl: success" >> $results_file
	elif [[ $timed_out == 1 ]]; then
		echo "simpl: timeout" >> $results_file
	else
		echo "simpl: failed" >> $results_file
	fi
}

timeout_check() {
	# Print whether the window of time exceeds the timeout
	# time.
	local start_time=$1
	local end_time=$2
	local timeout_time=$3

	if (( $end_time - $start_time > $timeout_time )); then
		# timeout
		echo 1
	else
		echo 0
	fi
}

results_file=examples/$test/results
echo "" -n > $results_file
check_l2 $l2_out $results_file $(timeout_check $start_time $l2_end $l2_timeout)
check_makespeare $makespeare_out $results_file $(timeout_check $start_time $makespeare_end $makespeare_timeout)
check_simpl $simpl_out $results_file $(timeout_check $start_time $simpl_end $simpl_timeout)

if [[ ${#check} -ne 0 ]]; then
	echo "L2 Out:"
	tail -n 10 $l2_out
	echo "Makespeare Out:"
	tail -n 10 $makespeare_out
	echo "Simpl Out:"
	tail -n 10 $simpl_out
fi
