# Lab 4 — Logical Reasoning for Planning

A small STRIPS-style planning agent for the A-B-C warehouse scenario in the lab handout.

## Files

- `planner.py` — action representation, precondition checking, state transitions, BFS planning, and printed state trace.
- `test_planner.py` — unit tests for solvable/impossible cases, preconditions, effects, and the goal distinction.
- `planner.pl` — optional Prolog logical verifier.
- `lab4_report.md` — report template and explanations.

## Requirements

Python 3.10+ recommended. The main Python program uses only the standard library.
Prolog is optional and requires SWI-Prolog if you want to run the extension.

## Run the Python planner

```bash
python planner.py
python -m unittest -v
```

## Run the optional Prolog extension

If SWI-Prolog is installed:

```bash
swipl -s planner.pl
```

At the Prolog prompt, enter queries such as:

```prolog
can_move(a,b).
can_move(a,c).
valid_move(a,b).
valid_move(b,c).
valid_move(a,c).
reduce_speed.
```

Type `halt.` to exit.

## Model assumptions

- The warehouse has locations A, B, and C, connected only A-B and B-C in both directions.
- The initial state is `At(Robot, A)` and `At(Package, A)`.
- The goal is `At(Package, C)`.
- Each move, pickup, and drop is a unit-cost action; BFS returns a plan with the fewest actions.
- Facts not present in a state are treated as false for negative preconditions.
- The planner checks that the action's positive preconditions are all present and its negative preconditions are absent.
