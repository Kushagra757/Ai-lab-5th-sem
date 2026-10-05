import heapq

start = [2, 8, 3,
         1, 6, 4,
         7, 0, 5]

goal = [1, 2, 3,
        8, 0, 4,
        7, 6, 5]


def manhattan_distance(state, goal):
    """Calculates the sum of Manhattan distances of tiles from their goal positions (excluding the blank space 0)."""
    distance = 0
    for i in range(9):
        tile = state[i]
        if tile != 0:
            # Current 2D coordinates
            curr_row, curr_col = i // 3, i % 3
            
            # Goal 2D coordinates
            goal_index = goal.index(tile)
            goal_row, goal_col = goal_index // 3, goal_index % 3
            
            distance += abs(curr_row - goal_row) + abs(curr_col - goal_col)
    return distance


def misplaced_tiles(state, goal):
    """Calculates the number of misplaced tiles (excluding the blank space 0)."""
    count = 0
    for i in range(9):
        if state[i] != 0 and state[i] != goal[i]:
            count += 1
    return count


def get_neighbors(state):
    neighbors = []

    blank = state.index(0)
    row = blank // 3
    col = blank % 3

    if row > 0:
        new_state = state.copy()
        new_state[blank], new_state[blank - 3] = \
            new_state[blank - 3], new_state[blank]
        neighbors.append(new_state)

    if row < 2:
        new_state = state.copy()
        new_state[blank], new_state[blank + 3] = \
            new_state[blank + 3], new_state[blank]
        neighbors.append(new_state)

    if col > 0:
        new_state = state.copy()
        new_state[blank], new_state[blank - 1] = \
            new_state[blank - 1], new_state[blank]
        neighbors.append(new_state)

    if col < 2:
        new_state = state.copy()
        new_state[blank], new_state[blank + 1] = \
            new_state[blank + 1], new_state[blank]
        neighbors.append(new_state)

    return neighbors


def a_star(start, goal, heuristic_fn=misplaced_tiles):
    h = heuristic_fn(start, goal)
    initial_path = [(start, 0, h, h)]
    priority_queue = [(h, 0, start, initial_path)]
    visited = set()

    total_branches = 0
    states_checked = 0

    while priority_queue:
        f, g, current, path = heapq.heappop(priority_queue)
        current_tuple = tuple(current)

        if current_tuple in visited:
            continue

        visited.add(current_tuple)
        neighbors = get_neighbors(current)
        total_branches += len(neighbors)
        states_checked += 1

        if current == goal:
            branching_factor = total_branches / states_checked if states_checked > 0 else 0
            return path, len(visited), branching_factor

        for next_state in neighbors:
            if tuple(next_state) not in visited:
                new_g = g + 1
                new_h = heuristic_fn(next_state, goal)
                new_f = new_g + new_h

                next_step_info = (next_state, new_g, new_h, new_f)
                heapq.heappush(
                    priority_queue,
                    (new_f, new_g, next_state, path + [next_step_info])
                )

    return None, len(visited), 0


def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i], state[i + 1], state[i + 2])
    print()


# Solve using Misplaced Tiles Heuristic
solution_path, explored_states, b = a_star(start, goal, heuristic_fn=misplaced_tiles)

if solution_path:
    print("Initial State:")
    print_puzzle(start)

    print("Goal State:")
    print_puzzle(goal)

    print("Solution:")
    print("Number of moves:", len(solution_path) - 1)
    print("Number of states:", len(solution_path))
    print("States explored:", explored_states)
    print()

    for i, (state, g, h, f) in enumerate(solution_path):
        print(f"Step {i} (Path Cost g={g}, Heuristic h={h}, Total f={f})")
        print_puzzle(state)

else:
    print("No solution found.")
