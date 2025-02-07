from utils import *
from tictactoe_algorithm import TicTacToeAlgorithm
import random

class TicTacToeMiniMax(TicTacToeAlgorithm):

    def get_move(self, board, player):

        if score(board) is not None:
            return None

        moves = available_moves(board)

        move_scores = {}
        for move in moves:
            board_after_move = make_move(board, move, player)
            score_after_move = self.minimax(board_after_move, other_player(player))
            move_scores[move] = score_after_move

        # The Key of the highest scoring move, is the move itself.
        if player == X:
            max_value = max(move_scores.values())
            filtered_scores = {k: v for k, v in move_scores.items() if v == max_value}
            return random.choice(list(filtered_scores.keys()))
        else:
            min_value = min(move_scores.values())
            filtered_scores = {k: v for k, v in move_scores.items() if v == min_value}
            return random.choice(list(filtered_scores.keys()))


    def minimax(self, board, player):
        moves = available_moves(board)

        if moves == []:
            return score(board)

        move_scores = {}
        for move in moves:
            board_after_move = make_move(board, move, player)

            this_move_score = score(board_after_move)

            if this_move_score is not None:
                move_scores[move] = this_move_score
                continue

            # Not a definitive result, keep searching
            score_after_move = self.minimax(board_after_move, other_player(player))
            move_scores[move] = score_after_move

        if player == X:
            return max(move_scores.values())
        else:
            return min(move_scores.values())
