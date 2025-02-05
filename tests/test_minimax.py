import unittest
from tictactoe_minimax import *
from constants import *


class test_minimax(unittest.TestCase):

    def test_can_see_winning_move(self):
        board = [
                X, O, N,
                X, O, N,
                N, N, N
            ]
        ai = TicTacToeMiniMax()
        move = ai.get_move(board, X)
        self.assertEqual(6, move)


    def test_forced_move_for_X(self):
        board = [
                X, N, N,
                X, O, N,
                O, N, N
            ]
        ai = TicTacToeMiniMax()
        move = ai.get_move(board, X)
        self.assertEqual(2, move)


    def test_forced_move_for_O(self):
        board = [
                N, N, N,
                N, O, N,
                X, X, N
            ]
        ai = TicTacToeMiniMax()
        move = ai.get_move(board, O)
        self.assertEqual(8, move)


    def test_find_a_win(self):
        board = [
                X, O, X,
                N, O, N,
                N, N, X
            ]
        ai = TicTacToeMiniMax()
        move = ai.get_move(board, O)
        self.assertEqual(5, move)


    def test_perfect_game_is_a_draw(self):
        board = [
                N, N, N,
                N, N, N,
                N, N, N
            ]
        ai = TicTacToeMiniMax()
        result = ai.minimax(board, X)
        self.assertEqual(N, result)


    def test_O_mistake_X_wins(self):
        board = [
                X, O, N,
                N, N, N,
                N, N, N
            ]
        ai = TicTacToeMiniMax()
        result = ai.minimax(board, X)
        self.assertEqual(X, result)
