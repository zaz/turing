; double a string of 1s  (2n^2 + 2n + 2 steps)
0 1 X r 0    ; state 0: replace all ones with the letter X...
0 _ _ l 1    ; ...then proceed to state 1
1 1 1 l 1    ; state 1: find the rightmost X, skipping any ones
1 _ * r halt ; if there are no more Xes, we're done.
1 X 1 r 2    ; otherwise, change the rightmost X back to a one, then go to state 2
2 1 1 r 2    ; state 2: find the first post-sequence blank space, skipping any ones
2 _ 1 l 1    ; add a new one to the end, then continue the process in state 1
