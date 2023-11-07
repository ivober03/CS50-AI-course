"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    countX = 0
    countO = 0

    for row in board:
        for cell in row:
            if cell == X:
                countX += 1
            if cell == O:
                countO += 1

    if countX > countO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    possible_actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise Exception("Invalid move.")

    i, j = action  # Unpack the (i, j) tuple

    # Create a deep copy of the board to avoid modifying the original
    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check for horizontal wins
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]

    # Check for vertical wins
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]

    # Check for main diagonal win (top-left to bottom-right)
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]

    # Check for other diagonal win (top-right to bottom-left)
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    # No winner found
    return None

def is_board_full(board):
    """
    Returns True if the tic-tac-toe board is completely filled, False otherwise.
    """

    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    return is_board_full(board) or winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board): # End game
        return None
    elif player(board) == X:  # Maximizing player
        best_action = None
        max_val = -math.inf
        for action in actions(board):
            val = min_value(result(board, action))
            if val > max_val:
                max_val = val
                best_action = action
        return best_action
    else:  # Minimizing player
        best_action = None
        min_val = math.inf
        for action in actions(board):
            val = max_value(result(board, action))
            if val < min_val:
                min_val = val
                best_action = action
        return best_action
