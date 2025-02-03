# Players X, O, None
X = 1
O = -1
N = 0

characters = {X: "X", O: "O", N: " "}

TOP_ROW = [0, 1, 2]
MIDDLE_ROW = [3, 4, 5]
BOTTOM_ROW = [6, 7, 8]
LEFT_COL = [0, 3, 6]
MIDDLE_COL = [1, 4, 7]
RIGHT_COL = [2, 5, 8]
DIAGONAL1 = [0, 4, 8]
DIAGONAL2 = [2, 4, 6]
WIN_PATTERNS = [TOP_ROW, MIDDLE_ROW, BOTTOM_ROW, LEFT_COL, MIDDLE_COL, RIGHT_COL, DIAGONAL1, DIAGONAL2]

EMPTY_BOARD = [0 for i in range(9)]

