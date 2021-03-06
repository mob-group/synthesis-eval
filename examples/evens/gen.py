import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    array_len = random.randint(1, 30)

    arr1 = gen_utils.randomintarray(array_len)
    res = [x for x in arr1 if x % 2 == 0]

    return (arr1, res)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0])
    example_class.array_output(example[1])

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
fun arr, len, arrout, lenoth ->
r=1;
n = 0;
k = 0;
while(?) {
?;
}
return arrout;
"""
    example_sets['simpl'].empty_partial_program = """
fun arr, len, arrout, lenoth ->
?;
return arrout;
"""
    example_sets['simpl'].int_comps = "0,1,2"
    example_sets['simpl'].int_var_comps = 'len, r, n, lenoth, k'
    example_sets['simpl'].array_var_comps = 'arr, arrout'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.array_output([])
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
