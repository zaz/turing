#!/usr/bin/env python
from collections import defaultdict
from itertools import chain
import re
CONTEXT = 15
COMMENT_CHARACTERS = "#"
BLANK = "_"
TALLY = "1"

class CodeError(Exception):
    """There's an error in the Turing machine's code."""
    pass
class FieldsError(CodeError):
    """The line is non-empty, but has the wrong number of fields."""
    pass
class TooManyFields(FieldsError): pass
class TooFewFields(FieldsError): pass
class InvalidDirection(CodeError): pass


def get_last_padded(coll, n, pad=None):
    last = coll[-n:]
    padding = [pad] * (n-len(coll))
    return padding + last


class Machine:
    """A Turing machine"""
    def __init__(self, code="", l=[], r=[" "], s="0"):
        self.s = s  # state
        # Tape to the left of head. Last item is just to the left of head:
        self.l = [str(i) for i in l]
        # Tape to the right of head in reverse (last item is head):
        self.r = [str(i) for i in reversed(r)]
        # Number of positions show when we view the tape:
        self.context = 15
        # A map of (state, item) -> (new_item, movement_fn, new_state)
        # Non-existent keys are mapped to "__halt__":
        self.program = defaultdict(self.halt_symbol)
        self.load(code)

    def get_tape(self):
        return get_last_padded(self.l, self.context, " ") \
                + list(reversed(get_last_padded(self.r, self.context + 1, " ")))

    def show_tape(self): return " ".join(self.get_tape())

    def check(self, fields):
        """Check line for errors."""
        # Raise exception if the number of fields is wrong:
        if   len(fields) > 5: raise TooManyFields(len(fields))
        elif len(fields) < 5: raise TooFewFields(len(fields))

        # Raise exception if a field in invalid:
        if fields[3] not in {'r', 'R', '1', 'l', 'L', '-1', 'x', 'X', '0'}:
            raise InvalidDirection(fields[3])

    def create_command(self, o, d, s1):
        """Generate an efficient Python command from the 3 command fields"""
        if   d in {'r', 'R',  '1'}:
            def command():
                # Optimize for the case where neither state nor input changes:
                if self.s == s1:
                    orig_i = self.r[-1]
                    while self.r[-1] == orig_i:
                        self.l.append(o)
                        self.r.pop()
                else:
                    self.l.append(o)
                    self.r.pop()
                    self.s = s1
                if len(self.r) < 1: self.r.append(BLANK)  # r should never be []
        elif d in {'l', 'L', '-1'}:
            def command():
                # Optimize for the case where neither state nor input changes:
                if self.s == s1:
                    orig_i = self.r[-1]
                    while self.r[-1] == orig_i:
                        self.r[-1] = o
                        try: self.r.append(self.l.pop())
                        except IndexError: self.r.append(BLANK)
                        self.s = s1
                else:
                    self.r[-1] = o
                    try: self.r.append(self.l.pop())
                    except IndexError: self.r.append(BLANK)
                    self.s = s1
        elif d in {'x', 'X',  '0'}:
            def command():
                self.r[-1] = o
                self.s = s1
        return command

    def parse(self, line):
        fields = re.split("\s+", line.strip())
        if fields == [""]: return None
        if fields[0][0] in COMMENT_CHARACTERS: return None
        self.check(fields)
        s0, i, o, d, s1 = fields
        return {(s0, i): self.create_command(o, d, s1)}

    def load(self, code):
        for n, line in enumerate(code.split("\n")):
            try:
                parsed = self.parse(line)
                if parsed: self.program.update(parsed)
            except CodeError as e:
                # Add line number to exception:
                raise type(e)(str(e) + " on line " + str(n)) from None

    def halt_symbol(self): return "__halt__"

    def step(self):
        command = self.program[(self.s, self.r[-1])]
        if command == "__halt__":
            return None
        else:
            command()
            return True

    def run(self, n=-1, debug=False):
        if debug: print( self.show_tape() )
        if 0 > n:
            while self.step():
                if debug: print( self.show_tape() )
        else:
            for i in range(n):
                if debug: print( self.show_tape() )
                if not self.step(): break

    def tape(self):
        return chain(self.l, reversed(self.r))

    def tape_str(self):
        tape = "".join([str(i) for i in self.tape()])
        return tape.strip("_ ")

    def count(self, tally):
        """Count the number of consecutive tallys on tape, starting at far left"""
        coll = self.tape()
        n=0
        for i in coll:
            if i == tally: n+=1
            if i != tally: break
        return n


def test(program, test_cases, limit_steps=-1):
    """Map each item of test_cases to its output when program is run on it.
    If a dict is passed, its values will be discarded and the keys mapped as
    above, so a program can be tested for correctness with:

        test_dict == test(program, test_dict)
    """
    output = {}
    for test in test_cases:
        # If the input in an integer, convert it into tally:
        if   type(test) is int: inp = "".join([TALLY] * test)
        elif type(test) is str: inp = test
        else: raise TypeError("Test input type should be int or str")
        machine = Machine(program, [], inp)
        machine.run(limit_steps)
        if   type(test) is int: output[test] = machine.count(TALLY)
        elif type(test) is str: output[test] = machine.tape_str()
    return output


if __name__ == "__main__":
    import sys

    # double a string of 1s:
    program = """
    0 1 0 l 1
    1 _ 1 r 2
    1 1 1 l 1
    2 0 1 r 0
    2 1 1 r 2
    """

    args = [int(i) for i in sys.argv[1:]]
    print( test(program, set(args)) )



# Potential test cases:
#
# - blank lines in program
# - commented lines in program
# - simple programs: doubling, to_binary
# - r, R, 1; l, L, -1; x, X, 0
