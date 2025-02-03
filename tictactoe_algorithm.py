from abc import ABC, abstractmethod

class TicTacToeAlgorithm(ABC):
    @abstractmethod
    def get_move(self, board, player):
        pass    # This is an abstract method, no implementation here.




