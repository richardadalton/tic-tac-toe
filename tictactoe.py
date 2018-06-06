from flask import Flask, redirect, render_template, request
import json
from random import choice

app = Flask(__name__)

@app.route("/")
def get_index():
    board = "".join([choice(["x", "b", "o"]) for i in range(9)])
    return render_template("index.html", board = board)


@app.route("/new")
def get_new_gamge():
    board = "bbbbbbbbb"
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
    return render_template("index.html", board=board, moves=json.dumps(moves))

if __name__ == '__main__':
    app.run(debug=True)