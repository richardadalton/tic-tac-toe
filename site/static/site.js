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


function on_receive_game(data) {
    data = JSON.parse(data);

    var board = data['game']['board']
    var moves = data['links']['moves']
    var new_game = data['links']['new_game']
    var result = data['game']['result'] || ''

    var resultEl = document.getElementById("result_text");
    if (resultEl) {
        resultEl.textContent = result;
    }

    // Clear existing SVG pieces so items don't stack and cover the new_game link
    var g = document.getElementById("board");
    if (g) {
        var pieces = g.querySelectorAll('.piece, .win-line');
        pieces.forEach(function (p) {
            g.removeChild(p);
        });
    }

    for (i=0; i<9; i++) {
        show_piece(board, i, moves)
    }

    // Draw a line through the winning cells, or flash all symbols on a draw
    var win_line = data['game']['win_line'] || null;
    var isDraw = (result && result.toLowerCase() === 'draw');
    if (win_line) {
        // Highlight winning pieces with a glow
        highlight_winning_pieces(win_line);
        // Delay the strike-through line so the glow animation plays first
        setTimeout(function () {
            draw_win_line(win_line);
        }, 600);
    } else if (isDraw) {
        // Flash all non-blank symbols in a draw
        highlight_all_pieces(board);
    }

    // TODO: This doesn't work yet, could just reload the page, but want to use api/new
    var  ng = document.getElementById("new_game_link");
    ng.setAttribute("onclick", "click_square('" + new_game + "')");
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


function click_square(move) {
    get_game(move, on_receive_game);
}

// On page load, start a new game
get_game("/api/new", on_receive_game)
