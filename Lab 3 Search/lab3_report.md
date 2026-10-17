# Laboratory Report: Search and A*

**Name:**  
**ID:**  
**Course:** Artificial Intelligence  
**Lab:** Search and A*

> Important: Run the programs yourself and replace the result placeholders below with your actual terminal outputs. The reflection section should accurately describe what you designed, what the LLM suggested, and what you changed or verified.

## 1. Formulation of the search problem

- **States \(S\):** all traversable grid positions, represented by `(row, column)`.
- **Actions \(A\):** Up, Down, Left and Right.
- **Transition \(T\):** an action changes the row or column by one cell, provided the destination is inside the grid and is not an obstacle.
- **Initial state \(s_0\):** the cell marked `S`, at `(1, 1)` in the supplied map (zero-based row and column indices).
- **Goal \(G\):** the cell marked `G`, at `(7, 15)` in the supplied map.
- **Cost \(c\):** every legal move costs 1.

### Questions

**(a) What information is necessary to specify a state?**  
The robot's current row and column are sufficient because the map is fixed and the robot's legal moves depend only on its current cell.

**(b) What makes an action invalid?**  
An action is invalid if it moves outside the grid or into a cell marked `#`.

**(c) Is this deterministic?**  
Yes. Given a current position and a legal action, the next position is uniquely determined.

**(d) What constitutes a solution?**  
A sequence of legal moves that starts at `S` and reaches `G`. With unit movement costs, a shortest solution minimises the number of moves.

## 2. Agent design

The grid is stored as a list of strings. A state is a `(row, column)` tuple. The frontier for A* is a min-heap ordered by \(f(n)=g(n)+h(n)\). The implementation stores each state's best known cost `g_score` and its parent. When a better route to a state is found, its cost, parent and heap entry are updated. Once the goal is popped as the best current frontier entry, following parent pointers reconstructs the path.

The program reports whether a solution was found, the path positions, the action sequence, path length in moves, and states expanded.

## 3. A* implementation

See `astar.py`. The default heuristic is Manhattan distance:

\[
h(n)=|r-r_G|+|c-c_G|
\]

It is appropriate because movement is restricted to horizontal and vertical steps, each costing one. It never overestimates the true remaining cost in this grid.

## 4. Tests

Run:

```bash
python -m unittest -v
```

The test suite covers:
1. the original warehouse;
2. a one-move start/goal case;
3. an inaccessible goal;
4. equality of BFS and A* optimal path lengths;
5. admissible heuristic path lengths;
6. a map with alternative routes.

Record the output and any changes you made:

| Test | Expected behaviour | Actual result |
|---|---|---|
| Original warehouse | A path is found | Passed; path length 40 moves; 63 states expanded |
| Adjacent goal | Path length is 1 | Passed; path length 1 move |
| No solution | Failure is reported; no infinite loop | Passed; no solution found; search terminates |
| Alternative routes | A shortest path is returned for A* with admissible heuristic | Passed; path length 6 moves |

## 5. BFS versus A*

Run:

```bash
python bfs.py
python astar.py
```

Copy your actual measurements:

| Measure | BFS | A* with Manhattan |
|---|---:|---:|
| Solution found | Yes | Yes |
| Path length | 40 moves | 40 moves |
| States expanded | 63 | 63 |

Both BFS and A* with an admissible heuristic should find a shortest path in this unit-cost grid. BFS explores in increasing depth. A* orders the frontier by \(g(n)+h(n)\), using the estimated remaining distance to guide exploration. The number of expanded states depends on the grid and tie-breaking behaviour.

## 6. Heuristic investigation

Run:

```bash
python heuristic_experiments.py
```

Fill in the measurements:

| Heuristic | Solution found | Path length | States expanded |
|---|---|---:|---:|
| Manhattan | Yes | 40 | 63 |
| \(h(n)=0\) | Yes | 40 | 63 |
| Euclidean | Yes | 40 | 63 |
| \(2 \times\) Manhattan | Yes | 40 | 63 |

### Interpretation

- **Manhattan distance:** admissible for four-direction movement with unit costs.
- **Zero heuristic:** \(f(n)=g(n)\), so A* behaves like uniform-cost search; with unit costs this has the same path-length guarantee as BFS.
- **Euclidean distance:** straight-line distance is no greater than the number of horizontal/vertical unit moves, so it is admissible here.
- **Doubled Manhattan:** may overestimate the true remaining cost. It can guide search more aggressively, but standard A* optimality is no longer guaranteed.

Use your own observed expansion counts to discuss how the heuristic changed the search.

## 7. Inspecting A*

