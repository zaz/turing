0 1 1 r 1     ; go right
1 * * r 1     ; keep going right
1 1 - l 2     ;   if 1: change to -, go left
1 _ _ l 4     ;   if _: cleanup
2 - - l 2     ; keep going left
2 _ 1 r 3     ;   if _: change to 1, go right
2 0 1 r 3     ;   if 0: change to 1, go right
2 1 0 l 2     ;   if 1: change to 0, keep going left
3 * * r 3     ; keep going right
3 - - r 1     ;   if -: keep going for right
; cleanup:
4 - _ l 4     ; change all - to _
4 * * * halt  ; halt
