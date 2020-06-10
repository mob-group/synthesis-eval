import sys
sys.path.insert(1, '..')
import gen_utils
import random

gen_utils.handle_args()

def generate_example():
    M = int(random.randint(2, 6))
    K = int(random.randint(2, 6))

    inarr = gen_utils.randomintarray(M)
    karr = gen_utils.randomintarray(K)
    sumarr = [0] * M

    for i in range(M):
        sum = 0
        for j in range(K):
            idx = i - j
            ival = 0 if i - j < 0 else inarr[idx]
            sum += ival * karr[j]
        sumarr[i] = sum

    return (M, K, inarr, karr, sumarr)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_int_input(example[0])
    example_class.add_int_input(example[1])
    example_class.add_array_input(example[2], nolen=True)
    example_class.add_array_input(example[3], nolen=True)

    example_class.array_output(example[4], nolen=True)

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
fun m, k, marr, karr, arrout ->
i=0;
j=0;
while(?) {
?;
}
return arrout;
"""
    example_sets['simpl'].empty_partial_program = """
fun m, k, marr, karr, arrout ->
?;
return arrout;
"""
    example_sets['simpl'].int_comps = "0,1,2,3"
    example_sets['simpl'].int_var_comps = 'i, j, m, k'
    example_sets['simpl'].array_var_comps = 'marr, karr, arrout'

    base_case = gen_utils.L2Example()
    base_case.add_int_input(0)
    base_case.add_int_input(2)
    base_case.add_array_input([], nolen=True)
    base_case.add_array_input([3, 4], nolen=True)
    base_case.array_output([], nolen=True)
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
