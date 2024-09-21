import random

# Use nested loops to create the board
def create_board():
    board = []  # Initialize the board
    for i in range(3):  # Outer loop for rows
        row = []  # Start with an empty row
        for j in range(3):  # Inner loop for columns
            row.append(str(i * 3 + j + 1))  # Fill the row with values (1 to 9)
        board.append(row)  # Add the filled row to the board
    return board


# Allows user to place a mark on the board with an X or O
def place_mark(board, mark, position):
    row = (position - 1) // 3
    col = (position - 1) % 3

    if board[row][col] in ['X', 'O']:
        return False

    board[row][col] = mark
    return True


# Check for wins
def check_win(board, mark):
    # Check rows
    for row in board:
        if all(cell == mark for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == mark for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == mark for i in range(3)):
        return True
    if all(board[i][2 - i] == mark for i in range(3)):
        return True

    return False


# Check for a draw
def is_draw(board):
    return all(cell in ['X', 'O'] for row in board for cell in row)


# Find a winning move for the AI
def find_winning_move(board, mark):
    for position in range(1, 10):  # Loop through all positions 1 to 9
        row = (position - 1) // 3
        col = (position - 1) % 3

        if board[row][col] not in ['X', 'O']:  # Check if the cell is empty
            board[row][col] = mark  # Temporarily place the mark
            if check_win(board, mark):
                board[row][col] = str(position)  # Undo the move
                return position
            board[row][col] = str(position)  # Undo the move

    return None  # No winning move found


# Check if AI needs to block the player's winning move
def find_blocking_move(board, player_mark):
    for position in range(1, 10):  # Loop through all positions 1 to 9
        row = (position - 1) // 3
        col = (position - 1) % 3

        if board[row][col] not in ['X', 'O']:  # Check if the cell is empty
            board[row][col] = player_mark  # Temporarily place the opponent's mark
            if check_win(board, player_mark):
                board[row][col] = str(position)  # Undo the move
                return position
            board[row][col] = str(position)  # Undo the move

    return None  # No blocking move needed


# Function to check for available spots
def available_spots(board):
    return [i for i in range(1, 10) if board[(i - 1) // 3][(i - 1) % 3] not in ['X', 'O']]


# Global variable to track if it's the first game
is_first_game = True


# Minimax algorithm to find the best move for AI
def minimax(board, depth, is_maximizing, ai_mark, player_mark):
    # Base cases: check for a winner or draw
    if check_win(board, ai_mark):
        return 10 - depth
    elif check_win(board, player_mark):
        return depth - 10
    elif is_draw(board):
        return 0

    # Maximizing player (AI's turn)
    if is_maximizing:
        best_score = -float('inf')
        for move in available_spots(board):
            row, col = (move - 1) // 3, (move - 1) % 3
            board[row][col] = ai_mark  # AI makes a move
            score = minimax(board, depth + 1, False, ai_mark, player_mark)  # Recursively call minimax
            board[row][col] = str(move)  # Undo the move
            best_score = max(score, best_score)
        return best_score

    # Minimizing player (Player's turn)
    else:
        best_score = float('inf')
        for move in available_spots(board):
            row, col = (move - 1) // 3, (move - 1) % 3
            board[row][col] = player_mark  # Player makes a move
            score = minimax(board, depth + 1, True, ai_mark, player_mark)  # Recursively call minimax
            board[row][col] = str(move)  # Undo the move
            best_score = min(score, best_score)
        return best_score


# AI move function with first game rigging
def ai_smart_move(board, player_mark, ai_mark):
    global is_first_game  # Access the global variable

    # If it's the first game, the AI plays randomly
    if is_first_game:
        available_positions = available_spots(board)
        return random.choice(available_positions)  # AI makes a random move in the first game

    # After the first game, use the unbeatable AI strategy with minimax
    best_score = -float('inf')
    best_move = None

    # Loop through available spots to find the best move
    for move in available_spots(board):
        row, col = (move - 1) // 3, (move - 1) % 3
        board[row][col] = ai_mark  # AI makes a tentative move
        score = minimax(board, 0, False, ai_mark, player_mark)  # Call minimax for evaluation
        board[row][col] = str(move)  # Undo the move

        # Find the move with the highest score
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


# Function to reset the game and switch to unbeatable AI after the first game
def end_game_logic():
    global is_first_game
    is_first_game = False  # Disable the rigged AI after the first game

