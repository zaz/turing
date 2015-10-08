; double a string of 1s  (2n^2 + n + 1 steps)
0 1 0 l 1 ; mark current 1 as 0, move left
1 _ 1 r 2 ; fill 1 in empty cell, move right  
1 1 1 l 1 ; skip 1s moving left
2 0 1 r 0 ; restore currently marked 1, move to the next 1
2 1 1 r 2 ; skip 1s moving right0 1 0 l 1
