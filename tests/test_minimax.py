import unittest
from tictactoe_minimax import *
from tictactoe_random import TicTacToeRandom
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
        # O can force a win from this position — verify the outcome, not the specific move,
        # since minimax may choose between multiple equally-optimal winning moves
        result = ai.minimax(board, O)
        self.assertEqual(O, result)


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


    def test_get_move_returns_an_empty_cell(self):
        board = [X, O, N, N, X, N, N, N, N]
        ai = TicTacToeMiniMax()
        move = ai.get_move(board, O)
        self.assertIn(move, range(9))
        self.assertEqual(N, board[move])

    def test_get_move_returns_none_on_finished_board(self):
        # Board already won by X (top row)
        board = [X, X, X, N, O, N, N, N, O]
        ai = TicTacToeMiniMax()
        self.assertIsNone(ai.get_move(board, O))

    def _play_game(self, x_ai, o_ai):
        """Play a complete game, returning the final score."""
        board = EMPTY_BOARD.copy()
        current_player = X
        while True:
            result = score(board)
            if result is not None:
                return result
            ai = x_ai if current_player == X else o_ai
            move = ai.get_move(board, current_player)
            board = make_move(board, move, current_player)
            current_player = other_player(current_player)

    def test_minimax_vs_minimax_always_draws(self):
        ai = TicTacToeMiniMax()
        result = self._play_game(ai, ai)
        self.assertEqual(N, result)

    def test_minimax_as_x_never_loses_against_random(self):
        minimax = TicTacToeMiniMax()
        random_ai = TicTacToeRandom()
        for _ in range(50):
            result = self._play_game(minimax, random_ai)
            # Minimax (X) must win or draw — never lose
            self.assertNotEqual(O, result)

    def test_minimax_as_o_never_loses_against_random(self):
        minimax = TicTacToeMiniMax()
        random_ai = TicTacToeRandom()
        for _ in range(50):
            result = self._play_game(random_ai, minimax)
            # Minimax (O) must win or draw — never lose
            self.assertNotEqual(X, result)

