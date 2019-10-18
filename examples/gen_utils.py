# These constants represent the number of examples that we should present to each
# type of synthesis tool.
MAX_MAKESPEARE = 2200
MAX_SIMPL = 10
MAX_L2 = 10
MAX_PLDI = 10 # TODO
MAX_BASELINE = 10 # TODO
TYPE_LENGTHS = {
        'simpl': MAX_SIMPL,
        'L2': MAX_L2,
        'PLDI': MAX_PLDI,
        'Baseline': MAX_BASELINE,
        'makespeare': MAX_MAKESPEARE
}
MAX = TYPE_LENGTHS[max(TYPE_LENGTHS)]

# This is a list of the supported synthesis program types.
TYPES = ["L2", "makespeare", "simpl"] # TODO -- Add PLDI and Baseline once those are supported.


# This is a set of classes that help formatting everything to the right output.
class ExampleSet(object):
    def __init__(self):
        self.examples = []


    def add_example(self, example):
        self.examples.append(example)


    def write(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))


    def __str__(self):
        return '\n'.join([str(example) for example in self.examples])


# This is a superset of the single example classes.  It contains a list
# of functions that should be implemented to help the generation tools.
class Example(object):
    def __init__(self):
        pass

    # This should set the input stream to two arrays.  Lengths should
    # be specified where appropriate if needed.
    def two_array_input(self, arr1, arr2):
        pass

    # This sets a single array as the expected output.  Lengths should
    # be specified where appropriate if needed.
    def array_output(self):
        pass

    # Format an array as requied for the input format of the program (if required).
    def __format_arr(self, arr):
        return arr


# A list of makespeare examples: this one is just an empty body.
class Makespeare(ExampleSet):
    def __init__(self):
        super(Makespeare, self).__init__()
        self.type = "makespeare"

    def __str__(self):
        # Make sure there are some training and some test data
        for i in range(0, int(0.9 * len(self.examples))):
            self.examples[i].traintest = 0
        for i in range(int(0.9 * len(self.examples)), len(self.examples)):
            self.examples[i].traintest = 1

        return super(Makespeare, self).__str__()


# Simpl tracks a few other fields and makes sure those are appropriately
# output.
class Simpl(ExampleSet):
    def __init__(self):
        super(Simpl, self).__init__()
        self.type = "simpl"
        self.partial_program = "TODO"
        self.int_comps = "TODO"
        self.int_var_comps = "TODO"
        self.array_var_comps = "none"

    def __str__(self):
        return """Examples
{example}

Partial Program
{prog}

Int Comps
{ints}

Int Var Comps
{vars}

Array Var Comps
{arrays}""".format(example=super(Simpl, self).__str__(), prog=self.partial_program, ints=self.int_comps, vars=self.int_var_comps, arrays=self.array_var_comps)


class L2(ExampleSet):
    def __init__(self):
        super(L2, self).__init__()
        self.type = "L2"
        self.name = "f"
        self.kind = 'examples'
        self.description = "An auto-generated example set"
        self.background = []


    def __str__(self):
        self_dict = {
                'name': self.name,
                'kind': self.kind,
                'description': self.description,
                'background': self.background,
                'contents': {
                    'examples': [str(ex) for ex in self.examples]
                }
        }
        return str(self_dict)


# TODO -- These all need to have a constructor that is: (a) no (non-self) arguments, and (b) makes a call to the superclass __init__ function.
# These two need to implment the __str__(self) function, which should return a string
# that will be put in a file as the input file for the synthesis tool.
class PLDI(ExampleSet):
    pass

class Baseline(ExampleSet):
    pass

# TODO -- These all need to have a constructor that is: (a) no (non-self) arguments, and (b) makes a call to the superclass __init__ function.
# These need to implement all the skeletons in the Example class. Warning: there are likely
# to be more skeletons that need to be done later.
class PLDIExample(Example):
    pass

class BaselineExample(Example):
    pass


