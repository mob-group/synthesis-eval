from type import Context, arrow, tint, tlist, UnificationFailure
from functools import reduce
import argparse
import json
import random
import pickle
import re

# These constants represent the number of examples that we should present to each
# type of synthesis tool.
MAX_MAKESPEARE = 2200
MAX_SIMPL = 10
MAX_L2 = 10
MAX_PLDI = 10 # TODO
MAX_BASELINE = 10 # TODO
MAX_SKETCH_ADAPT = 10
MAX_LLM=10
TYPE_LENGTHS = {
        'simpl': MAX_SIMPL,
        'L2': MAX_L2,
        'PLDI': MAX_PLDI,
        'Baseline': MAX_BASELINE,
        'makespeare': MAX_MAKESPEARE,
        'SketchAdapt': MAX_SKETCH_ADAPT,
        'LLM': MAX_LLM
}
MAX = max(TYPE_LENGTHS.values())
# Do not assign here.  This is set via the --no-help flag.  See the args() function.
NO_HELP_MODE = False

# This is a list of the supported synthesis program types.
TYPES = ["L2", "makespeare", "simpl", "SketchAdapt", "LLM"] # TODO -- Add PLDI and Baseline once those are supported.

def load_file():
    # Load the ref.c file into a string.
    with open('ref.c', 'r') as f:
        return f.readlines()

def get_function():
    lines = load_file()
    # all lines but the deps.
    return ''.join([line for line in lines if '#include' not in line])

def get_deps():
    lines = load_file()
    return ''.join([line for line in lines if '#include' in line])

def in_place():
    header = get_header()
    typ = header.split(' ')[0]
    return typ.strip() == 'void'

def get_header():
    lines = load_file()
    # Get the first line that is plausibly the signature

    for line in lines:
        if line.strip().endswith('{'):
            if line.strip().startswith('{'):
                # Format is likely sig \n {
                starting_line = last_line
                break
            else:
                starting_line = line
                break
        else: # line does not end with {
            last_line = line
    return starting_line.replace('{', '')

def get_implementation():
    return ''.join(load_file())

def get_arg_names():
    return [n for (_, n) in get_args()]

def get_arg_types():
    return [t for (t, _) in get_args()]

def get_fname():
    header = get_header()
    header = header.replace('*', '').replace('(', ' ')
    name_start = header.split(' ')[1]

    return name_start

def get_args():
    sig = get_header()
    argstart = sig.index('(')
    argend = sig.index(')')

    args = sig[argstart + 1:argend]
    names_and_types = []
    for arg in args.split(','):
        print(arg)
        type, name = arg.strip().split(' ')
        while name.startswith('*'):
            name = name[1:]
            type = type + '*'
        names_and_types.append((type, name))

    return names_and_types

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
        self.add_array_input(arr1)
        self.add_array_input(arr2)

    def two_int_input(self, i1, i2):
        self.add_int_input(i1)
        self.add_int_input(i2)

    def str_to_array(self, string):
        arry = []
        for chr in string:
            assert ord(chr) != 0
            arry.append(ord(chr))
        arry.append(0)
        return arry

    def add_str_input(self, string, tail_length=0):
        # This is just a zero-terminated array, so make it so.
        arry = self.str_to_array(string)

        if tail_length > 0:
            # Makespeare and L2 can 'cheat' where they know
            # where the end of the array is because they
            # know (Makespeare) how long memory is or because
            # they have empty list checks (L2).
            # This makes string operations harder, but 
            # aguably fairer for them where it's nessecary.
            arry += [0] * tail_length

        self.add_array_input(arry, nolen=True)

    def add_chr_input(self, char):
        assert len(char) == 1
        self.add_int_input(ord(char)) 
    def add_array_input(self, arr, nolen=False):
        pass

    def add_int_input(self, int):
        pass

    def str_output(self, str):
        array = self.str_to_array(str)
        self.array_output(array)

    def in_place_str_output(self, str):
        array = self.str_to_array(str)
        self.in_place_array_output(array)

    # This sets a single array as the expected output.  Lengths should
    # be specified where appropriate if needed.
    def array_output(self, arr, nolen=False):
        pass

    def char_output(self, char):
        self.int_output(ord(char))

    def string_output(self, string):
        pass

    # For many languages, this is not possible, so just skip it.
    def in_place_array_output(self, arr):
        self.array_output(arr)

    def int_output(self, i):
        pass

    # Format an array as requied for the input format of the program (if required).
    def __format_arr(self, arr):
        return arr


