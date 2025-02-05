from tictactoe_random import TicTacToeRandom
from tictactoe_minimax import TicTacToeMiniMax
from utils import *

# Allows tictactoe algorithms to be run using a simple console interface.
# This helps with debugging.

def console_display_board(board):
    def display_row(board, row):
        row_moves = [characters[board[i]] for i in row]
        print("|".join(row_moves))

    display_row(board, TOP_ROW)
    print("-----")
    display_row(board, MIDDLE_ROW)
    print("-----")
    display_row(board, BOTTOM_ROW)

def main():
    board = EMPTY_BOARD
    player = X
    while True:
        print("")
        print("----------------------------")
        print("")

        console_display_board(board)

        if available_moves(board) == []:
            print("Game Over")
            break

        if player == X:
            move = int(input("Enter Move: "))
        else:
            ai = TicTacToeMiniMax()
            move = ai.get_move(board, O)

        board = make_move(board, move, player)
        player = other_player(player)


if __name__ == "__main__":
    main()