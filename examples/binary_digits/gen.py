import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    number = int(random.randint(1, 16))

    res = 1
    orig = number

    while number > 1:
        res += 1
        number = number // 2

    return (orig, res)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_int_input(example[0])
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
fun x ->
r=1;
while(?) {
?;
}
return r;
"""
    example_sets['simpl'].empty_partial_program = """
fun x ->
?;
return r;
"""
    example_sets['simpl'].int_comps = "0,1,2"
    example_sets['simpl'].int_var_comps = 'x, r'
    example_sets['simpl'].array_var_comps = 'none'

    base_case = gen_utils.L2Example()
    base_case.add_int_input(1)
    base_case.int_output(1)
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
