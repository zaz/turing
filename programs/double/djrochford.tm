0 1 x r 1	; This puts an ‘x’ at the front of the input
1 1 1 r 1	; This moves along the input...
1 _ y l 2	; ...until you get to the end, and leave a ‘y’ afterwards
2 1 1 l 2	; This heads back left, skipping any ‘1’s...
2 y y l 2	; ...and any ‘y’s…
2 x 1 r 3	; ...until you hit an ‘x’, which you replace with a ‘1’. You then move to the right one place...
3 y 1 * halt	; ...to check if there is a ‘y’. If so, you replace it with a ‘1’ then halt.
3 1 x r 4	; If not, you replace the ‘1’ with an x...
4 1 1 r 4	; ...and move back to the right, skipping ‘1’s...
4 y y r 4	; ...and ‘y’s…
4 _ 1 l 2	; ...until you get to the end, and put a ‘1’ after it. You then head back left...
