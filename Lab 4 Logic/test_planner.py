"""Unit tests for the logical planning agent."""
import unittest
from planner import (
    Action, INITIAL_STATE, GOAL, breadth_first_plan, warehouse_actions
)


class PlannerTests(unittest.TestCase):
    def test_original_problem_finds_valid_plan(self):
        actions = warehouse_actions()
        result = breadth_first_plan(INITIAL_STATE, GOAL, actions)
        self.assertTrue(result["found"])
        self.assertIn("At(Package, C)", result["final_state"])
        self.assertEqual(len(result["states"]), len(result["plan"]) + 1)

        state = frozenset(INITIAL_STATE)
        for action, recorded_successor in zip(result["plan"], result["states"][1:]):
            self.assertTrue(action.is_applicable(state))
            state = action.apply(state)
            self.assertEqual(state, recorded_successor)
        self.assertIn("At(Package, C)", state)

    def test_pickup_removed_means_no_plan(self):
        result = breadth_first_plan(
            INITIAL_STATE, GOAL, warehouse_actions(include_pickup=False)
        )
        self.assertFalse(result["found"])
        self.assertEqual(result["plan"], [])

    def test_robot_at_goal_is_not_package_at_goal(self):
        goal = {"At(Package, C)"}
        result = breadth_first_plan(
            INITIAL_STATE, goal, warehouse_actions()
        )
        self.assertTrue(result["found"])
        self.assertIn("At(Package, C)", result["final_state"])
        self.assertNotEqual(goal, {"At(Robot, C)"})

    def test_action_preconditions_are_checked(self):
        pickup_b = next(
            a for a in warehouse_actions() if a.name == "PickUp(Package, B)"
        )
        initial = frozenset(INITIAL_STATE)
        self.assertFalse(pickup_b.is_applicable(initial))
        with self.assertRaises(ValueError):
            pickup_b.apply(initial)

    def test_effects_remove_and_add_facts(self):
        move_ab = next(
            a for a in warehouse_actions() if a.name == "Move(A, B)"
        )
        state = frozenset(INITIAL_STATE)
        successor = move_ab.apply(state)
        self.assertNotIn("At(Robot, A)", successor)
        self.assertIn("At(Robot, B)", successor)
        self.assertIn("At(Package, A)", successor)

    def test_negative_precondition(self):
        action = Action.make(
            "TestAction",
            positive_preconditions={"ready"},
            negative_preconditions={"blocked"},
            add_effects={"done"},
        )
        self.assertTrue(action.is_applicable(frozenset({"ready"})))
        self.assertFalse(action.is_applicable(frozenset({"ready", "blocked"})))


if __name__ == "__main__":
    unittest.main()
