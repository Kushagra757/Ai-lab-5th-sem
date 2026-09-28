import random

board = [" " for _ in range(9)]

def display_board():
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])
    print()

def check_winner(player):
    combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in combinations:
        if board[a] == player and board[b] == player and board[c] == player:
            return True

    return False

def ai_move():
    empty_positions = []

    for i in range(9):
        if board[i] == " ":
            empty_positions.append(i)

    if not empty_positions:
        return

    # 1. Check if AI can win in the next move
    for i in empty_positions:
        board[i] = "O"
        if check_winner("O"):
            print("AI chose position:", i + 1)
            return
        board[i] = " " # Undo the move

    # 2. Check if player can win in the next move and block them
    for i in empty_positions:
        board[i] = "X"
        if check_winner("X"):
            board[i] = "O" # Block the player
            print("AI chose position:", i + 1)
            return
        board[i] = " " # Undo the move

    # 3. Try to take the center
    if 4 in empty_positions:
        board[4] = "O"
        print("AI chose position: 5")
        return

    # 4. Try to take a corner
    corners = [0, 2, 6, 8]
    available_corners = [c for c in corners if c in empty_positions]
    if available_corners:
        position = random.choice(available_corners)
        board[position] = "O"
        print("AI chose position:", position + 1)
        return

    # 5. Take any remaining empty spot (sides)
    if empty_positions:
        position = random.choice(empty_positions)
        board[position] = "O"
        print("AI chose position:", position + 1)

def game():
    print("TIC-TAC-TOE")
    print("You = X")
    print("AI  = O")

    for turn in range(9):

        display_board()

        # Human's turn
        if turn % 2 == 0:
            while True:
                try:
                    position = int(input("Enter your position (1-9): "))
                    if position < 1 or position > 9:
                        print("Invalid position!")
                        continue
                    if board[position - 1] != " ":
                        print("Position already occupied!")
                        continue
                    break
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 9.")

            board[position - 1] = "X"

            if check_winner("X"):
                display_board()
                print("You win!")
                return

        # AI's turn
        else:
            ai_move()

            if check_winner("O"):
                display_board()
                print("AI wins!")
                return

    display_board()
    print("It's a draw!")

game()
