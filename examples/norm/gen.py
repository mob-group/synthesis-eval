import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    array_len = random.randint(1, 30)
    arr = gen_utils.randomintarray(array_len, min=1)
    output = gen_utils.randomintarray(array_len)
    output_orig = output[:]

    size = 0
    for e in arr:
        size += e

    for i in range(len(output)):
        output[i] = (100 * output[i]) // size

    return (arr, output_orig, output)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0])
    example_class.add_array_input(example[1])
    example_class.in_place_array_output(example[2])

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
fun arr, len, outarr, outlen ->
r=0;
n=0;
while(?) {
?;
};
while(?) {
?;
};
return outarr;
"""
    example_sets['simpl'].empty_partial_program = """
fun arr, len, outarr, outlen ->
?;
return outarr;
"""
    example_sets['simpl'].int_comps = "0,1,100"
    example_sets['simpl'].int_var_comps = 'outlen, len, r, n'
    example_sets['simpl'].array_var_comps = 'arr, outarr'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.add_array_input([])
    base_case.array_output([])
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
