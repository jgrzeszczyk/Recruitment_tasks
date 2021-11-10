import numpy as np
from datetime import datetime
import json
from copy import deepcopy
import time
import sys

from PyQt5.QtWidgets import QApplication


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


class GameEngine:
    def __init__(self, config_path: str, console_logs=False):
        with open(config_path) as f:
            self.config = json.load(f)

        self.validate_config()
        self.init_array = np.array(self.config['initial_pose'])
        self.refresh_rate = self.config['refresh_rate']

        # Create cells board that consists of array of cells of type Cell
        self.cells_board = np.array([[Cell(row, col, state=self.init_array[row, col])
                                      for col in range(self.init_array.shape[1])]
                                     for row in range(self.init_array.shape[0])], dtype='object')
        self.temp_board = deepcopy(self.cells_board)
        self.running = False
        self.console_logs = console_logs

    def validate_config(self) -> None:
        """Validates game config"""
        if 'initial_pose' not in self.config.keys() or 'refresh_rate' not in self.config.keys():
            raise Exception('Config file should contain initial_pose and refresh_rate keys!')
        elif not isinstance(self.config['initial_pose'], list):
            raise Exception(f'Initial pose array should be of type: list, not {type(self.config["initial_pose"])}')
        elif not isinstance(self.config['refresh_rate'], int):
            raise Exception(f'Refresh rate should be of type int, not {self.config["refresh_rate"]}')

    def compute_iter(self) -> None:
        """Computes game iteration"""
        for row in range(self.cells_board.shape[0]):
            for col in range(self.cells_board.shape[1]):
                current_cell = self.cells_board[row, col]
                neighbours_count = current_cell.count_neighbours(self.cells_board)

                self.apply_game_rules(neighbours_count, current_cell)

    def run(self, kwargs) -> None:
        """Runs the whole game"""
        while self.running:
            start_time = datetime.now()
            self.compute_iter()
            self.update_board()
            elapsed_time = self.measure_iter_time(start_time)
            if self.console_logs:
                self.print_iter(elapsed_time)
            time.sleep(self.refresh_rate)
            update_gui_func = kwargs['update_gui_func']
            update_gui_func(elapsed_time)

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

    def print_iter(self, elapsed_time: int) -> None:
        """Prints current iteration array"""
        board_repr = [[self.cells_board[row, col].state for col in range(self.cells_board.shape[1])]
                      for row in range(self.cells_board.shape[0])]
        print('\n'.join([str(x) for x in board_repr]), '\n', f'Iter time: {elapsed_time}')


def run_gui(console_logs):
    from game_gui import GUI
    window = GUI(console_logs=console_logs)


def main():
    # TO PRINT CONSOLE LOGS CHANGE console_logs argument in run_gui method to True
    app = QApplication([])
    run_gui(console_logs=True)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
