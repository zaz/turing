#!/usr/bin/env python
import pytest
import turing
from os import listdir, path
PROGRAM_PATH = "programs"
LIMIT = 999999

# TODO: Allow things such as blanks and 0s to be interchangeable
tests = {
    "2-1s": { "": "11" },
    "double": { 0: 0,  1: 2,  18: 36,  7: 14,  6: 12,  400: 800 },
    "double-with-0": { "": "",  "1": "1_1",  "1"*18: "1"*18+"_"+"1"*18,
        "1"*7: "1"*7+"_"+"1"*7,  "1"*6: "1"*6+"_"+"1"*6 },
    "switch": { "": "",  "1": "0",  "0": "1",  "01": "10",  "10": "01",
        "11": "00",  "1010": "0101",  "111010111": "000101000"},
    "halt-iff-0": { "0": "0",  "1": turing.TooManySteps },
    "unary-to-binary": { "": "",  "1": "1",  "11": "10",  "111": "11",
        "1111": "100",  "11111": "101",  "1"*19: "10011" }
}

def is_exception(obj):
    return hasattr(obj, "__call__") and isinstance(obj(), Exception)

def run_on(program, test_cases, limit_steps=LIMIT):
    """Map each item of test_cases to its output when program is run on it.
    Will return the same dict if every test passes.
    """
    assert type(test_cases) is dict
    output = {}
    for test in test_cases:
        expected = test_cases[test]
        # If the input in an integer, convert it into tally:
        if   type(test) is int: inp = "".join([turing.TALLY] * test)
        elif type(test) is str: inp = test
        else: raise TypeError("Test input type should be int or str")
        machine = turing.Machine(program, inp)
        if is_exception(expected):
            with pytest.raises(expected) as e:
                machine.run(limit_steps)
            output[test] = expected
            continue
        else:
            machine.run(limit_steps)
        if   type(test) is int: output[test] = machine.count(turing.TALLY)
        elif type(test) is str: output[test] = machine.tape()
    return output

def debug(program, limit_steps=LIMIT):
    machine = turing.Machine(program, inp)
    machine.run(limit_steps, debug=True)

def get_path(test_name, filename=""):
    return path.join(PROGRAM_PATH, test_name, filename)

def get_code(filepath):
    with open(filepath, "r") as f:
        return f.read()

def get_programs_for(test_name):
    for filename in listdir(get_path(test_name)):
        if path.isfile(get_path(test_name, filename)): yield filename

def list_all():
    for test_name in tests:
        for filename in get_programs_for(test_name):
            yield (test_name, filename)

@pytest.mark.parametrize("test_name,filename", list_all())
def test_program(test_name, filename):
    filepath = get_path(test_name, filename)
    code = get_code(filepath)
    print(code)
    inp = tests[test_name]
    output = run_on(code, inp)
    assert inp == output
