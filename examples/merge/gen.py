import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    array_len_1 = random.randint(1, 30)
    array_len_2 = random.randint(1, 30)

    arr1 = sorted(gen_utils.randomintarray(array_len_1))
    arr2 = sorted(gen_utils.randomintarray(array_len_2))

    outarr = sorted(arr1 + arr2)
    return (arr1, arr2, outarr)

# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0])
    example_class.add_array_input(example[1])
    example_class.array_output(example[2])

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
fun arr, len, arroth, lenoth, outarr, outlen ->
p1 = 0;
p2 = 0;
p3 = 0;
while(?) {
?;
}
return outarr;
"""
    example_sets['simpl'].empty_partial_program = """
fun arr, len, arroth, lenoth, outarr, outlen ->
?;
return outarr;
"""
    example_sets['simpl'].int_comps = "0,1"
    example_sets['simpl'].int_var_comps = 'len, lenoth, outlen, p1, p2, p3'
    example_sets['simpl'].array_var_comps = 'arr, arroth, outarr'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.add_array_input([1])
    base_case.array_output([1])
    base_case2 = gen_utils.L2Example()
    base_case2.add_array_input([1])
    base_case2.add_array_input([])
    base_case2.array_output([1])
    base_case3 = gen_utils.L2Example()
    base_case3.add_array_input([])
    base_case3.add_array_input([])
    base_case3.array_output([])
    example_sets['L2'].base_cases = [base_case, base_case2, base_case3]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
