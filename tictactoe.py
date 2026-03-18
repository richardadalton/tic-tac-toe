import os
from flask import Flask, request, abort, send_from_directory, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.middleware.proxy_fix import ProxyFix
from constants import *
from tictactoe_minimax import TicTacToeMiniMax
from tictactoe_random import TicTacToeRandom
from utils import other_player, score, winning_line

app = Flask(__name__, static_folder='site/static')
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
cors = CORS(app)

ALGORITHMS = {
    'minimax': TicTacToeMiniMax,
    'random':  TicTacToeRandom,
}


def base_url():
    return request.url_root.rstrip('/')


def get_algorithm(name):
    cls = ALGORITHMS.get(name)
    if cls is None:
        abort(400, f"Unknown algorithm: {name}")
    return cls()


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


def parse_player_config(request):
    x_player = request.args.get('x_player', 'human')
    o_player = request.args.get('o_player', 'minimax')
    return x_player, o_player


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


def api_get_move_urls(board, player, x_player, o_player):
    moves = {}
    for i in range(9):
        if board[i] == 'b':
            board_str = board[:i] + player + board[i+1:]
            moves[i] = (
                f"{base_url()}/api/move"
                f"?player={player}&board={board_str}"
                f"&x_player={x_player}&o_player={o_player}"
            )
    return moves


def serialize_response(player, board, score, win_line=None, x_player='human', o_player='minimax'):
    if score is None:
        moves = api_get_move_urls(board, player, x_player, o_player)
    else:
        moves = []

    response = {
        'game': {
            'player': player,
            'board': board,
            'x_player': x_player,
            'o_player': o_player,
        }
    }

    result = score_to_result(score)
    if result:
        response['game']['result'] = result

    if win_line:
        response['game']['win_line'] = win_line

    links = {
        'new_game': base_url() + '/api/new',
        'moves': moves,
    }

    # If the current player is an AI, compute its best move and include the link.
    # The frontend will follow this automatically, showing each move individually.
    if score is None and player in ('x', 'o'):
        current_player_config = x_player if player == 'x' else o_player
        if current_player_config != 'human':
            player_int = str_to_player(player)
            board_list = str_to_board(board)
            ai = get_algorithm(current_player_config)
            best_move = ai.get_move(board_list, player_int)
            board_with_move = board[:best_move] + player + board[best_move + 1:]
            links['ai_move'] = (
                f"{base_url()}/api/move"
                f"?player={player}&board={board_with_move}"
                f"&x_player={x_player}&o_player={o_player}"
            )

    response['links'] = links
    return jsonify(response)


@app.route("/api/new")
@cross_origin()
def api_new_game():
    x_player, o_player = parse_player_config(request)
    # Always return the empty board — serialize_response adds the ai_move link
    # if X is an AI, so the frontend will kick off the first move automatically.
    return serialize_response('x', 'bbbbbbbbb', None, None, x_player, o_player)


@app.route("/api/move")
@cross_origin()
def api_move():
    player, board = parse_request(request)
    x_player, o_player = parse_player_config(request)

    # Check whether the submitted move ended the game
    result = score(board)
    if result is not None:
        board_str = board_to_str(board)
        win_line = winning_line(board)
        return serialize_response(None, board_str, result, win_line, x_player, o_player)

    # Advance to the next player; serialize_response handles the ai_move link
    next_player_str = player_to_str(other_player(player))
    board_str = board_to_str(board)
    return serialize_response(next_player_str, board_str, None, None, x_player, o_player)


@app.route("/")
def get_index():
    return send_from_directory('site', 'index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9000))
    print(f"Starting tic-tac-toe on 0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
