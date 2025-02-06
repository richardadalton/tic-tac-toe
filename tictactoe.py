from os import abort

from flask import Flask, request, abort, render_template, jsonify
from tictactoe_minimax import TicTacToeMiniMax
from constants import *
from utils import other_player, score

app = Flask(__name__)

BASE_URL = "http://127.0.0.1:5000"

# Map between the web based string representation of the player and board, and the algorithm representation
def str_to_player(str):
    map_str_to_player = {
        'b': N,
        'x': X,
        'o': O,
    }
    return map_str_to_player[str]


def player_to_str(player):
    map_player_to_str = {
        N: 'b',
        X: 'x',
        O: 'o',
    }
    return player_to_str(player)


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


# Use AI to get move for a given position
def get_move(board, player):
    board2 = str_to_board(board)
    ai = TicTacToeMiniMax()
    move = ai.get_move(board2, player)
    board2[move] = O
    return board2




def api_get_moves(board, player):
    moves = {}
    for i in range(9):
        if board[i] == 'b':
            board_str = board[:i] + player + board[i+1:]
            moves[i] = f"{BASE_URL}/api/move?player={player}&board={board_str}"
    return moves


@app.route("/api/new")
def api_new_game():
    player = 'x'
    board = 'bbbbbbbbb'
    moves = api_get_moves(board, player)

    response = {
        'player': player,
        'board': board,
        'result': None,
        'links': {
            'new_game': BASE_URL + '/api/new',
            'moves': moves,
        }
    }
    return jsonify(response)


@app.route("/api/move")
def api_move():
    player_str, board_str = parse_request(request)

    player = str_to_player(player_str)
    oplayer = other_player(player)
    board = get_move(board_str, oplayer)

    str = board_to_str(board)
    moves = api_get_moves(str, 'x')

    result = score(board)
    if result is not None:
        moves = []

    response = {
        'player': 'x',
        'board': str,
        'result': result,
        'links': {
            'new_game': BASE_URL + '/api/new',
            'moves': moves,
        }

    }
    return jsonify(response)





def get_moves(board, player):
    moves = {}
    for i in range(9):
        if board[i] == 'b':
            moves[i] = board[:i] + player + board[i+1:]
    return moves


@app.route("/new")
def get_new_game():
    player = 'x'
    board = "bbbbbbbbb"
    moves = get_moves(board, player)
    return render_template("index.html", board=board, moves=moves, player=player)


@app.route("/")
def get_index():
    if 'move' in request.args:
        board = request.args['move']
    else:
        board = 'bbbbbbbbb'

    board = get_move(board, O)
    str = board_to_str(board)
    moves = get_moves(str, 'x')
    return render_template("index.html", board=str, moves=moves, player='x')


def parse_request(request):
    if 'board' in request.args:
        board_str = request.args['board']
    else:
        abort(400, "board not provided")

    if 'player' in request.args:
        player_str = request.args['player']
    else:
        abort(400, "player not provided")

    return player_str, board_str


if __name__ == '__main__':
    app.run(debug=True)