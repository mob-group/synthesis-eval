import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    N = random.randint(2, 5)
    M = random.randint(2, 5)
    arr1 = gen_utils.randomintarray(N * M)
    arr2 = gen_utils.randomintarray(N * M)
    newarr = [0] * (N * M)

    for i in range(N * M):
        newarr[i] = arr1[i] + arr2[i]

    return (arr1, arr2, N, M, newarr)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0], nolen=True)
    example_class.add_array_input(example[1], nolen=True)
    example_class.add_int_input(example[2])
    example_class.add_int_input(example[3])
    example_class.array_output(example[4], nolen=True)

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
fun arr, arr2, n, m, arrout ->
r=0;
p=0;
while(?) {
?;
}
return arrout;
"""
    example_sets['simpl'].int_comps = "0,1"
    example_sets['simpl'].int_var_comps = 'r, p, m, n'
    example_sets['simpl'].array_var_comps = 'arr, arr2, arrout'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([], nolen=True)
    base_case.add_array_input([], nolen=True)
    base_case.add_int_input(0)
    base_case.add_int_input(0)
    base_case.array_output([], nolen=True)
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
