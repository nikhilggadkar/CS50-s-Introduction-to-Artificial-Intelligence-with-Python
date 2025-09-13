"""
Tic Tac Toe Player
"""

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
    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

    # If both have played equal or X has played less, it's X's turn
    if x_count <= o_count:
        return X
    else:
        return O
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))
    return possible_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # If that spot is already filled, it’s a wrong move
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid move: this place is already taken.")

    # Make a new board from the old one
    new_board = [row[:] for row in board]

    # Put the symbol of the current player on the new board
    new_board[i][j] = player(board)

    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checking rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    # Checking both diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None
def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    # No empty cell and no winner means match is drawn
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current = player(board)

    # When it's X's turn - X wants highest score
    def max_value(board):
        if terminal(board):
            return utility(board), None

        best_score = float('-inf')  # Starting with lowest score possible
        best_move = None

        for action in actions(board):
            new_board = result(board, action)
            score, _ = min_value(new_board)

            if score > best_score:
                best_score = score
                best_move = action

        return best_score, best_move

    # When it's O's turn - O wants lowest score
    def min_value(board):
        if terminal(board):
            return utility(board), None

        best_score = float('inf')  # Starting with highest score
        best_move = None

        for action in actions(board):
            new_board = result(board, action)
            score, _ = max_value(new_board)

            if score < best_score:
                best_score = score
                best_move = action

        return best_score, best_move

    # Call the right helper depending on who is playing
    if current == X:
        _, move = max_value(board)
    else:
        _, move = min_value(board)

    return move

