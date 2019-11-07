import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    len = random.randint(1, 20)
    string = list(gen_utils.randomstring(len))
    starting_ind_count = random.randint(0, len // 2)

    starting_char = string[0]
    replacement_char = starting_char
    while replacement_char == starting_char:
        replacement_char = gen_utils.random_char()

    for i in range(0, starting_ind_count):
        string[i] = starting_char

    # Make sure the next char is not the same as the
    # ones we are looking at.
    if string[starting_ind_count] == starting_char:
        string[starting_ind_count] = replacement_char

    return (''.join(string), starting_char, starting_ind_count)


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
