import unittest
from tictactoe import app, str_to_board, board_to_str, str_to_player, player_to_str, score_to_result
from constants import *


class TestStringConversions(unittest.TestCase):

    def test_str_to_board_all_blank(self):
        self.assertEqual([N] * 9, str_to_board('bbbbbbbbb'))

    def test_str_to_board_x_and_o(self):
        board = str_to_board('xobbxbbbo')
        self.assertEqual([X, O, N, N, X, N, N, N, O], board)

    def test_str_to_board_maps_x_correctly(self):
        board = str_to_board('xbbbbbbbb')
        self.assertEqual(X, board[0])

    def test_str_to_board_maps_o_correctly(self):
        board = str_to_board('bbbbbbbbo')
        self.assertEqual(O, board[8])

    def test_str_to_board_maps_b_to_n(self):
        board = str_to_board('bbbbbbbbb')
        self.assertTrue(all(c == N for c in board))

    def test_board_to_str_round_trip(self):
        original = [X, O, N, N, X, N, O, N, N]
        self.assertEqual(original, str_to_board(board_to_str(original)))

    def test_board_to_str_all_blank(self):
        self.assertEqual('bbbbbbbbb', board_to_str([N] * 9))

    def test_str_to_player_x(self):
        self.assertEqual(X, str_to_player('x'))

    def test_str_to_player_o(self):
        self.assertEqual(O, str_to_player('o'))


    def test_player_to_str_round_trip_x(self):
        self.assertEqual(X, str_to_player(player_to_str(X)))

    def test_player_to_str_round_trip_o(self):
        self.assertEqual(O, str_to_player(player_to_str(O)))

    def test_score_to_result_x_wins(self):
        self.assertEqual('X Wins', score_to_result(X))

    def test_score_to_result_o_wins(self):
        self.assertEqual('O Wins', score_to_result(O))

    def test_score_to_result_draw(self):
        self.assertEqual('Draw', score_to_result(N))

    def test_score_to_result_none_when_game_in_progress(self):
        self.assertIsNone(score_to_result(None))


