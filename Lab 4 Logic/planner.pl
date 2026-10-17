% Optional Prolog extension from the Lab 4 handout.
% Run with SWI-Prolog: swipl -s planner.pl
% At the prompt, try:
% ?- can_move(a,b).
% ?- can_move(a,c).
% ?- valid_move(a,b).
% ?- valid_move(b,c).
% ?- valid_move(a,c).
% ?- reduce_speed.

connected(a,b).
connected(b,a).
connected(b,c).
connected(c,b).

can_move(X,Y) :-
    connected(X,Y).

valid_move(X,Y) :-
    connected(X,Y).

wet_road.

slippery :-
    wet_road.

reduce_speed :-
    slippery.
