"""Breadth-first search baseline for the warehouse navigation lab."""
from collections import deque
from astar import Grid, Position, WAREHOUSE, parse_grid


def bfs(grid: Grid) -> dict:
    start, goal = parse_grid(grid)
    rows, cols = len(grid), len(grid[0])
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    action_names = {(-1, 0): "Up", (1, 0): "Down", (0, -1): "Left", (0, 1): "Right"}

    frontier = deque([start])
    parent: dict[Position, Position | None] = {start: None}
    expanded = 0

    while frontier:
        current = frontier.popleft()
        if current == goal:
            path = []
            cursor: Position | None = goal
            while cursor is not None:
                path.append(cursor)
                cursor = parent[cursor]
            path.reverse()
            actions = [
                action_names[(b[0] - a[0], b[1] - a[1])]
                for a, b in zip(path, path[1:])
            ]
            return {
                "found": True,
                "path": path,
                "actions": actions,
                "path_length": len(path) - 1,
                "states_expanded": expanded,
            }

        expanded += 1
        for dr, dc in moves:
            neighbor = (current[0] + dr, current[1] + dc)
            r, c = neighbor
            if (
                0 <= r < rows
                and 0 <= c < cols
                and grid[r][c] != "#"
                and neighbor not in parent
            ):
                parent[neighbor] = current
                frontier.append(neighbor)

    return {
        "found": False,
        "path": [],
        "actions": [],
        "path_length": None,
        "states_expanded": expanded,
    }


if __name__ == "__main__":
    from astar import display_result
    display_result("BFS", bfs(WAREHOUSE))
