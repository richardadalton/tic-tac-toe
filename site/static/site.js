function get_game(url, on_success) {
    var xhr = new XMLHttpRequest();

    xhr.onload = function () {
        on_success(xhr.responseText);
    };

    xhr.open('GET', url);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader("Authorization", "Token " + localStorage.authtoken);
    xhr.send();
}


// Holds the pending auto-play timeout so it can be cancelled on New Game
var auto_play_timer = null;

function on_receive_game(data) {
    data = JSON.parse(data);

    var board    = data['game']['board'];
    var moves    = data['links']['moves'];
    var ai_move  = data['links']['ai_move'] || null;
    var result   = data['game']['result'] || '';

    var resultEl = document.getElementById("result_text");
    if (resultEl) {
        resultEl.textContent = result;
    }

    // Clear existing SVG pieces
    var g = document.getElementById("board");
    if (g) {
        var pieces = g.querySelectorAll('.piece, .win-line');
        pieces.forEach(function (p) { g.removeChild(p); });
    }

    // When it's an AI's turn, don't attach onclick to squares —
    // the AI will auto-play and we don't want the human to interfere
    var effective_moves = ai_move ? {} : moves;
    for (i=0; i<9; i++) {
        show_piece(board, i, effective_moves);
    }

    // Win / draw animations
    var win_line = data['game']['win_line'] || null;
    var isDraw   = (result && result.toLowerCase() === 'draw');
    if (win_line) {
        highlight_winning_pieces(win_line);
        setTimeout(function () { draw_win_line(win_line); }, 600);
    } else if (isDraw) {
        highlight_all_pieces(board);
    }

    // Cancel any previously scheduled auto-play before scheduling a new one
    if (auto_play_timer) {
        clearTimeout(auto_play_timer);
        auto_play_timer = null;
    }

    if (ai_move) {
        // Show which player is thinking, then follow the pre-computed move link
        var player = data['game']['player'];
        if (resultEl) {
            resultEl.textContent = (player === 'x' ? 'X' : 'O') + ' is thinking…';
        }
        auto_play_timer = setTimeout(function () {
            auto_play_timer = null;
            get_game(ai_move, on_receive_game);
        }, 1000);
    }

    // New game button always reads the current player-select values
    var ng = document.getElementById("new_game_link");
    ng.onclick = start_new_game;
}


function show_piece(board, position, moves) {
    var board_positions = {
        0: [0, 0],
        1: [100, 0],
        2: [200, 0],
        3: [0, 100],
        4: [100, 100],
        5: [200, 100],
        6: [0, 200],
        7: [100, 200],
        8: [200, 200],
    };
    var coords = board_positions[position];
    var piece = board.charAt(position);

    var  svgns = "http://www.w3.org/2000/svg";
    var  xlinkns = "http://www.w3.org/1999/xlink";

    var  g = document.getElementById("board");
    var  use = document.createElementNS(svgns, "use");

    if (piece == "x") {
        use.setAttributeNS(xlinkns, "href", "#x-piece");
    } else if (piece == "o") {
        use.setAttributeNS(xlinkns, "href", "#o-piece");
    } else {
        use.setAttributeNS(xlinkns, "href", "#blank");
    }
    use.setAttribute("class", "piece")
    use.setAttribute("data-position", position);
    use.setAttribute("x", coords[0]);
    use.setAttribute("y", coords[1]);

    if (position in moves) {
        use.setAttribute("onclick", "click_square('" + moves[position] + "')");
    }
    g.appendChild(use);
}


function highlight_winning_pieces(win_line) {
    var g = document.getElementById("board");
    var pieces = g.querySelectorAll('.piece');
    pieces.forEach(function (p) {
        var pos = parseInt(p.getAttribute("data-position"), 10);
        if (win_line.indexOf(pos) !== -1) {
            p.setAttribute("class", "piece winning");
        }
    });
}


function highlight_all_pieces(board) {
    var g = document.getElementById("board");
    var pieces = g.querySelectorAll('.piece');
    pieces.forEach(function (p) {
        var pos = parseInt(p.getAttribute("data-position"), 10);
        // Only add class for non-blank pieces
        if (board.charAt(pos) !== 'b') {
            p.setAttribute("class", "piece winning");
            // Remove the class after the animation ends so it doesn't persist
            setTimeout(function () { p.setAttribute("class", "piece"); }, 500);
        }
    });
}


function draw_win_line(win_line) {
    // Center of each board cell (each cell is 100x100)
    var cell_centers = {
        0: [50, 50],   1: [150, 50],   2: [250, 50],
        3: [50, 150],  4: [150, 150],  5: [250, 150],
        6: [50, 250],  7: [150, 250],  8: [250, 250],
    };

    var start = cell_centers[win_line[0]];
    var end   = cell_centers[win_line[2]];

    var svgns = "http://www.w3.org/2000/svg";
    var g = document.getElementById("board");
    var line = document.createElementNS(svgns, "line");

    line.setAttribute("x1", start[0]);
    line.setAttribute("y1", start[1]);
    line.setAttribute("x2", end[0]);
    line.setAttribute("y2", end[1]);
    line.setAttribute("class", "win-line");

    g.appendChild(line);
}


function start_new_game() {
    if (auto_play_timer) {
        clearTimeout(auto_play_timer);
        auto_play_timer = null;
    }
    var xPlayer = document.getElementById("x_player").value;
    var oPlayer = document.getElementById("o_player").value;
    get_game("/api/new?x_player=" + xPlayer + "&o_player=" + oPlayer, on_receive_game);
}

function click_square(move) {
    get_game(move, on_receive_game);
}

// On page load, start a new game with the default player selections
start_new_game();
