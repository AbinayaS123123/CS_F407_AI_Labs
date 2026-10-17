"""Unit tests for A* and BFS."""
import unittest
from astar import WAREHOUSE, astar, manhattan, zero_heuristic, euclidean
from bfs import bfs


class SearchTests(unittest.TestCase):
    def test_original_warehouse_has_solution(self):
        result = astar(WAREHOUSE)
        self.assertTrue(result["found"])
        self.assertEqual(result["path_length"], len(result["actions"]))
        self.assertEqual(result["path"][0], (1, 1))
        self.assertEqual(result["path"][-1], (7, 15))

    def test_adjacent_goal_one_step(self):
        grid = ["#####", "#SG##", "#####"]
        result = astar(grid)
        self.assertTrue(result["found"])
        self.assertEqual(result["path_length"], 1)
        self.assertEqual(result["actions"], ["Right"])

    def test_unreachable_goal(self):
        grid = [
            "#######",
            "#S....#",
            "###.###",
            "#...#G#",
            "#######",
        ]
        result = astar(grid)
        self.assertFalse(result["found"])
        self.assertIsNone(result["path_length"])

    def test_bfs_and_astar_same_optimal_length(self):
        a_result = astar(WAREHOUSE)
        b_result = bfs(WAREHOUSE)
        self.assertTrue(a_result["found"])
        self.assertTrue(b_result["found"])
        self.assertEqual(a_result["path_length"], b_result["path_length"])

    def test_admissible_heuristics_match_bfs_length(self):
        baseline = bfs(WAREHOUSE)["path_length"]
        for heuristic in (manhattan, zero_heuristic, euclidean):
            with self.subTest(heuristic=heuristic.__name__):
                self.assertEqual(astar(WAREHOUSE, heuristic)["path_length"], baseline)

    def test_alternative_routes(self):
        grid = [
            "#######",
            "#S....#",
            "#.#.#.#",
            "#....G#",
            "#######",
        ]
        result = astar(grid)
        self.assertTrue(result["found"])
        self.assertEqual(result["path_length"], 6)


if __name__ == "__main__":
    unittest.main()
