import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    N = int(random.randint(2, 5))
    alpha = int(random.randint(-5, 5))

    out = [0] * N
    x = gen_utils.randomintarray(N)
    y = gen_utils.randomintarray(N)

    for i in range(N):
        out[i] = alpha * x[i] + (1 - alpha) * y[i]

    return (x, y, alpha, N, out)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0])
    example_class.add_array_input(example[1])
    example_class.add_int_input(example[2])
    example_class.add_int_input(example[3])
    example_class.array_output(example[4])

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
fun x, xlen, y, ylen, alpha, n, out, outlen ->
i=0;
while(?) {
?;
}
return out;
"""
    example_sets['simpl'].empty_partial_program = """
fun x, xlen, y, ylen, alpha, n, out, outlen ->
?;
return out;
"""
    example_sets['simpl'].int_comps = "0,1"
    example_sets['simpl'].int_var_comps = 'xlen, ylen, alpha, n, outlen, i'
    example_sets['simpl'].array_var_comps = 'x, y, out'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.add_array_input([])
    base_case.add_int_input(0)
    base_case.add_int_input(0)
    base_case.array_output([])
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