| Concept | Where it appears |
|---|---|
| State | `(row, column)` tuples |
| Action | `moves` list in `astar.py` |
| Transition | Adding a move delta and checking `is_open` |
| Goal test | `current == goal` |
| \(g(n)\) | `g_score` and `tentative_g` |
| \(h(n)\) | The selected heuristic function |
| \(f(n)\) | `tentative_g + heuristic(neighbor, goal)` |
| Frontier | `frontier`, a `heapq` min-heap |
| Visited/expanded states | `closed` set |
| Path reconstruction | Following `parent` links from goal to start |

### Questions

**(a) What data structure is used for the A* frontier?**  
A min-heap priority queue.

**(b) How is the next state selected?**  
The heap returns the entry with the smallest \(f(n)=g(n)+h(n)\), ignoring stale entries.

**(c) Where is the heuristic calculated?**  
When a neighbour is added to the frontier, using the selected heuristic function.

**(d) Is \(f(n)=g(n)+h(n)\) explicitly calculated?**  
Yes, in the `f_score` assignment.

**(e) How are repeated explorations limited?**  
The best known cost is stored in `g_score`; stale heap entries and already closed states are skipped.

## 8. Evaluation of the LLM-generated agent

Edit these answers so they accurately reflect your own process.

1. **What was correct immediately?** The suggested implementation represented states as grid coordinates, checked legal moves, used a priority queue and reconstructed a path.
2. **Were bugs or design problems found?** State what your tests actually revealed. Do not claim to have found a bug unless you did.
3. **How were problems discovered?** By running tests with known expected behaviour, including a one-step solution and an unreachable goal.
4. **Unfamiliar terms or structures:** Explain any terms you had to investigate, such as heap, frontier, heuristic, or admissibility.
5. **Did you modify the code?** Describe only changes you actually made.
6. **Most useful tests:** The unreachable-goal test checks termination, while the adjacent-goal test checks a known path length.
7. **Could the program be trusted without testing?** No. Plausible output does not prove correctness for edge cases.
8. **What did implementation teach you?** Describe how the frontier, \(g\), \(h\), \(f\), parent links and test cases work together.

## 9. Final reflection

### 1. Why formulate the search problem first?
Formulating the search problem identifies the states, available actions, transition rules, initial state, goal condition and movement costs. This prevents ambiguity during implementation. For example, if the state representation or the definition of a legal move is wrong, even a correctly implemented A* algorithm may solve the wrong problem. A clear formulation also helps design tests because the expected behaviour can be derived from the specification.

### 2. In what sense is A* informed?
A* is informed because it uses a heuristic \(h(n)\), an estimate of the remaining cost to the goal, in addition to the cost \(g(n)\) already incurred. It prioritises states according to \(f(n)=g(n)+h(n)\). In this warehouse, Manhattan distance uses the robot's row and column differences to estimate how many horizontal and vertical moves remain. The heuristic guides the search toward promising states instead of relying only on the search depth.

### 3. Why does the heuristic matter?
The heuristic influences which states A* expands first. A useful admissible heuristic can reduce unnecessary exploration while preserving an optimal solution. A zero heuristic provides no directional guidance and behaves like uniform-cost search. Manhattan distance is appropriate for four-direction unit-cost movement. A heuristic such as twice Manhattan distance can overestimate the true remaining cost, which may make the search more aggressive but removes the usual guarantee that the returned path is shortest.

### 4. What did the LLM contribute?
The LLM can help translate the search design into Python, suggest a frontier data structure, show how to calculate the priority function, and provide a starting point for test cases and explanations. Its output is a proposal rather than proof of correctness. The engineer still needs to understand the implementation, execute it, compare results with expected behaviour, and document any changes.

### 5. What could go wrong if generated code were accepted without testing?
The code could mishandle boundaries, enter obstacles, fail to recognise an unreachable goal, reconstruct an invalid path, or report incorrect path lengths or expansion counts. A program may work on the supplied map while failing on simpler or unusual cases. Testing known cases, checking that each consecutive path position is a legal move, and comparing A* against BFS help reveal these problems. This is why validation remains the engineer's responsibility.

## 10. LLM prompt used

Example prompt (adapt it to describe your own design and preserve the prompt you actually used in your submission):

> Implement A* search in Python for the supplied warehouse grid. Represent each state as a `(row, column)` tuple. Legal moves are up, down, left and right, each with cost 1; `#` is an obstacle, `S` is the start and `G` is the goal. Use Manhattan distance by default, maintain a min-heap frontier, track the best `g` score and parent of each state, reconstruct the path, and report whether a solution was found, the path, path length in moves, and states expanded. Handle an unreachable goal without an infinite loop. Keep the code simple and explain the main components.

## 11. Conclusion

This laboratory demonstrates how a navigation task can be formulated as a search problem and solved using A*. It also illustrates the difference between an algorithm that produces output and an implementation whose behaviour has been tested. Comparing BFS and different heuristics shows how the frontier's prioritisation affects search behaviour. An LLM can assist with implementation, but the engineer must validate the result.
