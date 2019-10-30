import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    graphsize = random.randint(1, 5)
    arrlen = graphsize ** 2
    array = gen_utils.randomintarray(arrlen, max=1)
    all_arr = []

    for i in range(graphsize):
        all = 1
        for j in range(graphsize):
            if array[i * graphsize + j] != 0:
                all = 0
        all_arr.append(all)

    return (array, graphsize, all_arr)


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
fun arr, len, graphsize, outarr, outlen ->
i = 0;
j = 0;
while(?) {
all = 0;
?;
}
return ourarr;
"""
    example_sets['simpl'].int_comps = "0,1,2"
    example_sets['simpl'].int_var_comps = 'len, graphsize, outlen, i, j, all'
    example_sets['simpl'].array_var_comps = 'arr, outarr'

    base_case = gen_utils.L2Example()
    base_case.add_array_input([])
    base_case.add_int_input(0)
    base_case.array_output([])
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
