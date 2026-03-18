# Tic-Tac-Toe

A browser-based Tic-Tac-Toe game built as an exercise in genuine
[HATEOAS](https://en.wikipedia.org/wiki/HATEOAS) REST API design.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [HATEOAS Design](#hateoas-design)
- [API Reference](#api-reference)
- [AI Algorithms](#ai-algorithms)
- [Frontend](#frontend)
- [Player Configuration](#player-configuration)
- [Installation](#installation)
- [Running Locally](#running-locally)
- [Deployment](#deployment)
- [Testing](#testing)

---

## Architecture Overview

The system is split into three distinct layers.

```
┌─────────────────────────────────────────┐
│              Browser (UI)               │
│  site/index.html  +  site/static/       │
│  SVG board, player-select dropdowns     │
│  Follows links from API — no URL logic  │
└────────────────────┬────────────────────┘
                     │ HTTP GET (XHR)
┌────────────────────▼────────────────────┐
│            Flask API Server             │
│  tictactoe.py                           │
│  /api/new    /api/move                  │
│  Stateless — all state lives in URLs    │
└────────────────────┬────────────────────┘
                     │ function calls
┌────────────────────▼────────────────────┐
│           AI / Game Logic               │
│  utils.py            — core rules       │
│  tictactoe_minimax.py — perfect play    │
│  tictactoe_random.py  — random moves    │
└─────────────────────────────────────────┘
```

### Key design principle — no server-side state

The server holds **zero session state**. Every piece of information needed to
describe the current game — the board, whose turn it is, which player types are
configured — is encoded in the URL that was followed to get there. A response
can always be bookmarked, shared, or replayed by re-issuing the same GET
request.

---

## HATEOAS Design

HATEOAS (Hypermedia As The Engine Of Application State) means that a client
should be able to interact with the API using only the links embedded in each
response. It never constructs a URL itself.

### How it works in this project

Every API response contains a `links` object that advertises **exactly what
actions are currently available**:

| Link | Present when | Purpose |
|---|---|---|
| `links.new_game` | Always | Start a fresh game |
| `links.moves` | Game in progress | One URL per empty cell — following it makes that move |
| `links.ai_move` | Current player is an AI | Pre-computed best-move URL; client follows it automatically |

The client (`site.js`) is intentionally dumb. On startup it calls
`/api/new`, then for every subsequent interaction it simply follows a URL from
the `links` object. It has no knowledge of how board strings are formatted,
which cell indices are valid, or how moves are constructed.

### State encoding

All game state is encoded directly in the URL query string:

| Parameter | Values | Meaning |
|---|---|---|
| `board` | 9-char string of `x`, `o`, `b` | Current board position |
| `player` | `x` or `o` | Player who just moved |
| `x_player` | `human`, `minimax`, `random` | Type of X player |
| `o_player` | `human`, `minimax`, `random` | Type of O player |

For example, a mid-game URL looks like:

```
/api/move?player=x&board=xobbxbbbo&x_player=human&o_player=minimax
```

### The `ai_move` link — driving AI turns

When the next player to move is an AI, the server does not wait for the client
to ask. It computes the AI's best move immediately and embeds the resulting URL
as `links.ai_move`:

```json
"links": {
  "new_game": "http://...:9000/api/new",
  "moves": {},
  "ai_move": "http://...:9000/api/move?player=o&board=xobbbbbbb&x_player=human&o_player=minimax"
}
```

The client detects this link, shows a short "thinking" delay (1 second), then
follows the URL. That response may itself contain another `ai_move` link (in
AI-vs-AI mode), driving the next move in turn. The game plays itself by
chaining link-follows until there is no `ai_move` in the response.

This is pure HATEOAS: the server controls the flow; the client just follows
instructions.

### Response structure

```jsonc
{
  "game": {
    "board":    "xobbxbbbo",   // 9-char position string
    "player":   "o",           // whose turn is next (absent when game over)
    "x_player": "human",       // configured type for X
    "o_player": "minimax",     // configured type for O
    "result":   "X Wins",      // present only when game is over
    "win_line": [0, 4, 8]      // present only when there is a winner
  },
  "links": {
    "new_game": "http://...:9000/api/new?x_player=human&o_player=minimax",
    "moves": {
      "2": "http://...:9000/api/move?player=o&board=xoxbxbbbo&...",
      "3": "http://...:9000/api/move?player=o&board=xoboxbbbo&...",
      ...
    },
    "ai_move": "http://...:9000/api/move?..."  // only when next player is AI
  }
}
```

---

## API Reference

### `GET /api/new`

Starts a new game. Returns a game-state response for an empty board with
player X to move.

**Query parameters** (all optional):

| Parameter | Default | Description |
|---|---|---|
| `x_player` | `human` | Player type for X |
| `o_player` | `minimax` | Player type for O |

If X is configured as an AI, the response includes an `ai_move` link so the
frontend kicks off the first move automatically.

---

### `GET /api/move`

Submits a move (the board passed in already contains the move that was made)
and returns the resulting game state.

**Query parameters** (all required):

| Parameter | Description |
|---|---|
| `board` | 9-char board string **after** the move was placed |
| `player` | The player who just moved (`x` or `o`) |
| `x_player` | Player type for X |
| `o_player` | Player type for O |

The server checks whether the move ends the game. If so, `result` and
`win_line` (where applicable) are included and no move links are returned. If
the game continues, the response advances the turn to the other player.

**Error responses:**

| Status | Reason |
|---|---|
| `400` | Missing `board` or `player` parameter |
| `400` | Unknown algorithm name supplied for `x_player` / `o_player` |

---

### `GET /`

Serves the static single-page frontend (`site/index.html`).

---

## AI Algorithms

All AI implementations extend the abstract base class `TicTacToeAlgorithm`,
which enforces a single interface:

```python
def get_move(self, board: list, player: int) -> int:
    # Returns the index (0-8) of the chosen cell
```

Internally, the board is a Python list of 9 integers using the constants:

| Constant | Value | Meaning |
|---|---|---|
| `X` | `1` | X's piece |
| `O` | `-1` | O's piece |
| `N` | `0` | Empty cell |

This integer representation means a win can be detected by summing any line:
`+3` is an X win, `-3` is an O win.

### Minimax (`TicTacToeMiniMax`)

Implements the [Minimax algorithm](https://en.wikipedia.org/wiki/Minimax)
to play perfectly. It recursively evaluates every possible game continuation
and picks the move that maximises the score for the current player (X
maximises, O minimises). It never loses; against a perfect opponent it
always draws.

When multiple moves score equally (which is common early in the game), one is
chosen at random — this prevents the AI from always playing the same game.

### Random (`TicTacToeRandom`)

Selects a move uniformly at random from the available empty cells. Useful for
testing and as the weaker side in AI-vs-AI matches.

---

## Frontend

The UI is a static single-page application served from `site/`.

- **`site/index.html`** — structure and SVG piece/grid definitions
- **`site/static/site.js`** — all game logic
- **`site/static/style.css`** — styling

The SVG board uses `<defs>` to define reusable `x-piece`, `o-piece`, `blank`,
and `grid` symbols. Each cell is rendered as a `<use>` element positioned on a
100×100 grid within a 300×300 viewBox, so the board scales to any screen size.

`site.js` has one job: follow links. Its main function `on_receive_game` parses
a response, renders the board, and decides what to do next:

- If `links.moves` is populated, attach `onclick` handlers so the human can
  click a cell.
- If `links.ai_move` is present, suppress human clicks and schedule an
  automatic follow after a 1-second delay.
- If `game.win_line` is present, animate the winning pieces and draw the
  winning line through them.
- If the result is `"Draw"`, briefly animate all pieces.

The frontend never builds a URL — every URL it ever requests was provided by
the server in a previous response.

---

## Player Configuration

The player-select dropdowns on the home page control the `x_player` and
`o_player` parameters that are passed with every API call.

| Mode | x_player | o_player |
|---|---|---|
| Human vs Minimax AI | `human` | `minimax` |
| Human vs Random AI | `human` | `random` |
| Human vs Human | `human` | `human` |
| Minimax AI vs Human | `minimax` | `human` |
| AI vs AI | `minimax` | `random` (or any combination) |

In AI-vs-AI mode the game plays itself: each response contains an `ai_move`
link which the frontend follows after a 1-second delay, creating a visible
sequence of moves.

---

## Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/richardadalton/tic-tac-toe.git
cd tic-tac-toe
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Running Locally

### With Python directly

```bash
python tictactoe.py
```

### With Docker Compose

```bash
docker compose up --build
```

Both options serve the app on **port 9000**, reachable at:

```
http://localhost:9000
http://<your-local-ip>:9000
```

The port can be overridden with an environment variable (Python only):

```bash
PORT=8080 python tictactoe.py
```

---

## Deployment

The project supports two deployment targets. Both use the same `Dockerfile`
and `compose.yml`; in production the Flask dev server is replaced by
[Gunicorn](https://gunicorn.org), which is included in `requirements.txt`.

### Fly.io (public)

The app is deployed at **https://restactoe.fly.dev**.

`fly.toml` is committed to the repository and already configured. Deploying
is a single command:

```bash
fly deploy
```

Fly.io builds the Docker image remotely and rolls it out. The app runs on a
`shared-cpu-1x 256 MB` machine in the `lhr` (London) region with
scale-to-zero enabled, so there are no idle charges.

**First-time setup** (already done — kept here for reference):

```bash
brew install flyctl       # install the Fly CLI
fly auth login
fly apps create restactoe
fly deploy
```

**Behind a proxy — `ProxyFix`**

Fly.io terminates TLS at its edge and forwards traffic to the container as
plain HTTP. Without correction, `request.url_root` would return `http://`
and all generated move links would be blocked by the browser as mixed
content. `ProxyFix` in `tictactoe.py` reads the `X-Forwarded-Proto: https`
header Fly.io injects and rewrites the scheme accordingly. It is harmless in
environments where that header is absent (plain `python tictactoe.py` or
`docker compose up` locally).

---

## Testing

Install pytest (included in the virtual environment after `pip install -r requirements.txt` once pytest has been added):

```bash
pip install pytest
python -m pytest tests/ -v
```

The test suite contains **100 tests** across four files:

| File | What it covers |
|---|---|
| `tests/test_tictactoe.py` | Core game primitives (`make_move`, `available_moves`, `score`, `other_player`) |
| `tests/test_utils.py` | All 8 win patterns for `score` and `winning_line`; edge cases for empty/full/won boards; `make_move` immutability |
| `tests/test_minimax.py` | Tactical move choices; minimax never loses vs random (50 games each as X and O); AI vs AI always draws |
| `tests/test_random.py` | Random AI always picks a valid empty cell |
| `tests/test_api.py` | All Flask endpoints; string conversion helpers; HATEOAS link presence/absence; win/draw results; error handling (400s) |
