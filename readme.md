# tic-tac-toe

## Overview
This project provides a web based front end through which tic-tac-toe can be played against a computer player.
The state of the game is entirely encoded in the page that is retrieved through the HTTP GET, and through the 
links that are embedded in that page.  Game state is not stored on the server in any way.

Multiple back end algorithms can be used (Minimax, Learning etc.)

## Installation

Just clone this repository

```bash
$ git clone https://github.com/richardadalton/tic-tac-toe.git
```

Create a virtual environment and install requirements.

```bash
$ python3 -m venv .venv
$ pip install -r requirements.txt
```

## Running tic-tac-toe

To run the web server, run the main tic-tac-toe script.

```bash
$ python tic-tac-toe.py
```

The webserver will run on port 5000 of localhost (127.0.0.1)
The root url redirects to /api/new which returns the game state for a new game.

## Payload
The payload of a game state is as follows:

```json
{
board: "bbbbbbbbb",
links: {
moves: {
0: "http://127.0.0.1:5000/api/move?player=x&board=xbbbbbbbb",
1: "http://127.0.0.1:5000/api/move?player=x&board=bxbbbbbbb",
2: "http://127.0.0.1:5000/api/move?player=x&board=bbxbbbbbb",
3: "http://127.0.0.1:5000/api/move?player=x&board=bbbxbbbbb",
4: "http://127.0.0.1:5000/api/move?player=x&board=bbbbxbbbb",
5: "http://127.0.0.1:5000/api/move?player=x&board=bbbbbxbbb",
6: "http://127.0.0.1:5000/api/move?player=x&board=bbbbbbxbb",
7: "http://127.0.0.1:5000/api/move?player=x&board=bbbbbbbxb",
8: "http://127.0.0.1:5000/api/move?player=x&board=bbbbbbbbx"
},
new_game: "http://127.0.0.1:5000/api/new"
},
player: "x",
result: null
}
```

* board: A string of 9 characters representing the values of the 9 positions in a tic-tac-toe board. x, o, or b (blank).
* player: The player whos turn it is. x, or o
* result: The result of the game, 1 (x wins), -1 (o wins), 0 (draw), None (not over yet)

* links: Actions that can be performed to change the game state. 
  * moves: A GET link for each aviailable move.  Following the link with make that move and get the AIs response.
  * new_game: A GET link to start a new game. 
