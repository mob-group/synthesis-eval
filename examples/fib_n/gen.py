import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    n = random.randint(1, 10)
    orig = n

    res = 1
    i = 1

    while n > 1:
        i = res - i
        res = i + res
        n = n - 1

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
fun n ->
i = 1;
r = 1;
while(?) {
?;
}
return r;
"""
    example_sets['simpl'].empty_partial_program = """
fun n ->
?;
return r;
"""
    example_sets['simpl'].int_comps = "1"
    example_sets['simpl'].int_var_comps = 'n,r,i'
    example_sets['simpl'].array_var_comps = 'none'

    base_case = gen_utils.L2Example()
    base_case.add_int_input(2)
    base_case.int_output(1)

    other_base_case = gen_utils.L2Example()
    other_base_case.add_int_input(1)
    other_base_case.int_output(1)
    example_sets['L2'].base_cases = [base_case, other_base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
