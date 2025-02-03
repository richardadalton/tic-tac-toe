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
