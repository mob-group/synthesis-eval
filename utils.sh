#!/bin/echo "This should be sourced"

# This needs to remain shell-agnostic.  It is used by
# both ZSH and Bash scripts.  I typically use -u -e, which
# means that undefined variable can't be loaded.
get_config_value() {
	local field_name=$1
	# We assume the default config file is a local one.
	local config_file=${2:-config}

	if [[ ! -f $config_file ]]; then
		echo "Config file $config_file doesn't exist" >&2
		exit 2
	fi

	matches_count=$(grep -c -e "^$field_name: " $config_file || true)
	if [[ $matches_count == "0" ]]; then
		echo "Expected to find config value $field_name but found" >&2
		echo "nothing.  Does the file $config_file contain $field_name?" >&2
		exit 1
	elif [[ $matches_count -gt 1 ]]; then
		echo "Expected to find only one value for $field_name but found " >&2
		echo "many.  Does the file $config_file contain $field_name?" >&2
		exit 1
	fi

	# Now we've got the field, we can get the value out with awk.
	awk -F': '  "/^$field_name:/ {print \$2}" $config_file
}

exportf() {
    export $(echo $1)="`whence -f $1 | sed -e "s/$1 //" `"
}

list_descendants () {
	children=$(ps -o pid= --ppid "$1")
	echo $children

	for pid in $children
	do
		list_descendants "$pid"
	done

	echo "$children"
}

list_descendents_from_proc() {
	list_descendants $$
}

kill_children() {
	echo "Killing children!"
	children=$(list_descendants $$)
	kill -9 $children || true
	echo "Killed $children"
}

