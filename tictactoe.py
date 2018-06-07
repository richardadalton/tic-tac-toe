from flask import Flask, request, render_template

app = Flask(__name__)

moves = {
    0: "xbbbbbbbb",
    1: "bxbbbbbbb",
    2: "bbxbbbbbb",
    3: "bbbxbbbbb",
    4: "bbbbxbbbb",
    5: "bbbbbxbbb",
    6: "bbbbbbxbb",
    7: "bbbbbbbxb",
    8: "bbbbbbbbx",
}

def get_moves(board, player):
    moves = {}
    for i in range(9):
        if board[i] == 'b':
            moves[i] = board[:i] + player + board[i+1:]
    return moves

@app.route("/")
def get_index():
    if 'move' in request.args:
        board = request.args['move']
    else:
        board = 'bbbbbbbbb'
    moves = get_moves(board, 'x')
    return render_template("index.html", board=board, moves=moves)

@app.route("/new")
def get_new_gamge():
    board = "bbbbbbbbb"
    return render_template("index.html", board=board, moves=get_moves(board, 'x'))

@app.route("/move/<move>")
def make_move(move):
    board = move
    moves = {
        0: "xbbbbbbbb",
        1: "bxbbbbbbb",
        2: "bbxbbbbbb",
        3: "bbbxbbbbb",
        4: "bbbbxbbbb",
        5: "bbbbbxbbb",
        6: "bbbbbbxbb",
        7: "bbbbbbbxb",
        8: "bbbbbbbbx",
    }
    return render_template("index.html", board=board, moves=moves)

if __name__ == '__main__':
    app.run(debug=True)