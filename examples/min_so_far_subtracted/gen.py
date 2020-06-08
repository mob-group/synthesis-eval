import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    len = random.randint(1, 10) * 2
    array = gen_utils.randomintarray(len)
    array2 = gen_utils.randomintarray(len)

    min_so_far_array = []
    min_so_far = 1

    for i in range(len):
        min_so_far = min_so_far if (min_so_far < array[i]) else 1
        min_so_far_array.append(min_so_far)

    #  Now, compute the max of the two
    max_of_min_so_far_and_other_array = []
    for i in range(len):
        m1 = min_so_far_array[i]
        m2 = array2[i]
        max = m1 if (m1 > m2) else m2
        max_of_min_so_far_and_other_array.append(max)

    result = []
    for i in range(len):
        result.append(min_so_far_array[i] - max_of_min_so_far_and_other_array[i])

    return (array, array2, result)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_array_input(example[0])
    example_class.add_array_input(example[1])
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
fun arr, len, drop ->
n = 0;
c = 0;
while(?) {
t = 0;
?;
}
return c;
"""
    example_sets['simpl'].empty_partial_program = """
fun arr, len, drop ->
?;
return c;
"""
    example_sets['simpl'].int_comps = "0,1,2,3"
    example_sets['simpl'].int_var_comps = 'n,c,len,t,drop'
    example_sets['simpl'].array_var_comps = 'arr'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.add_int_input(0)
    base_case.array_output([])
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
