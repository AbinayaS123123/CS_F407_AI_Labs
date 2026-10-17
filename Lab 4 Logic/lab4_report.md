# Laboratory Report: Logical Reasoning for Planning

**Name:**  
**ID:**  
**Course:** Artificial Intelligence  
**Lab:** Logical Reasoning for Planning

> Run `python planner.py` and `python -m unittest -v` yourself. Update the test-results section with your own terminal output, and make sure reflection answers accurately describe what you understood, accepted, changed and verified.

## 1. Planning problem specification

### Initial state

\[
I=\{At(Robot,A), At(Package,A)\}
\]

### Goal

\[
G=\{At(Package,C)\}
\]

### Actions, preconditions and effects

| Action | Positive preconditions | Negative preconditions | Add effects | Delete effects |
|---|---|---|---|---|
| `Move(A,B)` | `At(Robot,A)` | none | `At(Robot,B)` | `At(Robot,A)` |
| `Move(B,A)` | `At(Robot,B)` | none | `At(Robot,A)` | `At(Robot,B)` |
| `Move(B,C)` | `At(Robot,B)` | none | `At(Robot,C)` | `At(Robot,B)` |
| `Move(C,B)` | `At(Robot,C)` | none | `At(Robot,B)` | `At(Robot,C)` |
| `PickUp(Package,A)` | `At(Robot,A)`, `At(Package,A)` | none | `Holding(Package)` | `At(Package,A)` |
| `PickUp(Package,B)` | `At(Robot,B)`, `At(Package,B)` | none | `Holding(Package)` | `At(Package,B)` |
| `PickUp(Package,C)` | `At(Robot,C)`, `At(Package,C)` | none | `Holding(Package)` | `At(Package,C)` |
| `Drop(Package,A)` | `At(Robot,A)`, `Holding(Package)` | none | `At(Package,A)` | `Holding(Package)` |
| `Drop(Package,B)` | `At(Robot,B)`, `Holding(Package)` | none | `At(Package,B)` | `Holding(Package)` |
| `Drop(Package,C)` | `At(Robot,C)`, `Holding(Package)` | none | `At(Package,C)` | `Holding(Package)` |

The planner represents each state as a set of propositions. An action is applicable when every positive precondition is present and every negative precondition is absent. Applying an action removes its delete effects and adds its add effects.

### Initial applicability

`PickUp(Package,A)` is applicable because both `At(Robot,A)` and `At(Package,A)` are in the initial state. `Drop(Package,C)` is not applicable because the robot is not at C and is not holding the package.

## 2. Manually constructed plan and states

One valid plan is:

1. `PickUp(Package,A)`
2. `Move(A,B)`
3. `Move(B,C)`
4. `Drop(Package,C)`

| State | Facts |
|---|---|
| \(S_0\) | `At(Robot,A)`, `At(Package,A)` |
| \(S_1\) | `At(Robot,A)`, `Holding(Package)` |
| \(S_2\) | `At(Robot,B)`, `Holding(Package)` |
| \(S_3\) | `At(Robot,C)`, `Holding(Package)` |
| \(S_4\) | `At(Robot,C)`, `At(Package,C)` |

The goal is satisfied in \(S_4\) because `At(Package,C)` is true.

## 3. Planner design

See `planner.py`. An `Action` stores its name, positive and negative preconditions, add effects and delete effects. The BFS frontier stores states waiting to be explored. A visited set prevents repeated exploration of the same state. Each queue entry carries the plan and state sequence so the program can print the resulting actions and the state after each action.

## 4. Tests

Run:

```bash
python -m unittest -v
```

The tests check:
- the original problem has a valid plan;
- removing all pickup actions makes the delivery goal impossible;
- reaching a robot-location goal is not confused with delivering the package;
- actions with unsatisfied preconditions cannot be applied;
- effects remove and add the expected facts;
- negative preconditions are respected.

Record your actual output:

