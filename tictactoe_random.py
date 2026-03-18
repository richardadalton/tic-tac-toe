from utils import *
from tictactoe_algorithm import TicTacToeAlgorithm
import random

class TicTacToeRandom(TicTacToeAlgorithm):
    def get_move(self, board, player):
        return random.choice(available_moves(board))
