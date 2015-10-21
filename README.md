### Usage

    import turing

    machine = turing.Machine(program, tape, h=0, s="0")
    machine.run(steps=1e309, debug=False)
    machine.count(tally="1")

Where `program` is a Turing machine program as below, `tape` is the initial state of the tape (e.g. if you want to represent 17 in unary, use `tape = "1" * 17`), `h` is the initial position of the head, and `s` is the initial state.

`steps` is the maximum number of steps that will be run (default is infinity). Multiple consecutive steps with the same parameters (same state and input) are called *zoom steps*, are more efficient, and count for 1/3 of a step.

`machine.count()` is optional and will count the number of consecutive `1`s (or other specified mark) starting from the beginning of the tape. This is useful for working with unary.

`0`, `"0"`, `1e309`, `False`, and `"1"` are default values for arguments that can be omitted. If you create a machine without specifying program or tape, empty ones will be created.

### Example: Doubling program

    import turing

    program = """
    0 1 0 l 1  ; mark current 1 as 0, move left
    1 _ 1 r 2  ; fill 1 in empty cell, move right
    1 1 1 l 1  ; skip 1s moving left
    2 0 1 r 0  ; restore currently marked 1, move to the next 1
    2 1 1 r 2  ; skip 1s moving right
    """
    tape = "1111"

    turing.OPTIMIZE = False  # to see the full, pretty debug output
    machine = turing.Machine(program, tape)
    machine.run(debug=True)

Output:

    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 0 1 1 1 _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 0 1 1 1 _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 0 1 1 _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 0 1 1 _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 0 1 1 _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 0 1 1 _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 0 1 1 _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 0 1 1 _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 _ _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 0 1 _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 0 1 _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 0 1 _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 0 1 _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 0 1 _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 0 1 _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 0 1 _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 0 1 _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 0 1 _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 0 1 _ _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 1 _ _ _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 0 _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _ 1 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ 1 1 1 1 1 1 1 0 _ _ _ _ _ _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ 1 1 1 1 1 1 1 1 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

Result: **8** (`11111111`)

*The amount of context (number of cells shown on either side of head) shown in the debug output defaults to 15 but can be changed with e.g: `machine.context = 20`*
