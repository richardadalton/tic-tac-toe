# Multiplayer Design Notes

*Recorded March 2026. Hypothetical — not yet implemented.*

---

## The core problem

The current HATEOAS model is **single-client, request-driven**. It works perfectly
for one browser because that browser is the only actor — it always has the latest
state because *it* just caused it. There is no concept of "waiting for someone else
to move."

With two browsers, Player 2's browser has no mechanism to learn that Player 1 has
moved. It just sits there with a stale board.

---

## Why the current model can't stretch to cover this

The state lives entirely in URLs. After Player 1 makes a move, the new board state
exists in the response Player 1's browser received. Player 2's browser has no way
to get that URL without:

- **Out-of-band communication** — Player 1 manually copies and sends the URL to
  Player 2 each turn. Technically correct, completely impractical.
- **Server-side state** — the server remembers what the current board is, so
  Player 2 can ask "what's the state now?"

There is no third option. The stateless model *requires* the same browser to make
every request, because the browser *is* the state store.

---

## The minimal fix that preserves the HATEOAS spirit

Two things need to be added to the server:

1. **A game session** — a short ID (`/api/game/abc123`) that both browsers can
   reference.
2. **A stored current state** — the server holds the latest board for that session
   (a dict in memory, or Redis).

The HATEOAS link model handles the rest almost unchanged. The server returns
different links depending on whose turn it is:

**Active player's response** (it's your turn):
```json
{
  "game": { "board": "xbbbbbbbb", "player": "o" },
  "links": {
    "moves": {
      "0": "/api/game/abc123/move?...",
      "1": "/api/game/abc123/move?...",
      ...
    }
  }
}
```

**Inactive player's response** (waiting for opponent):
```json
{
  "game": { "board": "xbbbbbbbb", "player": "o" },
  "links": {
    "poll": "/api/game/abc123/state"
  }
}
```

The inactive browser follows `links.poll` on a timer — the same pattern as the
current `links.ai_move` chain. When the opponent moves, the next poll response
will have `links.moves` instead of `links.poll`. The client logic barely changes.

---

## The three realistic implementation approaches

### 1. Polling (extends current model most naturally)

As above. Player 2's browser follows `links.poll` every second or two. Simple,
but has latency equal to the poll interval and generates constant requests.

### 2. Server-Sent Events (SSE) — recommended

Player 2's browser opens a persistent connection to `/api/game/abc123/stream`.
The server pushes the new game state the moment Player 1's move is processed.
Real-time, one-way (server → client), fits naturally with HTTP, and Flask
supports it natively. The right answer for this app — a small upgrade from
polling with no protocol change.

### 3. WebSockets

Full bidirectional real-time. Needs something like `flask-socketio`. Overkill
for turn-based Tic-Tac-Toe where moves happen seconds apart.

---

## The deeper HATEOAS tension

HATEOAS was designed around a **single client** navigating application state.
The philosophy — "the client needs no prior knowledge; it just follows links" —
holds perfectly for one browser. With two clients, you have a **shared state
synchronisation problem**, which is outside what HATEOAS addresses.

The polling model preserves the spirit best: both browsers start at the same
URL, and the server's response links tell each browser exactly what to do next.
Neither browser needs any hard-coded knowledge of the game flow. The server is
still the engine of application state — just now driving two clients
simultaneously rather than one.

---

## Options comparison

| Approach | Server state needed | Real-time | Complexity | Fits current model |
|---|---|---|---|---|
| Out-of-band URL passing | None | No | Impractical | ✅ Pure HATEOAS |
| Polling + `links.poll` | Current board per game | ~1s delay | Low | ✅ Good fit |
| SSE | Current board per game | Yes | Medium | ✅ Good fit |
| WebSockets | Current board per game | Yes | High | ❌ Different model |

