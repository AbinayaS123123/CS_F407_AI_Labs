"""A* search for the warehouse navigation lab."""
from __future__ import annotations

import heapq
import itertools
import math
from typing import Callable

Grid = list[str]
Position = tuple[int, int]
Heuristic = Callable[[Position, Position], float]

WAREHOUSE: Grid = [
    "#################",
    "#S....#.........#",
    "#.###.#.#######.#",
    "#...#.#.......#.#",
    "###.#.#######.#.#",
    "#...#.........#.#",
    "#.###########.#.#",
    "#.............#G#",
    "#################",
]


def parse_grid(grid: Grid) -> tuple[Position, Position]:
    """Return (start, goal), validating a rectangular grid with one S and G."""
    if not grid or not grid[0]:
        raise ValueError("Grid must not be empty.")
    width = len(grid[0])
    if any(len(row) != width for row in grid):
        raise ValueError("Grid must be rectangular.")

    starts = [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == "S"]
    goals = [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch == "G"]
    if len(starts) != 1 or len(goals) != 1:
        raise ValueError("Grid must contain exactly one S and exactly one G.")
    return starts[0], goals[0]


def manhattan(a: Position, b: Position) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def zero_heuristic(a: Position, b: Position) -> float:
    return 0.0


def euclidean(a: Position, b: Position) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def doubled_manhattan(a: Position, b: Position) -> float:
    return 2 * manhattan(a, b)


def astar(
    grid: Grid,
    heuristic: Heuristic = manhattan,
) -> dict:
    """Return search outcome, shortest path when guaranteed, and expansion count.

    Positions are (row, column). Each legal move costs 1.
    With an admissible heuristic (such as Manhattan, Euclidean, or zero),
    the returned path is optimal. Doubled Manhattan is included for experiments
    but is not generally admissible, so optimality is not guaranteed.
    """
    start, goal = parse_grid(grid)
    rows, cols = len(grid), len(grid[0])

    def is_open(pos: Position) -> bool:
        r, c = pos
        return 0 <= r < rows and 0 <= c < cols and grid[r][c] != "#"

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    action_names = {(-1, 0): "Up", (1, 0): "Down", (0, -1): "Left", (0, 1): "Right"}

    frontier = []
    counter = itertools.count()
    g_score = {start: 0}
    parent: dict[Position, Position | None] = {start: None}
    heapq.heappush(frontier, (heuristic(start, goal), next(counter), 0, start))
    closed: set[Position] = set()
    expanded = 0

    while frontier:
        _, _, queued_g, current = heapq.heappop(frontier)

        # Ignore outdated heap entries and states already expanded.
        if queued_g != g_score.get(current, float("inf")) or current in closed:
            continue

        if current == goal:
            path = []
            cursor: Position | None = goal
            while cursor is not None:
                path.append(cursor)
                cursor = parent[cursor]
            path.reverse()
            actions = []
            for previous, nxt in zip(path, path[1:]):
                delta = (nxt[0] - previous[0], nxt[1] - previous[1])
                actions.append(action_names[delta])
            return {
                "found": True,
                "path": path,
                "actions": actions,
                "path_length": len(path) - 1,
                "states_expanded": expanded,
            }

        closed.add(current)
        expanded += 1

        for dr, dc in moves:
            neighbor = (current[0] + dr, current[1] + dc)
            if not is_open(neighbor) or neighbor in closed:
                continue
            tentative_g = g_score[current] + 1
            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(frontier, (f_score, next(counter), tentative_g, neighbor))

    return {
        "found": False,
        "path": [],
        "actions": [],
        "path_length": None,
        "states_expanded": expanded,
    }


def display_result(name: str, result: dict) -> None:
    print(f"=== {name} ===")
    print(f"Solution found: {result['found']}")
    print(f"Path: {result['path']}")
    print(f"Actions: {result['actions']}")
    print(f"Path length: {result['path_length']}")
    print(f"States expanded: {result['states_expanded']}")
    print()


def main() -> None:
    display_result("A* (Manhattan heuristic)", astar(WAREHOUSE))


if __name__ == "__main__":
    main()
