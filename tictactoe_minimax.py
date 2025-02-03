from utils import *
from tictactoe_algorithm import TicTacToeAlgorithm

class TicTacToeMiniMax(TicTacToeAlgorithm):

    def get_move(self, board, player):
        moves = available_moves(board)

        move_scores = {}
        for move in moves:
            board_after_move = make_move(board, move, player)
            score_after_move = self.__minimax(board_after_move, other_player(player))
            move_scores[move] = score_after_move * player

        # The Key of the highest scoring move, is the move itself.
        return max(move_scores, key=move_scores.get)


    def __minimax(self, board, player):
        moves = available_moves(board)

        if moves == []:
            return score(board)

        move_scores = {}
        for move in moves:
            board_after_move = make_move(board, move, player)
            score_after_move = minimax(board_after_move, other_player(player))
            move_scores[move] = score_after_move * player

        this_score = max(move_scores.values())
        return this_score * player