| Test | Expected behaviour | Actual result |
|---|---|---|
| Solvable problem | Plan reaches `At(Package,C)` | Fill in after running |
| Impossible problem | Prints `No plan found` | Fill in after running |
| Irrelevant action | Robot at C alone does not mean package at C | Fill in after running |

## 5. Logic and search

**Logical reasoning** checks whether action preconditions hold and computes the successor state from action effects. **Search** explores alternative sequences of applicable actions. The combined process is:

Current state → check action preconditions → if applicable, apply effects and generate successor state → search over alternatives → test the goal.

If the preconditions fail, the action is not applied. If the goal is reached, the plan is returned; if the frontier becomes empty, no plan exists in the explored state space.

## 6. Optional Prolog extension

The facts `connected(a,b)`, `connected(b,a)`, `connected(b,c)`, and `connected(c,b)` describe direct connections. The rule `can_move(X,Y) :- connected(X,Y).` says that a direct connection implies a legal move.

Expected queries:
- `can_move(a,b).` — succeeds.
- `can_move(a,c).` — fails because there is no direct `connected(a,c)` fact.
- `valid_move(a,b).` — succeeds.
- `valid_move(b,c).` — succeeds.
- `valid_move(a,c).` — fails.
- `reduce_speed.` — succeeds because `wet_road` is a fact, `slippery` follows from it, and `reduce_speed` follows from `slippery`.

## 7. Reflection questions

### 1. Why specify preconditions and effects before asking an LLM to write the planner?
They provide a precise description of when actions can be performed and how the world changes. Without this specification, the generated program might permit impossible actions or change facts incorrectly. A clear model also makes it easier to test the planner against expected behaviour.

### 2. Give an error that could occur if preconditions were not checked.
The planner might execute `Drop(Package,C)` while the robot is at A and is not holding the package. This would create the fact `At(Package,C)` without a valid delivery.

### 3. Why is a plan that looks reasonable not necessarily valid?
Every action must be applicable in the state where it occurs, and its effects must produce the next state. A sequence can sound plausible but attempt to pick up a package at a location where it is not present, or drop it when the robot is not holding it. Validity requires checking each transition and confirming the final goal.

### 4. What did the LLM contribute?
An LLM can help translate the formal action model into Python, suggest BFS for finding a short plan, and scaffold tests and explanations. The generated implementation still needs to be run and checked against the problem specification.

### 5. What did you have to verify independently?
The action preconditions and effects, that each transition changes only the appropriate facts, that the returned plan reaches the package-delivery goal, and that impossible cases terminate with no plan. The unit tests help verify these behaviours.

### 6. Where is logical reasoning used?
It is used when the planner checks whether an action's preconditions are satisfied and when it applies the action's effects to produce a successor state.

### 7. How is planning related to search algorithms from the previous module?
Planning can be treated as search over states. Each applicable action generates a successor state, and a plan is a path from the initial state to a state satisfying the goal. BFS explores these states in increasing number of actions and therefore finds a plan with the fewest actions when all actions have equal cost.

## 8. LLM prompt used

Example prompt (adapt it to your own design and save the actual prompt you used):

> Implement a simple planning agent in Python. Represent a state as a set of logical propositions. Each action should have a name, positive preconditions, negative preconditions, positive effects and negative effects. An action is applicable only if all positive preconditions are present and all negative preconditions are absent. Applying an action removes its negative effects and adds its positive effects. Use breadth-first search to find a sequence of actions that reaches a goal. Detect when no plan exists, print the action sequence and print the states reached after each action. Use the A-B-C warehouse problem with initial facts `At(Robot,A)` and `At(Package,A)`, and goal `At(Package,C)`.

## 9. Conclusion

The lab combines logical reasoning with search. Preconditions and effects specify which actions are possible and how the state changes, while BFS searches for an action sequence that reaches the goal. Testing both solvable and impossible cases helps establish whether the implementation follows the specification. The optional Prolog extension demonstrates how a separate rule-based system can independently check claims about possible moves.
