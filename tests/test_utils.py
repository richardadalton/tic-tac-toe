import unittest
from utils import score, winning_line, make_move, available_moves, other_player
from constants import *


class TestScore(unittest.TestCase):

    def test_score_top_row_x(self):
        board = [X, X, X, N, O, N, N, N, O]
        self.assertEqual(X, score(board))

    def test_score_middle_row_x(self):
        board = [N, O, N, X, X, X, N, N, O]
        self.assertEqual(X, score(board))

    def test_score_bottom_row_o(self):
        board = [X, N, X, N, X, N, O, O, O]
        self.assertEqual(O, score(board))

    def test_score_left_col_x(self):
        board = [X, O, N, X, O, N, X, N, N]
        self.assertEqual(X, score(board))

    def test_score_middle_col_o(self):
        board = [X, O, N, N, O, X, N, O, N]
        self.assertEqual(O, score(board))

    def test_score_right_col_x(self):
        board = [O, N, X, N, O, X, N, N, X]
        self.assertEqual(X, score(board))

    def test_score_diagonal1_o(self):
        board = [O, X, X, N, O, N, X, N, O]
        self.assertEqual(O, score(board))

    def test_score_diagonal2_x(self):
        board = [N, O, X, N, X, N, X, N, O]
        self.assertEqual(X, score(board))

    def test_score_draw(self):
        board = [X, X, O, O, O, X, X, X, O]
        self.assertEqual(N, score(board))

    def test_score_no_result_yet(self):
        board = [N, N, N, N, X, O, N, O, O]
        self.assertIsNone(score(board))

    def test_score_empty_board_is_no_result(self):
        self.assertIsNone(score(EMPTY_BOARD))


class TestWinningLine(unittest.TestCase):

    def test_winning_line_top_row(self):
        board = [X, X, X, N, O, N, N, N, O]
        self.assertEqual(TOP_ROW, winning_line(board))

    def test_winning_line_middle_row(self):
        board = [N, O, N, X, X, X, N, N, O]
        self.assertEqual(MIDDLE_ROW, winning_line(board))

    def test_winning_line_bottom_row(self):
        board = [X, N, X, N, X, N, O, O, O]
        self.assertEqual(BOTTOM_ROW, winning_line(board))

    def test_winning_line_left_col(self):
        board = [X, O, N, X, O, N, X, N, N]
        self.assertEqual(LEFT_COL, winning_line(board))

    def test_winning_line_middle_col(self):
        board = [X, O, N, N, O, X, N, O, N]
        self.assertEqual(MIDDLE_COL, winning_line(board))

    def test_winning_line_right_col(self):
        board = [O, N, X, N, O, X, N, N, X]
        self.assertEqual(RIGHT_COL, winning_line(board))

    def test_winning_line_diagonal1(self):
        board = [O, X, X, N, O, N, X, N, O]
        self.assertEqual(DIAGONAL1, winning_line(board))

    def test_winning_line_diagonal2(self):
        board = [N, O, X, N, X, N, X, N, O]
        self.assertEqual(DIAGONAL2, winning_line(board))

    def test_winning_line_returns_none_when_no_winner(self):
        board = [N, N, N, N, X, O, N, O, O]
        self.assertIsNone(winning_line(board))

    def test_winning_line_returns_none_on_draw(self):
        board = [X, X, O, O, O, X, X, X, O]
        self.assertIsNone(winning_line(board))

    def test_winning_line_returns_none_on_empty_board(self):
        self.assertIsNone(winning_line(EMPTY_BOARD))


class TestAvailableMoves(unittest.TestCase):

    def test_available_moves_empty_board_returns_all_nine(self):
        self.assertEqual(list(range(9)), available_moves(EMPTY_BOARD))

    def test_available_moves_full_board_returns_empty(self):
        # xxoooxxxo — a drawn game, all cells filled
        board = [X, X, O, O, O, X, X, X, O]
        self.assertEqual([], available_moves(board))

    def test_available_moves_won_board_returns_empty(self):
        # Once someone wins there are no more valid moves
        board = [X, X, X, N, O, N, N, N, O]
        self.assertEqual([], available_moves(board))

    def test_available_moves_returns_correct_indices(self):
        board = [X, N, X, N, O, N, O, N, X]
        self.assertEqual([1, 3, 5, 7], available_moves(board))


class TestMakeMove(unittest.TestCase):

    def test_make_move_places_player_on_board(self):
        board = EMPTY_BOARD.copy()
        new_board = make_move(board, 4, X)
        self.assertEqual(X, new_board[4])

    def test_make_move_does_not_mutate_original_board(self):
        original = EMPTY_BOARD.copy()
        snapshot = original.copy()
        make_move(original, 4, X)
        self.assertEqual(snapshot, original)

    def test_make_move_returns_new_board_object(self):
        original = EMPTY_BOARD.copy()
        new_board = make_move(original, 0, X)
        self.assertIsNot(original, new_board)

    def test_make_move_leaves_other_cells_unchanged(self):
        board = [X, N, N, N, O, N, N, N, N]
        new_board = make_move(board, 8, X)
        self.assertEqual(board[:8], new_board[:8])


class TestOtherPlayer(unittest.TestCase):

    def test_other_player_of_x_is_o(self):
        self.assertEqual(O, other_player(X))

    def test_other_player_of_o_is_x(self):
        self.assertEqual(X, other_player(O))

    def test_other_player_is_symmetric(self):
        self.assertEqual(X, other_player(other_player(X)))
        self.assertEqual(O, other_player(other_player(O)))

