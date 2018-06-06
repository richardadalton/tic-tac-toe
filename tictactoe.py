from flask import Flask, redirect, render_template, request
import json
from random import choice

app = Flask(__name__)

@app.route("/")
def get_index():
    board_pieces = { i: choice([-1, 0, 1]) for i in range(9)}
    return render_template("index.html", board_pieces = json.dumps(board_pieces))

if __name__ == '__main__':
    app.run(debug=True)