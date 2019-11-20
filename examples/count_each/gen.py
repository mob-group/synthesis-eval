import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    n = random.randint(1, 1000000)
    orig = n

    res = [0] * 10

    while n > 0:
        dig = n % 10
        res[dig] += 1
        n = n // 10

    return (orig, res)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_int_input(example[0])
    example_class.array_output(example[1])

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
fun n, resarr ->
while(?) {
?;
}
return resarr;
"""
    example_sets['simpl'].empty_partial_program = """
fun n, resarr ->
?;
return resarr;
"""
    example_sets['simpl'].int_comps = "0,10"
    example_sets['simpl'].int_var_comps = 'n'
    example_sets['simpl'].array_var_comps = 'resarr'

    base_case = gen_utils.L2Example()
    base_case.add_int_input(0)
    base_case.array_output([0] * 10)
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
