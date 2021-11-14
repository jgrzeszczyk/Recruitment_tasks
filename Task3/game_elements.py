import numpy as np
from copy import deepcopy


class Cell:
    def __init__(self, row: int, col: int, state: int):
        self.row = row
        self.col = col
        self.state = state

    def count_neighbours(self, board: np.array) -> int:
        """Counts neighbours surrounding the specific cell"""

        # Periodic boundary conditions
        row1 = board.shape[0] - 1 if self.row == 0 else self.row - 1
        row3 = 0 if self.row == board.shape[0] - 1 else self.row + 1

        col1 = board.shape[1] - 1 if self.col == 0 else self.col - 1
        col3 = 0 if self.col == board.shape[1] - 1 else self.col + 1

        rows = [row1, self.row, row3]
        cols = [col1, self.col, col3]

        self.neighbours = np.array([[board[row, col].state for col in cols] for row in rows])

        return np.sum(self.neighbours) if self.state == 0 else (np.sum(self.neighbours) - 1)


class Board:
    def __init__(self, board: np.array):
        self.board = np.array([[Cell(row, col, state=board[row, col])
                                for col in range(board.shape[1])]
                               for row in range(board.shape[0])], dtype='object')

    def __repr__(self):
        board_repr = [[self.board[row, col].state for col in range(self.board.shape[1])]
                      for row in range(self.board.shape[0])]
        return '\n'.join([str(x) for x in board_repr])

    def update_board(self, new_board) -> bool:
        """Updates board by coping temp board"""
        if isinstance(new_board, Board):
            self.board = deepcopy(new_board.board)
            return True
        return False
