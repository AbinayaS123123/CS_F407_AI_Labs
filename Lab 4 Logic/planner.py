"""A small STRIPS-style planner using breadth-first search.

States are frozensets of propositions (strings). Actions specify positive and
negative preconditions and positive and negative effects.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Action:
    name: str
    positive_preconditions: frozenset[str]
    negative_preconditions: frozenset[str]
    add_effects: frozenset[str]
    delete_effects: frozenset[str]

    @classmethod
    def make(
        cls,
        name: str,
        positive_preconditions: Iterable[str] = (),
        negative_preconditions: Iterable[str] = (),
        add_effects: Iterable[str] = (),
        delete_effects: Iterable[str] = (),
    ) -> "Action":
        return cls(
            name,
            frozenset(positive_preconditions),
            frozenset(negative_preconditions),
            frozenset(add_effects),
            frozenset(delete_effects),
        )

    def is_applicable(self, state: frozenset[str]) -> bool:
        return (
            self.positive_preconditions <= state
            and self.negative_preconditions.isdisjoint(state)
        )

    def apply(self, state: frozenset[str]) -> frozenset[str]:
        if not self.is_applicable(state):
            raise ValueError(f"Action {self.name!r} is not applicable.")
        return frozenset((state - self.delete_effects) | self.add_effects)


def warehouse_actions(include_pickup: bool = True) -> list[Action]:
    """Create the actions for the A-B-C warehouse described in the lab."""
    actions = [
        Action.make(
            "Move(A, B)",
            positive_preconditions={"At(Robot, A)"},
            add_effects={"At(Robot, B)"},
            delete_effects={"At(Robot, A)"},
        ),
        Action.make(
            "Move(B, A)",
            positive_preconditions={"At(Robot, B)"},
            add_effects={"At(Robot, A)"},
            delete_effects={"At(Robot, B)"},
        ),
        Action.make(
            "Move(B, C)",
            positive_preconditions={"At(Robot, B)"},
            add_effects={"At(Robot, C)"},
            delete_effects={"At(Robot, B)"},
        ),
        Action.make(
            "Move(C, B)",
            positive_preconditions={"At(Robot, C)"},
            add_effects={"At(Robot, B)"},
            delete_effects={"At(Robot, C)"},
        ),
        Action.make(
            "Drop(Package, A)",
            positive_preconditions={"At(Robot, A)", "Holding(Package)"},
            add_effects={"At(Package, A)"},
            delete_effects={"Holding(Package)"},
        ),
        Action.make(
            "Drop(Package, B)",
            positive_preconditions={"At(Robot, B)", "Holding(Package)"},
            add_effects={"At(Package, B)"},
            delete_effects={"Holding(Package)"},
        ),
        Action.make(
            "Drop(Package, C)",
            positive_preconditions={"At(Robot, C)", "Holding(Package)"},
            add_effects={"At(Package, C)"},
            delete_effects={"Holding(Package)"},
        ),
    ]

    if include_pickup:
        actions.extend([
            Action.make(
                "PickUp(Package, A)",
                positive_preconditions={"At(Robot, A)", "At(Package, A)"},
                add_effects={"Holding(Package)"},
                delete_effects={"At(Package, A)"},
            ),
            Action.make(
                "PickUp(Package, B)",
                positive_preconditions={"At(Robot, B)", "At(Package, B)"},
                add_effects={"Holding(Package)"},
                delete_effects={"At(Package, B)"},
            ),
            Action.make(
                "PickUp(Package, C)",
                positive_preconditions={"At(Robot, C)", "At(Package, C)"},
                add_effects={"Holding(Package)"},
                delete_effects={"At(Package, C)"},
            ),
        ])
    return actions


def breadth_first_plan(
    initial_state: Iterable[str],
    goal: Iterable[str],
    actions: Iterable[Action],
) -> dict:
    """Find a shortest action sequence (fewest actions) that reaches the goal."""
    start = frozenset(initial_state)
    goal_set = frozenset(goal)
    action_list = list(actions)

    # Queue entries contain (state, action sequence, state sequence).
    frontier = deque([(start, [], [start])])
    visited = {start}
    expanded = 0

    while frontier:
        state, plan, states = frontier.popleft()
        if goal_set <= state:
            return {
                "found": True,
                "plan": plan,
                "states": states,
                "states_expanded": expanded,
                "final_state": state,
            }

        expanded += 1
        for action in action_list:
            if not action.is_applicable(state):
                continue
            successor = action.apply(state)
            if successor in visited:
                continue
            visited.add(successor)
            frontier.append((successor, plan + [action], states + [successor]))

    return {
        "found": False,
        "plan": [],
        "states": [],
        "states_expanded": expanded,
        "final_state": None,
    }


def format_state(state: frozenset[str]) -> str:
    return "{ " + ", ".join(sorted(state)) + " }"


def print_result(result: dict) -> None:
    if not result["found"]:
        print("No plan found")
        print(f"States expanded: {result['states_expanded']}")
        return

    print("Plan found:")
    for index, action in enumerate(result["plan"], start=1):
        print(f"{index}. {action.name}")
    print(f"Plan length: {len(result['plan'])} actions")
    print(f"States expanded: {result['states_expanded']}")
    print("\nState transitions:")
    for index, state in enumerate(result["states"]):
        print(f"S{index}: {format_state(state)}")


INITIAL_STATE = {"At(Robot, A)", "At(Package, A)"}
GOAL = {"At(Package, C)"}


def main() -> None:
    print("=== Original warehouse problem ===")
    result = breadth_first_plan(INITIAL_STATE, GOAL, warehouse_actions())
    print_result(result)

    print("\n=== Impossible problem (PickUp actions removed) ===")
    impossible = breadth_first_plan(
        INITIAL_STATE, GOAL, warehouse_actions(include_pickup=False)
    )
    print_result(impossible)

    print("\n=== Irrelevant action example ===")
    # Robot movement alone does not satisfy the package-delivery goal.
    robot_only_goal = {"At(Robot, C)"}
    robot_result = breadth_first_plan(
        INITIAL_STATE, robot_only_goal, warehouse_actions()
    )
    print("Goal is At(Robot, C), not At(Package, C):")
    print_result(robot_result)


if __name__ == "__main__":
    main()
