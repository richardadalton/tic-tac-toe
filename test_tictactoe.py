import unittest
from tictactoe_minimax import *


class test_tictactoe(unittest.TestCase):

    def test_finds_win_for_X(self):
        board = [
                X, O, N,
                N, X, O,
                N, N, X
            ]
        self.assertEqual(X, score(board))


    def test_finds_win_for_O(self):
        board = [
                X, O, O,
                N, X, O,
                X, X, O
            ]
        self.assertEqual(O, score(board))


    def test_finds_no_winner(self):
        board = [
                N, N, N,
                N, X, O,
                N, O, O
            ]
        self.assertEqual(N, score(board))


    def test_make_a_move(self):
        board = empty_board
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


    def test_a_full_game_played_perfectly_is_a_draw(self):
        board = empty_board
        result = minimax(board, X)
        print(result)
        self.assertEqual(N, result)


    def test_can_see_final_result(self):
        board = [
                X, N, N,
                N, O, N,
                O, N, X
            ]
        result = minimax(board, X)
        self.assertEqual(result, X)



    def test_can_see_winning_move(self):
        board = [
                X, O, N,
                X, O, N,
                N, N, N
            ]
        move = get_move(board, X)
        self.assertEqual(6, move)


    def test_can_see_blocking_move(self):
        board = [
                X, N, N,
                X, O, N,
                O, N, N
            ]
        move = get_move(board, X)
        self.assertEqual(2, move)


    def test_forced_move_for_O(self):
        board = [
                N, N, N,
                N, O, N,
                X, X, N
            ]
        move = get_move(board, O)
        self.assertEqual(8, move)
