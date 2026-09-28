def get_neighbors(state):
    neighbors = []

    index = state.index(0)
    row = index // 3
    col = index % 3

    moves = [
        (-1, 0), # Up
        (1, 0), # Down
        (0, -1), # Left
        (0, 1) # Right
    ]

    for dr, dc in moves:
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col

            new_state = list(state)
            new_state[index], new_state[new_index] = \
                new_state[new_index], new_state[index]

            neighbors.append(tuple(new_state))

    return neighbors


def dfs(start, goal):
    stack = [(start, [start])]
    visited = set()

    while stack:
        state, path = stack.pop()

        if state == goal:
            return path

        if state in visited:
            continue

        visited.add(state)

        for next_state in get_neighbors(state):
            if next_state not in visited:
                stack.append((next_state, path + [next_state]))

    return None


def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()


# Initial state
start = (
    1, 2, 3,
    4, 0, 6,
    7, 5, 8
)

# Goal state
goal = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)

solution = dfs(start, goal)

if solution:
    print("Solution found!")
    print("Number of moves:", len(solution) - 1)
    
    for step in solution:
        print_puzzle(step)
else:
    print("No solution found.")

import math

# Average branching factor for an 8-puzzle
# (4 corners * 2 moves + 4 edges * 3 moves + 1 center * 4 moves) / 9 positions
branching_factor = 3

# Depth of the solution is the number of moves
solution_depth = len(solution) - 1

print(f"Average branching factor (b): {branching_factor:.2f}")
print(f"Depth of the solution (d): {solution_depth}")

try:
    # Calculate approximate time and space complexity (b^d)
    time_space_complexity = math.pow(branching_factor, solution_depth)
    print(f"Approximate time/space complexity (b^d): {time_space_complexity:.2e}")
except OverflowError:
    print(f"Approximate time/space complexity (b^d): Too large to calculate (b={branching_factor:.2f}, d={solution_depth})")
