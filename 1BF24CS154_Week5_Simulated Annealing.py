import random
import math

# 1. COST FUNCTION
def calculate_cost(board):
    cost = 0

    for i in range(8):
        for j in range(i + 1, 8):

            # Same row
            if board[i] == board[j]:
                cost += 1

            # Same diagonal
            elif abs(board[i] - board[j]) == abs(i - j):
                cost += 1

    return cost

# 2. GENERATE RANDOM NEIGHBOUR
def generate_neighbour(board):
    neighbour = board.copy()

    # Random column
    column = random.randint(0, 7)

    # Different random row
    new_row = random.randint(0, 7)

    while new_row == neighbour[column]:
        new_row = random.randint(0, 7)

    neighbour[column] = new_row

    return neighbour

# 3. DISPLAY CHESS BOARD
def display_board(board):
    print("\nChess Board:")

    for row in range(8):
        for col in range(8):

            if board[col] == row:
                print("Q", end=" ")
            else:
                print(".", end=" ")

        print()

# 4. SIMULATED ANNEALING
def simulated_annealing(initial_board, initial_temperature,
                        cooling_factor, max_iterations):

    
    
    current = initial_board.copy()
    current_cost = calculate_cost(current)
    best = current.copy()
    best_cost = current_cost
    T = initial_temperature
    iteration = 0
    MIN_TEMPERATURE = 0.000001
    while T > MIN_TEMPERATURE and iteration < max_iterations:
        iteration += 1
        if current_cost == 0:
            break
        next_state = generate_neighbour(current)
        next_cost = calculate_cost(next_state)
        delta_E = current_cost - next_cost
        if delta_E > 0:
            current = next_state
            current_cost = next_cost
        else:
            probability = math.exp(delta_E / T)
            random_number = random.random()
            if random_number < probability:
                current = next_state
                current_cost = next_cost
        if current_cost < best_cost:
            best = current.copy()
            best_cost = current_cost
        T = T * cooling_factor
    return best, best_cost, iteration

# MAIN PROGRAM
print("==========================================")
print("     8-QUEENS SIMULATED ANNEALING")
print("==========================================")

print("\nBoard representation:")
print("board[column] = row")
print("Rows and columns are numbered from 0 to 7.")

print("\nExample:")
print("0 1 2 3 4 5 6 7")

# INPUT INITIAL BOARD

while True:

    try:
        board = list(
            map(int, input("\nEnter initial board (8 values): ").split())
        )

        if len(board) != 8:
            print("Error: Please enter exactly 8 values.")
            continue

        if any(row < 0 or row > 7 for row in board):
            print("Error: Each value must be between 0 and 7.")
            continue

        break

    except ValueError:
        print("Error: Please enter integers only.")


# ---------------------------------------------------------
# INPUT TEMPERATURE
# ---------------------------------------------------------
while True:

    try:
        temperature = float(
            input("Enter initial temperature (e.g. 10): ")
        )

        if temperature <= 0:
            print("Temperature must be greater than 0.")
            continue

        break

    except ValueError:
        print("Please enter a valid number.")


# ---------------------------------------------------------
# INPUT COOLING FACTOR
# ---------------------------------------------------------
while True:

    try:
        alpha = float(
            input("Enter cooling factor (e.g. 0.99): ")
        )

        if alpha <= 0 or alpha >= 1:
            print("Cooling factor must be between 0 and 1.")
            continue

        break

    except ValueError:
        print("Please enter a valid number.")


# ---------------------------------------------------------
# INPUT MAXIMUM ITERATIONS
# ---------------------------------------------------------
while True:

    try:
        max_iterations = int(
            input("Enter maximum iterations (e.g. 100000): ")
        )

        if max_iterations <= 0:
            print("Iterations must be greater than 0.")
            continue

        break

    except ValueError:
        print("Please enter an integer.")


# ---------------------------------------------------------
# INITIAL INFORMATION
# ---------------------------------------------------------
initial_cost = calculate_cost(board)

print("\n==========================================")
print("INITIAL STATE")
print("==========================================")

print("Initial Board :", board)
print("Initial Cost  :", initial_cost)
print("Temperature   :", temperature)
print("Cooling Factor:", alpha)


# ---------------------------------------------------------
# RUN SIMULATED ANNEALING
# ---------------------------------------------------------
solution, final_cost, iterations = simulated_annealing(
    board,
    temperature,
    alpha,
    max_iterations
)


# ---------------------------------------------------------
# FINAL RESULT
# ---------------------------------------------------------
print("\n==========================================")
print("FINAL RESULT")
print("==========================================")

print("Final Board :", solution)
print("Final Cost  :", final_cost)
print("Iterations  :", iterations)

display_board(solution)


if final_cost == 0:
    print("\nSUCCESS: 8-Queens solution found!")
else:
    print("\nNo solution found within the iteration limit.")
    print("Try a higher iteration limit or a slower cooling factor.")