class SimplExample(Example):
    def __init__(self):
        super(SimplExample, self).__init__()
        self.inputs = []
        self.outputs = []

    # Format an array like in simpl.
    def __format_arr(self, array):
        return '{' + ','.join([str(x) for x in array]) + '}'

    def two_array_input(self, arr1, arr2):
        self.inputs = [self.__format_arr(arr1), self.__format_arr(arr2), len(arr1), len(arr2)]
        
    def array_output(self, arr):
        self.outputs = [self.__format_arr(arr)]

    def __str__(self):
        return ','.join([str(x) for x in self.inputs]) + ' -> ' + ','.join([str(x) for x in self.outputs]) + ';'


class MakespeareExample(Example):
    def __init__(self):
        super(MakespeareExample, self).__init__()
        self.traintest = 0
        self.r7 = 0
        self.r6 = 0
        self.r2 = 0
        self.r0 = 0
        self.r8 = 0
        self.r9 = 0
        self.input_mem_size = 0
        self.input_mem = []
        self.scalar_ret_flag = 0
        self.scalar_ret_val = 0
        self.output_mem_start = 0
        self.output_mem_size = 0
        self.output_mem = []

    # Set two arrays as the inputs.
    def two_array_input(self, arr1, arr2):
        # This is a massive fudge because the input system 'supports' this,
        # but will never figure out how memory is partitioned.
        self.r7 = len(arr1)
        self.r6 = len(arr2)

        self.input_mem = arr1 + arr2
        self.input_mem_size = len(arr1) + len(arr2)

    # Set a single array as the expected output.
    def array_output(self, arr):
        self.output_mem_size = len(arr)
        self.output_mem = arr

    def __str__(self):
        values = [self.traintest, self.r7, self.r6, self.r2, self.r0, self.r8, self.r9, self.input_mem_size, ' '.join([str(x) for x in self.input_mem]), self.scalar_ret_flag, self.scalar_ret_val, self.output_mem_start, self.output_mem_size, ' '.join([str(x) for x in self.output_mem])]
        values = [str(value) for value in values]

        return '\t'.join(values)


class L2Example(Example):
    def __init__(self):
        super(L2Example, self).__init__()
        self.name = "f"
        self.inputs = []
        self.outputs = []

    def two_array_input(self, arr1, arr2):
        self.inputs = [arr1, arr2]

    def array_output(self, arr):
        self.outputs = arr

    def __str__(self):
        str_in = [str(inp) for inp in self.inputs]
        str_out = [str(out) for out in self.outputs]
        return "(" + self.name + ' ' + ' '.join(str_in) + ') -> ' + ' '.join(str_out)


# Generate as many examples as needed and return them as a list.
def generate(gen_function):
    examples = []
    for i in range(MAX):
        examples.append(gen_function())
    return examples


def empty_set_gen(type):
    if type == "L2":
        return L2()
    elif type == "simpl":
        return Simpl()
    elif type == "makespeare":
        return Makespeare()
    elif type == "PLDI":
        return PLDI()
    elif type == "Baseline":
        return Baseline()
    else:
        raise Error("Unsupported type " + type + " in the empty_set_gen function")


def empty_example_gen(type):
    if type == "L2":
        return L2Example()
    elif type == "simpl":
        return SimplExample()
    elif type == "makespeare":
        return MakespeareExample()
    elif type == "PLDI":
        return PLDIExample()
    elif type == "Baseline":
        return BaselineExample()
    else:
        raise Error("Unsupported type " + type + " in the empty_example_gen function")

# Given a list of examples, and a function to convert from (example: T, example: Example, type: str) to
# an ExampleSet of the appropriate type, generate the example sets for each TYPES.
def build_sets(examples, convert):
    sets = {}
    for type in TYPES:
        empty_set = empty_set_gen(type)
        type_count = TYPE_LENGTHS[type]
        # Don't generate more examples for this one than requested.
        for example in examples[0:type_count - 1]:
            empty_example_instance = empty_example_gen(type)
            empty_set.add_example(convert(example, empty_example_instance, type))

        sets[type] = empty_set
    return sets


# Given a dict of sets, write them out to disk on the appropriate files.
def write_sets(sets):
    for type in TYPES:
        # the type doubles as the filename.
        sets[type].write(type)