# A list of sketcadapt examples.
class SketchAdapt(ExampleSet):
    def __init__(self):
        super(SketchAdapt, self).__init__()
        self.type = "SketchAdapt"

    def write(self, filename):
        examples = self.convert_examples_to_datum()
        with open(filename, 'wb') as f:
            pickle.dump(examples, f)

    def convert_examples_to_datum(self):
        # Get the type first:
        funtype = self.examples[0].typeof()
        ioexamples = []
        for example in self.examples:
            inputs = example.inputs
            outputs = example.outputs[0]
            non_int = False
            for inp in inputs:
                if type(inp) != type(1):
                    non_int = True

            # This is all integers, so transform it into a list.
            if not non_int:
                print("Warning: converting type for SketchAdapt to avoid int->int")
                inputs = (list(example.inputs),)
                print(inputs)
                funtype = arrow(tlist(tint), self.examples[0].outtype)

            ioexamples.append((inputs, outputs))
        ioexamples = tuple(ioexamples)

        datum = Datum(funtype, None, None, ioexamples, None, None, None, None)
        return [datum]

    def __str__(self):
        print("Should not be calling SketchAdap.__str__")

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
        program_to_use = self.empty_partial_program if NO_HELP_MODE else self.partial_program
        return """Examples
{example}

Partial Program
{prog}

Int Comps
{ints}

Int Var Comps
{vars}

Array Var Comps
{arrays}""".format(example=super(Simpl, self).__str__(), prog=program_to_use, ints=self.int_comps, vars=self.int_var_comps, arrays=self.array_var_comps)


class L2(ExampleSet):
    def __init__(self):
        super(L2, self).__init__()
        self.type = "L2"
        self.name = "f"
        self.kind = 'examples'
        self.description = "An auto-generated example set"
        self.background = []
        self.base_cases = []


    def __str__(self):
        base_cases_to_use = [] if NO_HELP_MODE else self.base_cases
        self_dict = {
                'name': self.name,
                'kind': self.kind,
                'description': self.description,
                'background': self.background,
                'contents': {
                    'examples': [str(ex) for ex in base_cases_to_use] + [str(ex) for ex in self.examples]
                }
        }
        return json.dumps(self_dict)

class LLM(ExampleSet):
    def __init__(self):
        super(LLM, self).__init__()
        self.liveout = []

    def __str__(self):
        # io_pairs should be a list of dicts --- each dict should have 'input'
        # and 'output' sub-dicts
        io_pairs = []
        inputvnames = get_arg_names()
        inputtypes = get_arg_types()

        for example in self.examples:
            iopair = {}
            inputs = example.inputs
            outputs = example.outputs

            inputs_dict = {}
            for i in range(len(inputs)):
                inputs_dict[inputvnames[i]] = inputs[i]

            # These functions are either in-place or not in-place, never both.
            outputs_dict = {}
            if in_place():
                if len(self.liveout) == 0:
                    print("Warning: generating outputs for liveout, but have no liveout!  Empty function? (Or specify llm liveout)")
                for i in range(len(self.liveout)):
                    liveoutname = self.liveout[i]
                    outputs_dict[liveoutname] = outputs[i]
            else:
                for out in outputs:
                    outputs_dict["returnv"] = out

            iopair['inputs'] = inputs_dict
            iopair['outputs'] = outputs_dict

            io_pairs.append(iopair)

        self_dict = {
                'func_def': get_function(),
                'real_deps': get_deps(),
                'fun_head_types': get_header().strip(),
                'real_io_pairs': io_pairs,
                'fname': get_fname()
        }

        return json.dumps(self_dict)

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

