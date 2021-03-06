import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    len = random.randint(1, 20)
    array = gen_utils.randomintarray(len, min=-100, max=100)
    idx = 0
    min = 1000000
    for i in range(len):
        if array[i] < min:
            min = array[i]
            idx = i

    return (array, idx, min)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0])
    if syntool_name == "L2":
        # L2 is functional so needs an extra return value to keep track of the
        # min seen so far.
        example_class.array_output([example[2], example[1]])
    else:
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
n = 0;
c = 100000;
k = 0;
while (?) {
?;
};
return c;
"""
    example_sets['simpl'].empty_partial_program = """
fun arr, len ->
?;
return c;
"""
    example_sets['simpl'].int_comps = "0,1"
    example_sets['simpl'].int_var_comps = 'n,c,len,k'
    example_sets['simpl'].array_var_comps = 'arr'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.array_output([1000, -1])
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
