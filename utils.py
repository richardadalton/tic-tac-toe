from http.cookiejar import Cookie

from constants import *

def score(board):
    for pattern in WIN_PATTERNS:
        s = sum([board[i] for i in pattern])
        if s == 3:
            return X
        elif s == -3:
            return O

    for p in board:
        if p == N:
            return None

    return N

def make_move(board, move, player):
    new_board = board.copy()
    new_board[move] = player
    return new_board

def available_moves(board):
    this_score = score(board)
    if this_score != None:
        return []
    else:
        return [i for i in range(9) if board[i] == N]

def other_player(player):
    return -player



