import unittest
from tictactoe_random import TicTacToeRandom
from utils import available_moves
from constants import *


class TestTicTacToeRandom(unittest.TestCase):

    def setUp(self):
        self.ai = TicTacToeRandom()

    def test_get_move_returns_a_valid_cell_index(self):
        board = EMPTY_BOARD.copy()
        move = self.ai.get_move(board, X)
        self.assertIn(move, range(9))

    def test_get_move_only_picks_an_empty_cell(self):
        board = EMPTY_BOARD.copy()
        move = self.ai.get_move(board, X)
        self.assertEqual(N, board[move])

    def test_get_move_never_picks_an_occupied_cell(self):
        # Cells 0-5 are occupied; only 6, 7, 8 are available
        board = [X, O, X, O, X, O, N, N, N]
        for _ in range(50):
            move = self.ai.get_move(board, O)
            self.assertIn(move, [6, 7, 8])

    def test_get_move_returns_the_only_available_cell(self):
        # Only cell 8 is empty
        board = [X, O, X, O, X, O, O, X, N]
        move = self.ai.get_move(board, O)
        self.assertEqual(8, move)

    def test_get_move_returns_a_cell_within_available_moves(self):
        board = [X, N, X, N, O, N, O, N, X]
        expected_moves = available_moves(board)
        for _ in range(30):
            move = self.ai.get_move(board, O)
            self.assertIn(move, expected_moves)

