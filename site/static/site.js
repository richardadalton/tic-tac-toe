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

    var board = data['board']
    var moves = data['links']['moves']
    var new_game = data['links']['new_game']

    // TODO: This appends extra SVG elements, it doesn't replace
    for (i=0; i<9; i++) {
        show_piece(board, i, moves)
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
    var piece = board.charAt(i);

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
    use.setAttribute("x", coords[0]);
    use.setAttribute("y", coords[1]);

    if (position in moves) {
        use.setAttribute("onclick", "click_square('" + moves[position] + "')");
    }
    g.appendChild(use);
}


function click_square(move) {
    get_game(move, on_receive_game);
}

// On page load, start a new game
get_game("http://127.0.0.1:5000/api/new", on_receive_game)