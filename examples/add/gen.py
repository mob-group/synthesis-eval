import sys
sys.path.insert(1, '..')
import gen_utils
import random


def generate_example():
    array_len = random.randint(2, 100)

    arr1 = []
    arr2 = []
    res = []

    for i in range(array_len):
        n1 = random.randint(-100, 100)
        n2 = random.randint(-100, 100)
        arr1.append(n1)
        arr2.append(n2)
        res.append(n1 + n2)

    return (arr1, arr2, res)


# This tool is independent of the syntool name.
def convert(example, example_class, syntool_name):
    example_class.two_array_input(example[0], example[1])
    example_class.array_output(example[2])

    return example_class


if __name__ == "__main__":
    random.seed(0)
    examples = gen_utils.generate(generate_example)
    # Create an output of each type using the convert
    # function.
    example_sets = gen_utils.build_sets(examples, convert)

    # Set up any important sub-fields in any of the tests.
    # None for this test.
    
    # Write them out to files.
    gen_utils.write_sets(example_sets)
