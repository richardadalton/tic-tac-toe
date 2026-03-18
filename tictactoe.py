from flask import Flask, request, abort, send_from_directory, jsonify
from flask_cors import CORS, cross_origin
from constants import *
from tictactoe_minimax import TicTacToeMiniMax
from tictactoe_random import TicTacToeRandom
from utils import other_player, score, winning_line

app = Flask(__name__, static_folder='site/static')
cors = CORS(app)


def base_url():
    return request.url_root.rstrip('/')

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


def api_get_move_urls(board, player):
    moves = {}
    for i in range(9):
        if board[i] == 'b':
            board_str = board[:i] + player + board[i+1:]
            moves[i] = f"{base_url()}/api/move?player={player}&board={board_str}"
    return moves


def serialize_response(player, board, score, win_line=None):
    if score is None:
        moves = api_get_move_urls(board, player)
    else:
        moves = []

    response = {
        'game': {
            'player': player,
            'board': board,
        }
    }

    result = score_to_result(score)
    if result:
        response['game']['result'] = result

    if win_line:
        response['game']['win_line'] = win_line

    response['links'] = {
        'new_game': base_url() + '/api/new',
        'moves': moves,
    }

    return jsonify(response)


@app.route("/api/new")
@cross_origin()
def api_new_game():
    player = 'x'
    board = 'bbbbbbbbb'
    result = None
    return serialize_response(player, board, result)


@app.route("/api/move")
@cross_origin()
def api_move():
    player, board = parse_request(request)
    player_str = player_to_str(player)
    otherplayer = other_player(player)

    result = score(board)
    if result is not None:
        # Player move has ended the game
        board_str = board_to_str(board)
        win_line = winning_line(board)
        return serialize_response(None, board_str, result, win_line)
    else:
        # Get the other players move (AI)
        board = get_move(board, otherplayer)
        board_str = board_to_str(board)
        result = score(board)
        win_line = winning_line(board)
        return serialize_response(player_str, board_str, result, win_line)


@app.route("/")
def get_index():
    return send_from_directory('site', 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
