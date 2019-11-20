import sys
sys.path.insert(1, '..')
import gen_utils
import random
import math


def generate_example():
    array_len = random.randint(1, 30)
    arr = gen_utils.randomintarray(array_len)

    len = 0
    for e in arr:
        len += e * e

    return (arr, int(math.sqrt(len)))


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0])
    example_class.int_output(example[1])

    return example_class


if __name__ == "__main__":
    random.seed(0)
    examples = gen_utils.generate(generate_example)
    # Create an output of each type using the convert
    # function.
    example_sets = gen_utils.build_sets(examples, convert)

    # Set up any important sub-fields in any of the tests.
    # Need to set an example program for simpl.
    example_sets['simpl'].partial_program = """
fun arr, len ->
r=0;
n=0;
while(?) {
?;
};
?;
return r;
"""
    example_sets['simpl'].empty_partial_program = """
fun arr, len ->
?;
return r;
"""
    example_sets['simpl'].int_comps = "0,1"
    example_sets['simpl'].int_var_comps = 'len, r, n'
    example_sets['simpl'].array_var_comps = 'arr'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.int_output(0)
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
