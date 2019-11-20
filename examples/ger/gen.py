import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    M = int(random.randint(2, 5))
    N = int(random.randint(2, 5))

    a = [0] * (M * N)
    x = gen_utils.randomintarray(M)
    y = gen_utils.randomintarray(N)

    for i in range(M):
        for j in range(N):
            a[j + i * N] = x[i] * y[j]

    return (M, N, x, y, a)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_int_input(example[0])
    example_class.add_int_input(example[1])
    example_class.add_array_input(example[2], nolen=True)
    example_class.add_array_input(example[3], nolen=True)
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
fun m, n, a, x, y ->
i=0;
j=0;
while(?) {
?;
}
return y;
"""
    example_sets['simpl'].empty_partial_program = """
fun m, n, a, x, y ->
?;
return y;
"""
    example_sets['simpl'].int_comps = "0,1"
    example_sets['simpl'].int_var_comps = 'm, n, i, j'
    example_sets['simpl'].array_var_comps = 'a, x, y'

    base_case = gen_utils.L2Example()
    base_case.add_int_input(0)
    base_case.add_int_input(0)
    base_case.add_array_input([], nolen=True)
    base_case.add_array_input([], nolen=True)
    base_case.array_output([], nolen=True)
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
