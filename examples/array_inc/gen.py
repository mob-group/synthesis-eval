import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    array_len = random.randint(1, 30)

    arr1 = []
    diff = random.randint(0, 100)
    res = []

    for i in range(array_len):
        n = random.randint(-100, 100)
        arr1.append(n)
        res.append(n + diff)

    return (arr1, diff, res)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0])
    example_class.add_int_input(example[1])
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
fun arr, len, n ->
r=0;
while(?) {
?;
r = r + 1;
}
return arr;
"""
    example_sets['simpl'].int_comps = "0"
    example_sets['simpl'].int_var_comps = 'n, len, r'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.add_int_input(2)
    base_case.array_output([])
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
