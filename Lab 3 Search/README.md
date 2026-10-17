# Lab 3 — Search and A*

Python implementation for the warehouse robot navigation exercise.

## Files

- `astar.py`: A* with Manhattan distance by default; also contains zero, Euclidean, and doubled-Manhattan heuristics.
- `bfs.py`: Breadth-first search baseline.
- `heuristic_experiments.py`: compares the four heuristic choices.
- `test_search.py`: unit tests for the original map and edge cases.
- `lab3_report.md`: report template and worked explanations.

## Requirements

Python 3.10+ is recommended. No third-party packages are needed.

## Run

From this folder:

```bash
python astar.py
python bfs.py
python heuristic_experiments.py
python -m unittest -v
```

## Notes

- Positions are represented as `(row, column)`.
- A move costs 1; only up/down/left/right are allowed.
- `path_length` counts moves, not the number of positions in the path.
- `states_expanded` counts states removed from the frontier and processed, excluding the goal.
- Manhattan, Euclidean and zero heuristics are admissible for this four-direction, unit-cost grid, so A* returns an optimal path with this implementation.
- `2 × Manhattan` can overestimate the remaining cost; it is included for the lab's experiment, and optimality is not guaranteed.
- Record your own terminal outputs in the report. Expansion counts can depend on tie-breaking and on the exact counting convention.
