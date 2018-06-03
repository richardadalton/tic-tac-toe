# Players X, O, None
X = 1
O = -1
N = 0

characters = {X: "X", O: "O", N: " "}

top_row = [0, 1, 2]
middle_row = [3, 4, 5]
bottom_row = [6, 7, 8]
left_col = [0, 3, 6]
middle_col = [1, 4, 7]
right_col = [2, 5, 8]
diagonal1 = [0, 4, 8]
diagonal2 = [2, 4, 6]

patterns = [top_row, middle_row, bottom_row, left_col, middle_col, right_col, diagonal1, diagonal2]

empty_board = [0 for i in range(9)]


def make_move(board, move, player):
    new_board = board.copy()
    new_board[move] = player
    return new_board


def score(board):
    for pattern in patterns:
        s = sum([board[i] for i in pattern])
        if s == 3:
            return X
        elif s == -3:
            return O
    return N


def score2(board):
    for pattern in patterns:
        s = sum([board[i] for i in pattern])
        if s == 3:
            return X
        elif s == -3:
            return O
    return N



def available_moves(board):
    this_score = score(board)

    if this_score != N:
        return []
    else:
        return [i for i in range(9) if board[i] == N]


def other_player(player):
    return -player


def minimax(board, player):
    moves = available_moves(board)

    if moves == []:
        return score(board)

    move_scores = {}
    for move in moves:
        board_after_move = make_move(board, move, player)
        score_after_move = minimax(board_after_move, other_player(player))
        move_scores[move] = score_after_move * player

    this_score = max(move_scores.values())
    return this_score * player


def get_move(board, player):
    moves = available_moves(board)

    move_scores = {}
    for move in moves:
        board_after_move = make_move(board, move, player)
        score_after_move = minimax(board_after_move, other_player(player))
        move_scores[move] = score_after_move * player

    # The Key of the highest scoring move, is the move itself.
    return max(move_scores, key=move_scores.get)


def display_board(board):
    def display_row(board, row):
        row_moves = [characters[board[i]] for i in row]
        print("|".join(row_moves))

    display_row(board, top_row)
    print("-----")
    display_row(board, middle_row)
    print("-----")
    display_row(board, bottom_row)


def main():
    board = empty_board
    player = X
    while True:
        print("")
        print("----------------------------")
        print("")

        display_board(board)

        if available_moves(board) == []:
            print("Game Over")
            break

        if player == X:
            move = int(input("Enter Move: "))
        else:
            move = get_move(board, O)

        board = make_move(board, move, player)
        player = other_player(player)


if __name__ == "__main__":
    main()