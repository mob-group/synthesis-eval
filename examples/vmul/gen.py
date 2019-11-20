
import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    arrlen = random.randint(1, 20)
    array = gen_utils.randomintarray(arrlen)
    other_array = gen_utils.randomintarray(arrlen, min=1)
    n_arr = []

    for i in range(len(array)):
        n_arr.append(array[i] * other_array[i])

    return (array, other_array, n_arr)


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
fun arr, len, otherarray, otherlen, outarr, outlen ->
n = 0;
while(?) {
?;
}
return arr;
"""
    example_sets['simpl'].empty_partial_program = """
fun arr, len, otherarray, otherlen, outarr, outlen ->
?;
return arr;
"""
    example_sets['simpl'].int_comps = "0,1,2"
    example_sets['simpl'].int_var_comps = 'n,len,otherlen,outlen'
    example_sets['simpl'].array_var_comps = 'arr,otherarray,outarr'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.add_array_input([])
    base_case.array_output([])
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
