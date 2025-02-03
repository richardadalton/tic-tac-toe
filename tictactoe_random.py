from utils import *
from tictactoe_algorithm import TicTacToeAlgorithm
import random

class TicTacToeRandom(TicTacToeAlgorithm):
    def get_move(self, board, player):
        moves = available_moves(board)
        move = random.choice(moves)
        return move
