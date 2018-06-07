
function click_square(move) {
    window.location.href = "/?move=" + move;
}

function show_piece(position) {
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
    var piece = board[i];

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
    use.setAttribute("x", coords[0]);
    use.setAttribute("y", coords[1]);

    if (position in moves) {
        use.setAttribute("onclick", "click_square('" + moves[position] + "')");
    }
    g.appendChild(use);
}

for (i=0; i<9; i++) {
    show_piece(i);
}
