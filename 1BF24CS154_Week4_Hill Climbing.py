import random

# Calculate number of attacking pairs (conflicts to minimize)
def heuristic(state):
    conflicts = 0
    for i in range(4):
        for j in range(i + 1, 4):
            # Same row
            if state[i] == state[j]:
                conflicts += 1
            # Same diagonal
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts


# Generate all possible neighboring states
def get_neighbors(state):
    neighbors = []
    for col in range(4):
        for row in range(4):
            if row != state[col]:
                new_state = state.copy()
                new_state[col] = row
                neighbors.append(new_state)
    return neighbors


# Hill Climbing with Side-Steps to escape local minima
def hill_climbing(start, max_sidesteps=100):
    current = start
    current_h = heuristic(current)
    sidesteps = 0

    while True:
        neighbors = get_neighbors(current)
        
        # Find the best neighbors (minimize conflicts)
        best_neighbors = []
        best_h = current_h

        for neighbor in neighbors:
            h = heuristic(neighbor)
            if h < best_h:
                best_neighbors = [neighbor]
                best_h = h
            elif h == best_h:
                best_neighbors.append(neighbor)

        # If no neighbor is better or equal
        if best_h > current_h:
            break
            
        # If the best found is strictly better
        if best_h < current_h:
            current = random.choice(best_neighbors)
            current_h = best_h
            sidesteps = 0
        # If the best found is equal (side-step)
        elif best_h == current_h:
            if sidesteps < max_sidesteps and best_neighbors:
                current = random.choice(best_neighbors)
                current_h = best_h
                sidesteps += 1
            else:
                break

    return current


# Print board
def print_board(state):
    for row in range(4):
        for col in range(4):
            if state[col] == row:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()


# -----------------------------
# MAIN RUNNER
# -----------------------------

print("4 Queens - Hill Climbing")

print("\nEnter initial state.")
print("Enter 4 numbers (0-3).")
print("Each number represents the row of the queen in each column.")
print("\nExample: 1 3 0 2")

try:
    user_input = input("\nInitial state: ").strip()
    # Fallback default if input is empty
    if not user_input:
        user_input = "0 2 3 1"
        print(f"Using default state: {user_input}")
    start = list(map(int, user_input.split()))
except Exception as e:
    start = [0, 2, 3, 1]
    print(f"Invalid input, using default state: 0 2 3 1")

# Check input
if len(start) != 4 or any(x < 0 or x > 3 for x in start):
    print("Invalid input!")
    print("Enter 4 numbers between 0 and 3.")
else:
    print("\nInitial State:")
    print_board(start)
    print("\nInitial heuristic (conflicts):", heuristic(start))

    # Apply Hill Climbing
    solution = hill_climbing(start)

    print("\nFinal State:")
    print_board(solution)
    print("\nFinal heuristic (conflicts):", heuristic(solution))

    if heuristic(solution) == 0:
        print("\nSolution found!")
    else:
        print("\nHill Climbing got stuck at a local minimum.")
