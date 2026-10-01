from collections import deque


# ---------------------------------------------------------
# Warehouse Navigation Problem
# ---------------------------------------------------------
# This program implements a goal-based agent that finds a
# collision-free path from S (Start) to G (Goal).
#
# Search Algorithm: Breadth-First Search (BFS)
#
# BFS is appropriate because:
# 1. The warehouse is represented as a grid.
# 2. The agent can move Up, Down, Left, or Right.
# 3. Every move has the same cost (1 move).
# 4. BFS finds the shortest path in terms of number of moves.
# ---------------------------------------------------------


# The warehouse environment
warehouse = [
    "#####################",
    "#S....#............G#",
    "#.##....##########..#",
    "#....##.............#",
    "#.######.###.#.###..#",
    "#........#..........#",
    "#####################"
]


# ---------------------------------------------------------
# Find the starting position (S) and goal position (G)
# ---------------------------------------------------------
def find_positions(grid):
    start = None
    goal = None

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                start = (row, col)
            elif grid[row][col] == 'G':
                goal = (row, col)

    return start, goal


# ---------------------------------------------------------
# Check whether a position is valid
# ---------------------------------------------------------
def is_valid(grid, position):
    row, col = position

    # Check if position is inside the grid
    if row < 0 or row >= len(grid):
        return False

    if col < 0 or col >= len(grid[row]):
        return False

    # '#' represents an obstacle
    if grid[row][col] == '#':
        return False

    return True


# ---------------------------------------------------------
# BFS Search
# ---------------------------------------------------------
def bfs(grid, start, goal):

    # Queue stores positions that need to be explored
    queue = deque([start])

    # Keep track of positions already visited
    visited = {start}

    # Store the previous position of each cell.
    # This is used later to reconstruct the path.
    parent = {start: None}

    # Possible movements:
    # Up, Down, Left, Right
    directions = [
        (-1, 0),   # Up
        (1, 0),    # Down
        (0, -1),   # Left
        (0, 1)     # Right
    ]

    # Continue searching while there are positions in the queue
    while queue:

        current = queue.popleft()

        # If we reached the goal, reconstruct the path
        if current == goal:
            return reconstruct_path(parent, goal)

        # Try all four possible actions
        for dr, dc in directions:

            next_position = (
                current[0] + dr,
                current[1] + dc
            )

            # Check whether the new position can be visited
            if is_valid(grid, next_position) and next_position not in visited:

                visited.add(next_position)
                parent[next_position] = current

                queue.append(next_position)

    # No path exists
    return None


# ---------------------------------------------------------
# Reconstruct the path from Start to Goal
# ---------------------------------------------------------
def reconstruct_path(parent, goal):

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parent[current]

    # The path was constructed backwards,
    # so reverse it.
    path.reverse()

    return path


# ---------------------------------------------------------
# Convert coordinates into movement directions
# ---------------------------------------------------------
def get_directions(path):

    directions = []

    for i in range(1, len(path)):

        previous = path[i - 1]
        current = path[i]

        row_change = current[0] - previous[0]
        col_change = current[1] - previous[1]

        if row_change == -1:
            directions.append("Up")

        elif row_change == 1:
            directions.append("Down")

        elif col_change == -1:
            directions.append("Left")

        elif col_change == 1:
            directions.append("Right")

    return directions


# ---------------------------------------------------------
# Display the path on the warehouse map
# ---------------------------------------------------------
def display_path(grid, path):

    # Convert each row into a list so that we can modify it
    display = [list(row) for row in grid]

    # Mark the path with '*'
    # Do not replace S or G.
    for row, col in path:

        if display[row][col] not in ('S', 'G'):
            display[row][col] = '*'

    print("\nWarehouse with path:")
    for row in display:
        print("".join(row))


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------
def main():

    # Find Start and Goal
    start, goal = find_positions(warehouse)

    print("WAREHOUSE NAVIGATION")
    print("--------------------")

    print("Start position:", start)
    print("Goal position :", goal)

    # Make sure both positions were found
    if start is None or goal is None:
        print("Error: Start or Goal position not found.")
        return

    # Run BFS
    path = bfs(warehouse, start, goal)

    # Check whether a path exists
    if path is None:

        print("\nNo collision-free path exists from S to G.")

    else:

        print("\nCollision-free path found!")

        print("Number of moves:", len(path) - 1)

        print("\nPath:")
        print(" -> ".join(map(str, path)))

        # Get movement directions
        movements = get_directions(path)

        print("\nActions:")
        print(" -> ".join(movements))

        # Display the path on the map
        display_path(warehouse, path)


# Run the program
if __name__ == "__main__":
    main()