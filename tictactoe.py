from flask import Flask, request, render_template
from tictactoe_minimax import TicTacToeMiniMax
from tictactoe_random import TicTacToeRandom
from utils import score
from constants import *

app = Flask(__name__)

def get_moves(board, player):
    moves = {}
    for i in range(9):
        if board[i] == 'b':
            moves[i] = board[:i] + player + board[i+1:]
    return moves


def str_to_board(str):
    map_str_to_board = {
        'b': N,
        'x': X,
        'o': O,
    }
    return [map_str_to_board[c] for c in str]


def board_to_str(board):
    map_board_to_str = {
        N: 'b',
        X: 'x',
        O: 'o',
    }
    return "".join([map_board_to_str[b] for b in board])



@app.route("/new")
def get_new_game():
    board = "bbbbbbbbb"
    return render_template("index.html", board=board, moves=get_moves(board, 'x'))


@app.route("/")
def get_index():
    if 'move' in request.args:
        board = request.args['move']
    else:
        board = 'bbbbbbbbb'

    board = get_move(board, 'o')
    str = board_to_str(board)
    moves = get_moves(str, 'x')
    return render_template("index.html", board=str, moves=moves)





def get_move(board, player):
    board2 = str_to_board(board)
    ai = TicTacToeMiniMax()
    move = ai.get_move(board2, O)
    board2[move] = O
    return board2



if __name__ == '__main__':
    app.run(debug=True)