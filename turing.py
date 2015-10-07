#!/usr/bin/env python
from collections import defaultdict
from itertools import chain
import re
CONTEXT = 15
BLANK = "_"
TALLY = "1"
MOVE_RIGHT_SYMBOLS = {'r', 'R',  '1', '→', '»'}
MOVE_LEFT_SYMBOLS = {'l', 'L', '-1', '←' '«'}
COMMENT_CHARACTERS = "#;"
COMMENT_MATCHER = "[{0}].*".format(COMMENT_CHARACTERS)
OPTIMIZE = True
ZOOM_LIMIT = 99999

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
    def __init__(self, code="", t=[" "], h=0, s="0"):
        self.s = s  # state
        self.h = h  # position of head
        self.t = defaultdict(self.blank_symbol)
        for n, i in enumerate(t):
            self.t[n] = i
        # Number of positions show when we view the tape:
        self.context = CONTEXT
        # A map of (state, input) -> command_fn
        # Non-existent keys are mapped to "__halt__":
        self.program = defaultdict(self.halt_symbol)
        self.load(code)
        self.steps = 0  # track number of steps performed

    def get_tape(self):
        section = range(self.h - self.context, self.h + self.context)
        output = []
        for n in section:
            output.append(self.t[n])
        return output

    def show_tape(self): return " ".join(self.get_tape())

    def check(self, fields):
        """Check line for errors."""
        # Raise exception if the number of fields is wrong:
        if   len(fields) > 5: raise TooManyFields(len(fields))
        elif len(fields) < 5: raise TooFewFields(len(fields))

    def zoom(self, direction, i, o):
        """Efficiently perform operations that repeatedly move the cursor in a
        particular direction."""
        limit = self.h + (ZOOM_LIMIT * direction)
        if i == o:
            for n in range(self.h, limit, direction):
                if self.t[n] != i: break
        else:
            for n in range(self.h, limit, direction):
                if self.t[n] != i: break
                else: self.t[n] = o
        # 1 zoom step takes ~1/3 of the time of a normal step:
        self.steps += abs(n - self.h) / 3
        self.h = n

    def create_command(self, s0, i, o, d, s1):
        """Generate an efficient Python command from the 3 command fields"""
        if d in MOVE_RIGHT_SYMBOLS:
            # Optimize for the case where neither state nor input changes:
            if OPTIMIZE and s0 == s1: command = lambda: self.zoom(1, i, o)
            else:
                def command():
                    self.t[self.h] = o
                    self.h += 1
                    self.s = s1
        elif d in MOVE_LEFT_SYMBOLS:
            # Optimize for the case where neither state nor input changes:
            if OPTIMIZE and s0 == s1: command = lambda: self.zoom(-1, i, o)
            else:
                def command():
                    self.t[self.h] = o
                    self.h -= 1
                    self.s = s1
        else:
            def command():
                self.t[self.h] = o
                self.s = s1
        return command

    def parse(self, line):
        line = re.sub(COMMENT_MATCHER, "", line)
        fields = re.split("\s+", line.strip())
        if fields == [""]: return None
        self.check(fields)
        s0, i, o, d, s1 = fields
        return {(s0, i): self.create_command(s0, i, o, d, s1)}

    def load(self, code):
        for n, line in enumerate(code.split("\n")):
            try:
                parsed = self.parse(line)
                if parsed: self.program.update(parsed)
            except CodeError as e:
                # Add line number to exception:
                raise type(e)(str(e) + " on line " + str(n)) from None

    def halt_symbol(self): return "__halt__"
    def blank_symbol(self): return BLANK

    def step(self):
        command = self.program[(self.s, self.t[self.h])]
        if command == "__halt__":
            return None
        else:
            command()
            return True

    def run(self, n=1e309, debug=False):
        if debug: print( self.show_tape() )
        while self.steps < n:
            if debug: print( self.show_tape() )
            if not self.step(): break
            self.steps += 1

    def tape(self):
        mystr = ""
        for k in sorted(self.t):
            mystr += self.t[k]
        return mystr.strip("_ ")

    def count(self, tally):
        """Count the number of consecutive tallys on tape, starting at far left"""
        n=0
        for i in self.tape():
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
        machine = Machine(program, inp)
        machine.run(limit_steps)
        if   type(test) is int: output[test] = machine.count(TALLY)
        elif type(test) is str: output[test] = machine.tape()
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
