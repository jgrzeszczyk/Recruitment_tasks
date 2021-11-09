import numpy as np
from datetime import datetime
import json
from copy import deepcopy
import time


class Cell:
    def __init__(self, row: int, col: int, state: int):
        self.row = row
        self.col = col
        self.state = state

    def count_neighbours(self, board: np.array) -> int:
        """Counts neighbours surrounding the specific cell"""

        # TODO: Try to merge below conditions
        if self.row == 0:
            count_rows = [board.shape[0] - 1, self.row, self.row + 1]
        elif self.row == board.shape[0] - 1:
            count_rows = [self.row - 1, self.row, 0]
        else:
            count_rows = [self.row - 1, self.row, self.row + 1]

        if self.col == 0:
            count_cols = [board.shape[1] - 1, self.col, self.col + 1]
        elif self.col == board.shape[1] - 1:
            count_cols = [self.col - 1, self.col, 0]
        else:
            count_cols = [self.col - 1, self.col, self.col + 1]

        self.neighbours = np.array([[board[row, col].state for col in count_cols] for row in count_rows])

        return np.sum(self.neighbours) if self.state == 0 else (np.sum(self.neighbours) - 1)


class GameEngine:
    def __init__(self, config_path: str):
        with open(config_path) as f:
            config = json.load(f)

        self.init_array = np.array(config['initial_pose'])
        self.cells_board = np.array([[Cell(row, col, state=self.init_array[row, col])
                                      for col in range(self.init_array.shape[1])]
                                     for row in range(self.init_array.shape[0])], dtype='object')
        self.temp_board = deepcopy(self.cells_board)
        self.refresh_rate = config['refresh_rate']

    def compute_iter(self) -> None:
        """Computes game iteration"""
        for row in range(self.cells_board.shape[0]):
            for col in range(self.cells_board.shape[1]):
                current_cell = self.cells_board[row, col]
                neighbours_count = current_cell.count_neighbours(self.cells_board)

                self.apply_game_rules(neighbours_count, current_cell)

    def run(self) -> None:
        """Runs the whole game"""
        self.print_iter()
        while True:
            start_time = datetime.now()
            self.compute_iter()
            self.update_board()
            elapsed_time = self.measure_iter_time(start_time)
            self.print_iter()
            print('Iter time: ', elapsed_time, ' [\u03BCs]')
            time.sleep(self.refresh_rate)

    def update_board(self) -> None:
        """Updates board by coping temp board"""
        self.cells_board = deepcopy(self.temp_board)

    def apply_game_rules(self, neighbours_count: int, cell: Cell) -> None:
        """Apply Game Of Life main rules to current cells generation"""
        if neighbours_count in [2, 3] and cell.state == 1:
            self.temp_board[cell.row, cell.col].state = 1
        elif cell.state == 0 and neighbours_count == 3:
            self.temp_board[cell.row, cell.col].state = 1
        else:
            self.temp_board[cell.row, cell.col].state = 0

    @staticmethod
    def measure_iter_time(start_time: datetime.time) -> int:
        """Measures elapsed time since start_time"""
        return (datetime.now() - start_time).microseconds

    def print_iter(self) -> None:
        """Prints current iteration array"""
        board_repr = [[self.cells_board[row, col].state for col in range(self.cells_board.shape[1])]
                      for row in range(self.cells_board.shape[0])]
        print('\n'.join([str(x) for x in board_repr]))


def main():
    config_path = './config.json'
    game = GameEngine(config_path)
    game.run()


if __name__ == "__main__":
    main()
