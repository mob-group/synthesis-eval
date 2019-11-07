import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    array_len = random.randint(1, 30)
    len2 = random.randint(1, 30)

    arr1 = list(gen_utils.randomstring(array_len))
    arr2 = list(gen_utils.randomstring(len2))
    n = random.randint(1, 30)
    within_range_n = min(n, min(array_len, len2))

    are_equal = random.randint(0, 1)
    if are_equal == 1 or (array_len == len2 and arr1[:within_range_n] == arr2[:within_range_n]):
        res = 1
        for i in range(within_range_n):
            arr2[i] = arr1[i]
        if within_range_n < n:
            while len(arr2) > len(arr1):
                del arr2[-1]
            while len(arr1) > len(arr2):
                del arr1[-1]
    else:
        res = 0
    return (''.join(arr1), ''.join(arr2), n, res)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.add_str_input(example[0])
    example_class.add_str_input(example[1])
    example_class.add_int_input(example[2])
    example_class.int_output(example[3])

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
fun str1, str2, cmplen ->
r=1;
n=0;
while(?) {
?;
}
return r;
"""
    example_sets['simpl'].int_comps = "0,1"
    example_sets['simpl'].int_var_comps = 'r, n, cmplen'
    example_sets['simpl'].array_var_comps = 'str1, str2'

    base_case = gen_utils.L2Example()
    base_case.add_str_input('')
    base_case.add_str_input('')
    base_case.add_int_input(0)
    base_case.int_output(1)
    example_sets['L2'].base_cases = [base_case]

    # Write them out to files.
    gen_utils.write_sets(example_sets)
