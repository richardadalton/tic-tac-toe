import unittest
from tictactoe_minimax import *
from constants import *


class test_tictactoe(unittest.TestCase):

    def test_make_a_move(self):
        board = EMPTY_BOARD
        board = make_move(board, 4, X)
        board = make_move(board, 8, O)

        expected = [
            N, N, N,
            N, X, N,
            N, N, O
        ]
        self.assertListEqual(expected, board)


    def test_available_moves(self):
        board = [
            X, N, X,
            N, O, N,
            O, N, X
        ]
        moves = available_moves(board)
        self.assertListEqual([1, 3, 5, 7], moves)


    def test_toggle_player(self):
        self.assertEqual(O, other_player(X))
        self.assertEqual(X, other_player(O))


    def test_recognises_win_for_X(self):
        board = [
                X, O, N,
                N, X, O,
                N, N, X
            ]
        self.assertEqual(X, score(board))


    def test_recognises_win_for_O(self):
        board = [
                X, O, O,
                N, X, O,
                X, X, O
            ]
        self.assertEqual(O, score(board))


    def test_recognises_draw(self):
        board = [
            X, X, O,
            O, O, X,
            X, X, O
            ]
        self.assertEqual(N, score(board))


    def test_recognises_no_result_yet(self):
        board = [
                N, N, N,
                N, X, O,
                N, O, O
            ]
        self.assertEqual(None, score(board))


