import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    array_len_1 = random.randint(1, 30)
    array_len_2 = random.randint(1, 30)

    inp = gen_utils.randomintarray(array_len_1)
    outp = sorted(inp)

    return (inp, outp)

# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0])
    example_class.in_place_array_output(example[1])

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
fun arr, len ->
p1 = 0;
p2 = 0;
p3 = 0;
while(?) {
?;
}
return arr;
"""
    example_sets['simpl'].int_comps = "0,1"
    example_sets['simpl'].int_var_comps = 'len, p1, p2, p3'
    example_sets['simpl'].array_var_comps = 'arr'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([1])
    base_case.array_output([1])
    base_case2 = gen_utils.L2Example()
    base_case2.add_array_input([])
    base_case2.array_output([])
    example_sets['L2'].base_cases = [base_case, base_case2]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
