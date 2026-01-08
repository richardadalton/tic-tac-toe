from flask import Flask, request, abort, redirect, jsonify
from flask_cors import CORS, cross_origin
from constants import *
from tictactoe_minimax import TicTacToeMiniMax
from tictactoe_random import TicTacToeRandom
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

    if 'history' in request.args:
        history_str = request.args['history']
    else:
        abort(400, "history not provided")

    return  str_to_player(player_str), str_to_board(board_str), history_str


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

def score_to_result(score):
    if score == X:
        return 'X Wins'
    elif score == O:
        return 'O Wins'
    elif score == N:
        return 'Draw'
    else:
        return None


# Use AI to get a move for a given position
def get_move(board, player):
    ai = TicTacToeMiniMax()
    move = ai.get_move(board, player)
    board[move] = O
    return board


def api_get_move_urls(board, player, history):
    moves = {}
    for i in range(9):
        if board[i] == 'b':
            board_str = board[:i] + player + board[i+1:]
            moves[i] = f"{BASE_URL}/api/move?player={player}&board={board_str}&history={history + board_str}"
    return moves


def serialize_response(player, board, history, score):
    if score is None:
        moves = api_get_move_urls(board, player, history)
    else:
        moves = []

    response = {
        'player': player,
        'board': board,
        'result': score_to_result(score),
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
    history = board
    result = None
    return serialize_response(player, board, history, result)


@app.route("/api/move")
@cross_origin()
def api_move():
    player, board, history = parse_request(request)
    player_str = player_to_str(player)
    otherplayer = other_player(player)

    result = score(board)
    if result is not None:
        # Player move has ended the game
        board_str = board_to_str(board)
        return serialize_response(None, board_str, history, result)
    else:
        # Get the other players move (AI)
        board = get_move(board, otherplayer)
        board_str = board_to_str(board)
        result = score(board)
        return serialize_response(player_str, board_str, history, result)


@app.route("/")
def get_index():
    return redirect("/api/new")


if __name__ == '__main__':
    app.run(debug=True)