import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    N = int(random.randint(2, 20))

    inarr = gen_utils.randomintarray(N, min=-5, max=5)
    outarr = [0] * N
    coeffs = gen_utils.randomintarray(N, min=-5, max=5)

    for n in range(N):
        outarr[n] = 0
        for i in range(0, N - 1):
            outarr[n] += coeffs[i] * inarr[N - 1 - i]

    return (inarr, coeffs, N, outarr)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0], nolen=True)
    example_class.add_array_input(example[1], nolen=True)
    example_class.add_int_input(example[2])
    example_class.array_output(example[3], nolen=True)

    return example_class


if __name__ == "__main__":
    random.seed(0)
    examples = gen_utils.generate(generate_example)
    # Create an output of each type using the convert
    # function.
    example_sets = gen_utils.build_sets(examples, convert)

    example_sets['LLM'].liveout = ['out']

    # Set up any important sub-fields in any of the tests.
    # Need to set an example program for simpl.
    example_sets['simpl'].partial_program = """
fun in, coeffs, n, out ->
i=0;
j=0;
while(?) {
?;
}
return out;
"""
    example_sets['simpl'].empty_partial_program = """
fun in, coeffs, n, out ->
?;
return out;
"""
    example_sets['simpl'].int_comps = "0,1"
    example_sets['simpl'].int_var_comps = 'i, j, n'
    example_sets['simpl'].array_var_comps = 'in, coeffs, out'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([], nolen=True)
    base_case.add_array_input([], nolen=True)
    base_case.add_int_input(0)
    base_case.array_output([], nolen=True)
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
