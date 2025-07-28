import math

# Initialize board
board = [' ' for _ in range(9)]

# Print the board
def print_board():
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

# Check for winner or tie
def check_winner(board, player):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],  # Rows
        [0,3,6], [1,4,7], [2,5,8],  # Columns
        [0,4,8], [2,4,6]            # Diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == player for i in condition):
            return True
    return False

def is_board_full(board):
    return ' ' not in board

# Minimax Algorithm
def minimax(board, is_maximizing):
    if check_winner(board, 'O'):
        return 1
    elif check_winner(board, 'X'):
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                score = minimax(board, False)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                score = minimax(board, True)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score

# AI move
def ai_move():
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    board[move] = 'O'

# Main Game Loop
def play_game():
    print("Welcome to Tic-Tac-Toe! You are X, AI is O.")
    print_board()

    while True:
        # Player move
        try:
            move = int(input("Enter your move (0-8): "))
            if board[move] != ' ':
                print("Invalid move! Try again.")
                continue
            board[move] = 'X'
        except (ValueError, IndexError):
            print("Invalid input! Please enter a number from 0 to 8.")
            continue

        print_board()
        if check_winner(board, 'X'):
            print("You win!")
            break
        elif is_board_full(board):
            print("It's a tie!")
            break

        # AI move
        print("AI is making a move...")
        ai_move()
        print_board()

        if check_winner(board, 'O'):
            print("AI wins!")
            break
        elif is_board_full(board):
            print("It's a tie!")
            break

# Run the game
play_game()