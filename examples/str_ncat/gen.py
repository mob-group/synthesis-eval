import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    len = random.randint(1, 20)
    len2 = random.randint(1, 20)
    n = random.randint(1, 20)
    str1 = gen_utils.randomstring(len)
    str2 = gen_utils.randomstring(len2)

    if n > len2:
        out_str = str1 + str2[:n - 1]
    else:
        out_str = str1 + str2

    return (str1, str2, n, out_str)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_str_input(example[0])
    example_class.add_str_input(example[1])
    example_class.add_int_input(example[2])
    example_class.str_output(example[3])

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
fun str1, str2, lenapp, strout ->
n = 0;
c = 0;
while (?) {
?;
};
n = 0;
while(?){
?;
};
return strout;
"""
    example_sets['simpl'].empty_partial_program = """
fun str1, str2, lenapp, strout ->
?;
return strout;
"""
    example_sets['simpl'].int_comps = "0,1"
    example_sets['simpl'].int_var_comps = 'n,c,lenapp'
    example_sets['simpl'].array_var_comps = 'str1, str2, strout'

    base_case = gen_utils.L2Example()
    base_case.add_str_input('')
    base_case.add_str_input('')
    base_case.add_int_input(0)
    base_case.str_output('')
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
