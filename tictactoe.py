from os import abort

from flask import Flask, request, abort, redirect, jsonify
from flask_cors import CORS, cross_origin
from tictactoe_minimax import TicTacToeMiniMax
from constants import *
from utils import other_player, score

app = Flask(__name__)
cors = CORS(app)

BASE_URL = "http://127.0.0.1:5000"


def parse_request(request):
    if 'board' in request.args:
        board_str = request.args['board']
    else:
        abort(400, "board not provided")

    if 'player' in request.args:
        player_str = request.args['player']
    else:
        abort(400, "player not provided")

    return  str_to_player(player_str), str_to_board(board_str)


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
    return map_player_to_str[player]


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
    ai = TicTacToeMiniMax()
    move = ai.get_move(board, player)
    board[move] = O
    return board


def api_get_move_urls(board, player):
    moves = {}
    for i in range(9):
        if board[i] == 'b':
            board_str = board[:i] + player + board[i+1:]
            moves[i] = f"{BASE_URL}/api/move?player={player}&board={board_str}"
    return moves


def serialize_response(player, board, result, moves):
    response = {
        'player': player,
        'board': board,
        'result': result,
        'links': {
            'new_game': BASE_URL + '/api/new',
            'moves': moves,
        }
    }
    return jsonify(response)


@app.route("/api/new")
@cross_origin()
def api_new_game():
    player = 'x'
    board = 'bbbbbbbbb'
    result = None
    moves = api_get_move_urls(board, player)
    return serialize_response(player, board, result, moves)


@app.route("/api/move")
@cross_origin()
def api_move():
    player, board = parse_request(request)

    otherplayer = other_player(player)

    # Get the other players move (AI)
    board = get_move(board, otherplayer)

    player_str = player_to_str(player)
    board_str = board_to_str(board)
    moves = api_get_move_urls(board_str, player_str)

    result = score(board)
    if result is not None:
        moves = []
    return serialize_response(player_str, board_str, result, moves)


@app.route("/")
def get_index():
    return redirect("/api/new")


if __name__ == '__main__':
    app.run(debug=True)