# This is a datatype class used by the deepcoder data pickle files.
class Datum():
    def __init__(self, tp, p, pseq, IO, sketch, sketchseq, reward, sketchprob):
        self.tp = tp
        self.p = p
        self.pseq = pseq
        self.IO = IO
        self.sketch = sketch
        self.sketchseq = sketchseq
        self.reward = reward
        self.sketchprob = sketchprob

    def __hash__(self): 
        from utilities import flatten
        return reduce(lambda a, b: hash(a + hash(b)), flatten(self.IO), 0) + hash(self.p) + hash(self.sketch)


class SketchAdaptExample(Example):
    def __init__(self):
        super(SketchAdaptExample, self).__init__()
        self.inputs = []
        self.outputs = []

        self.intype = []
        self.outtype = None

    def add_array_input(self, arr1, nolen=False):
        self.intype.append(tlist(tint))
        if nolen:
            self.inputs.append(arr1)
        else:
            self.inputs.append(arr1)
            # I think the length field breaks a bunch
            # of the inputs.
            # self.add_int_input(len(arr1))

    def add_int_input(self, i):
        self.inputs.append(i)
        self.intype.append(tint)

    def array_output(self, arr, nolen=False):
        self.outputs = [arr]
        self.outtype = tlist(tint)

    def int_output(self, i):
        self.outputs = [i]
        self.outtype = tint

    def typeof(self):
        thetype = self.outtype
        for t in self.intype[::-1]:
            thetype = arrow(t, thetype)

        return thetype

    def __str__(self):
        print("SketchAdapt should be converted to pickel not a string")
        raise Error()

class SimplExample(Example):
    def __init__(self):
        super(SimplExample, self).__init__()
        self.inputs = []
        self.outputs = []

    # Format an array like in simpl.
    def __format_arr(self, array):
        return '{' + ','.join([str(x) for x in array]) + '}'

    def add_array_input(self, arr1, nolen=False):
        self.inputs.append(self.__format_arr(arr1))
        if not nolen:
            self.inputs.append(len(arr1))

    def add_int_input(self, i):
        self.inputs.append(i)

    def array_output(self, arr, nolen=False):
        self.outputs = [self.__format_arr(arr)]

        # We also need to add an array of the same length as an input
        # since there appears to be no way for Simpl to generate an array.
        self.add_array_input([0] * len(arr), nolen=nolen)

    def in_place_array_output(self, arr):
        # In-place means one of the arguments is going to be reused,
        # so don't pass the same thing again.
        self.outputs = [self.__format_arr(arr)]

    def int_output(self, i):
        self.outputs = [i]

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
        if NO_HELP_MODE:
            # Fill the registers with junk.  Meaningful values will
            # be placed in some registers when requierd.
            self.r7 = 14321
            self.r6 = 587
            self.r2 = 8320
            self.r0 = 7
            self.r8 = 92
            self.r9 = 29805
        self.input_mem_size = 0
        self.input_mem = []
        self.scalar_ret_flag = 0
        self.scalar_ret_val = 0
        self.output_mem_start = 0
        self.output_mem_size = 0
        self.output_mem = []

        self.length_register_index = 0


    # Use the next unused register to pass the number 'n'.
    def pass_number(self, n):
        # Note that there is no r6, as Makespeare is best helped
        # by putting len(memory - 1) in that.
        reg_list = ['r7', 'r2', 'r0', 'r8', 'r9']
        if NO_HELP_MODE:
            reg_list = ['r8', 'r7', 'r0', 'r9', 'r2']
        if self.length_register_index > len(reg_list):
            raise Exception("Makespear example was passed too many arguments.  Got " + str(self.length_register_index) + " but have a max of " + str(len(reg_list)))
        register = reg_list[self.length_register_index]

        self.length_register_index += 1
        self.__dict__[register] = n

    def add_array_input(self, arr, nolen=False):
        # This is a massive fudge because the input system 'supports' this,
        # but will never figure out how memory is partitioned.
        if not nolen:
            self.pass_number(len(arr))

        self.input_mem += arr
        self.input_mem_size += len(arr)

    def add_int_input(self, i):
        # This could happen, it may or may not help.
        # self.pass_number(input_mem_size)
        self.input_mem.append(i)
        self.input_mem_size += 1

    def int_output(self, i):
        self.output_mem_size = 1
        self.output_mem = [i]

    # Set a single array as the expected output.
    def array_output(self, arr, nolen=False):
        self.output_mem_size = len(arr)
        # There is no way to avoid passing the length here.
        self.output_mem = arr

    def __str__(self):
        self.r6 = self.input_mem_size - 1
        values = [self.traintest, self.r7, self.r6, self.r2, self.r0, self.r8, self.r9, self.input_mem_size, ' '.join([str(x) for x in self.input_mem]), self.scalar_ret_flag, self.scalar_ret_val, self.output_mem_start, self.output_mem_size, ' '.join([str(x) for x in self.output_mem])]
        values = [str(value) for value in values]

        return '\t'.join(values)


