import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    a = random.randint(0, 20)
    n = random.randint(0, 10)
    return (a, n, a ** n)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.two_int_input(example[0], example[1])
    example_class.int_output(example[2])

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
fun a, n ->
r=1;
while(?) {
?;
}
return r;
"""
    example_sets['simpl'].empty_partial_program = """
fun a, n ->
?;
return r;
"""
    example_sets['simpl'].int_comps = "0"
    example_sets['simpl'].int_var_comps = 'a, n, r'

    base_case = gen_utils.L2Example()
    base_case.two_int_input(5, 0)
    base_case.int_output(1)
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