class TestAPINewGame(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_new_game_returns_200(self):
        r = self.client.get('/api/new')
        self.assertEqual(200, r.status_code)

    def test_new_game_starts_with_player_x(self):
        r = self.client.get('/api/new')
        self.assertEqual('x', r.get_json()['game']['player'])

    def test_new_game_board_is_all_blank(self):
        r = self.client.get('/api/new')
        self.assertEqual('bbbbbbbbb', r.get_json()['game']['board'])

    def test_new_game_has_nine_move_links_for_human_vs_human(self):
        r = self.client.get('/api/new?x_player=human&o_player=human')
        self.assertEqual(9, len(r.get_json()['links']['moves']))

    def test_new_game_default_x_player_is_human(self):
        r = self.client.get('/api/new')
        self.assertEqual('human', r.get_json()['game']['x_player'])

    def test_new_game_default_o_player_is_minimax(self):
        r = self.client.get('/api/new')
        self.assertEqual('minimax', r.get_json()['game']['o_player'])

    def test_new_game_respects_custom_player_config(self):
        r = self.client.get('/api/new?x_player=random&o_player=human')
        data = r.get_json()['game']
        self.assertEqual('random', data['x_player'])
        self.assertEqual('human', data['o_player'])

    def test_new_game_includes_ai_move_link_when_x_is_ai(self):
        r = self.client.get('/api/new?x_player=minimax&o_player=human')
        self.assertIn('ai_move', r.get_json()['links'])

    def test_new_game_no_ai_move_link_when_x_is_human(self):
        r = self.client.get('/api/new?x_player=human&o_player=human')
        self.assertNotIn('ai_move', r.get_json()['links'])

    def test_new_game_includes_new_game_link(self):
        r = self.client.get('/api/new')
        self.assertIn('new_game', r.get_json()['links'])

    def test_new_game_has_no_result(self):
        r = self.client.get('/api/new')
        self.assertNotIn('result', r.get_json()['game'])


class TestAPIMove(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_move_returns_200(self):
        r = self.client.get('/api/move?player=x&board=xbbbbbbbb&x_player=human&o_player=human')
        self.assertEqual(200, r.status_code)

    def test_move_advances_turn_to_o_after_x_plays(self):
        r = self.client.get('/api/move?player=x&board=xbbbbbbbb&x_player=human&o_player=human')
        self.assertEqual('o', r.get_json()['game']['player'])

    def test_move_advances_turn_to_x_after_o_plays(self):
        r = self.client.get('/api/move?player=o&board=xobbbbbbb&x_player=human&o_player=human')
        self.assertEqual('x', r.get_json()['game']['player'])

    def test_move_missing_board_param_returns_400(self):
        r = self.client.get('/api/move?player=x')
        self.assertEqual(400, r.status_code)

    def test_move_missing_player_param_returns_400(self):
        r = self.client.get('/api/move?board=xbbbbbbbb')
        self.assertEqual(400, r.status_code)

    def test_winning_move_returns_x_wins_result(self):
        # X wins top row: positions 0,1,2 are X; 3,4 are O
        r = self.client.get('/api/move?player=x&board=xxxoobbbb&x_player=human&o_player=human')
        self.assertEqual('X Wins', r.get_json()['game']['result'])

    def test_winning_move_returns_o_wins_result(self):
        # O wins right column: positions 2,5,8 are O; 0,3,6 are X
        r = self.client.get('/api/move?player=o&board=xboxbooxo&x_player=human&o_player=human')
        self.assertEqual('O Wins', r.get_json()['game']['result'])

    def test_winning_move_includes_win_line(self):
        r = self.client.get('/api/move?player=x&board=xxxoobbbb&x_player=human&o_player=human')
        self.assertEqual([0, 1, 2], r.get_json()['game']['win_line'])

    def test_draw_returns_draw_result(self):
        # xxoooxxxo is a fully filled drawn board (5 X, 4 O)
        r = self.client.get('/api/move?player=x&board=xxoooxxxo&x_player=human&o_player=human')
        self.assertEqual('Draw', r.get_json()['game']['result'])

    def test_draw_has_no_win_line(self):
        r = self.client.get('/api/move?player=x&board=xxoooxxxo&x_player=human&o_player=human')
        self.assertNotIn('win_line', r.get_json()['game'])

    def test_in_progress_move_has_no_result(self):
        r = self.client.get('/api/move?player=x&board=xbbbbbbbb&x_player=human&o_player=human')
        self.assertNotIn('result', r.get_json()['game'])

    def test_ai_o_response_includes_ai_move_link(self):
        r = self.client.get('/api/move?player=x&board=xbbbbbbbb&x_player=human&o_player=minimax')
        self.assertIn('ai_move', r.get_json()['links'])

    def test_human_o_response_has_no_ai_move_link(self):
        r = self.client.get('/api/move?player=x&board=xbbbbbbbb&x_player=human&o_player=human')
        self.assertNotIn('ai_move', r.get_json()['links'])

    def test_ai_x_response_includes_ai_move_link(self):
        r = self.client.get('/api/move?player=o&board=xobbbbbbb&x_player=minimax&o_player=human')
        self.assertIn('ai_move', r.get_json()['links'])

    def test_unknown_algorithm_returns_400(self):
        # After X's move, O is next with an unknown algorithm
        r = self.client.get('/api/move?player=x&board=xbbbbbbbb&x_player=human&o_player=badbot')
        self.assertEqual(400, r.status_code)

    def test_player_config_preserved_in_response(self):
        r = self.client.get('/api/move?player=x&board=xbbbbbbbb&x_player=human&o_player=random')
        data = r.get_json()['game']
        self.assertEqual('human', data['x_player'])
        self.assertEqual('random', data['o_player'])


class TestAPIIndex(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index_returns_200(self):
        r = self.client.get('/')
        self.assertEqual(200, r.status_code)


