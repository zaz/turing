#!/usr/bin/env python
from collections import defaultdict
import re
CONTEXT = 15
COMMENT_CHARACTERS = "#"
BLANK = "_"

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
    def __init__(self, code="", l=[], r=[], s="0"):
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

    # Allow us to use h to refer to the head position (last item in r)
    @property
    def h(self):
        if len(self.r) > 0: return self.r[-1]
        else: return BLANK

    @h.setter
    def h(self, v):
        if len(self.r) > 0: self.r[-1] = v
        else: self.r.append(v)

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

    def parse(self, line):
        fields = re.split("\s+", line.strip())
        if fields == [""]: return None
        if fields[0][0] in COMMENT_CHARACTERS: return None
        self.check(fields)
        s0, i, o, d, s1 = fields
        if   d in {'r', 'R',  '1'}: m = self.move_r
        elif d in {'l', 'L', '-1'}: m = self.move_l
        elif d in {'x', 'X',  '0'}: m = self.move_x
        return {(s0, i): (o, m, s1)}

    def load(self, code):
        for n, line in enumerate(code.split("\n")):
            try:
                parsed = self.parse(line)
                if parsed: self.program.update(parsed)
            except CodeError as e:
                # Add line number to exception:
                raise type(e)(str(e) + " on line " + str(n)) from None

    def halt_symbol(self): return "__halt__"

    # Move head: right, left, nowhere
    def move_r(self):
        if len(self.r) > 0: self.l.append(self.r.pop())
        else:               self.l.append(BLANK)
    def move_l(self):
        if len(self.l) > 0: self.r.append(self.l.pop())
        else:               self.r.append(BLANK)
    def move_x(): pass

    def step(self):
        action = self.program[(self.s, self.h)]
        if action == "__halt__":
            return None
        else:
            self.h, m, self.s = action
            m()
            return (self.s, m)

    def run(self, n=-1):
        if 0 > n:
            while self.step(): pass
        else:
            for i in range(n):
                if not self.step(): break



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

    n = int(sys.argv[1])
    machine = Machine(program, [], [1] * n)
    machine.run()



# Potential test cases:
#
# - blank lines in program
# - commented lines in program
# - simple programs: doubling, to_binary
# - r, R, 1; l, L, -1; x, X, 0
