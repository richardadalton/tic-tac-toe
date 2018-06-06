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

function click_square(num) {
    alert(num)
}

function show_piece(piece, position) {
    var  svgns = "http://www.w3.org/2000/svg";
    var  xlinkns = "http://www.w3.org/1999/xlink";

    var  g = document.getElementById("board");
    var  use = document.createElementNS(svgns, "use");

    if (piece == 1) {
        use.setAttributeNS(xlinkns, "href", "#x-piece");
    } else if (piece == -1) {
        use.setAttributeNS(xlinkns, "href", "#o-piece");
    }

    use.setAttribute("x", position[0]);
    use.setAttribute("y", position[1]);
    g.appendChild(use);
}


Object.keys(board_pieces).forEach(function(key) {
    show_piece(board_pieces[key], board_positions[key]);
});
