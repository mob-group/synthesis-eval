import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    len = random.randint(1, 10) * 2
    array = gen_utils.randomintarray(len)
    array2 = gen_utils.randomintarray(len)

    result = 0
    for i in range(len(array)):
        x = arr[i] - arr2[i];
        if (x % 2 == 0):
          out[filtered] = x * arr2[filtered];
    return (array, array2, out)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0])
    example_class.add_array_input(example[1])
    example_class.add_array_output(example[2])

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
fun arr, len, arr2, len2, outarr, outlen ->
n = 0;
c = 0;
while(?) {
t = 0;
?;
}
return outarr;
"""
    example_sets['simpl'].empty_partial_program = """
fun arr, len, arr2, len2, outarr, outlen ->
?;
return c;
"""
    example_sets['simpl'].int_comps = "0,1,2,3"
    example_sets['simpl'].int_var_comps = 'n,c,len,t,len2,outlen'
    example_sets['simpl'].array_var_comps = 'arr, arr2, outarr'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.add_array_input([])
    base_case.array_output([])
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