class L2Example(Example):
    def __init__(self):
        super(L2Example, self).__init__()
        self.name = "f"
        self.inputs = []
        self.outputs = []

    def __format_arr(self, arr):
        return '[' + ' '.join([str(x) for x in arr]) + ']'

    def add_array_input(self, arr, nolen=False):
        self.inputs.append(self.__format_arr(arr))

    def add_int_input(self, i):
        self.inputs.append(i)

    def array_output(self, arr, nolen=False):
        self.outputs = [self.__format_arr(arr)]

    def int_output(self, i):
        self.outputs = [i]

    def __str__(self):
        str_in = [str(inp) for inp in self.inputs]
        str_out = [str(out) for out in self.outputs]
        return "(" + self.name + ' ' + ' '.join(str_in) + ') -> ' + ' '.join(str_out)


class LLMExample(Example):
    def __init__(self):
        super(LLMExample, self).__init__()
        self.inputs = []
        self.outputs = []

    def __format_arr(self, arr):
        return '[' + ', '.join([str(x) for x in arr]) + ']'

    def add_array_input(self, arr, nolen=False):
        self.inputs.append(self.__format_arr(arr))

    def add_int_input(self, i):
        self.inputs.append(i)

    def array_output(self, arr, nolen=False):
        self.outputs.append(self.__format_arr(arr))

    def int_output(self, i):
        self.outputs = [i]

    def __str__(self):
        return "Use the set buiding funcion"

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
    elif type == "SketchAdapt":
        return SketchAdapt()
    elif type == "LLM":
        return LLM()
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
    elif type == "SketchAdapt":
        return SketchAdaptExample()
    elif type == "LLM":
        return LLMExample()
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


def randomfloatarray(len):
    arr = []
    for i in range(len):
        arr.append(random.random() * 10.0)

    return arr


def randomintarray(len, min=0, max=10):
    arr = []
    for i in range(len):
        arr.append(random.randint(min, max))

    return arr


def randomstring(length):
    arr = []
    for i in range(length):
        arr.append(random_char())
    return ''.join(arr)

def random_char():
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHJIKLMNOPQRSTUVWXYZ '
    return alphabet[random.randint(0, len(alphabet) - 1)]

def handle_args():
    parser = argparse.ArgumentParser(description="If you have to edit this, it's called when gen_utils is imported")
    parser.add_argument('--no-help', dest='no_help', default=False, action='store_true')

    args = parser.parse_args()
    global NO_HELP_MODE
    NO_HELP_MODE = args.no_help
