import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    len = random.randint(1, 20)
    elem_index = random.randint(0, len - 1)
    string = gen_utils.randomstring(len)
    should_contain = random.randint(0, 1)

    if should_contain == 1:
        elem = string[elem_index]
    else:
        elem = string[0]
        tries = 0
        while elem in string:
            tries += 1
            elem = gen_utils.random_char()
            if tries == 100:
                should_contain = 1
                break

    return (string, elem, should_contain)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_str_input(example[0])
    example_class.add_chr_input(example[1])
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
fun str, elem ->
n = 0;
c = 0;
while (?) {
?;
};
return c;
"""
    example_sets['simpl'].empty_partial_program = """
fun str, elem ->
?;
return c;
"""
    example_sets['simpl'].int_comps = "0,1"
    example_sets['simpl'].int_var_comps = 'n,c,elem'
    example_sets['simpl'].array_var_comps = 'str'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.add_int_input(2)
    base_case.int_output(0)
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
