import numpy as np
from datetime import datetime
import json
from copy import deepcopy
import time

from Task1.traffic_lights import Worker

from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QApplication, QDialog, QGroupBox, QGridLayout, QButtonGroup, \
    QTextEdit
from PyQt5.QtCore import Qt, QSize, QThread


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
        self.running = False

    def compute_iter(self) -> None:
        """Computes game iteration"""
        for row in range(self.cells_board.shape[0]):
            for col in range(self.cells_board.shape[1]):
                current_cell = self.cells_board[row, col]
                neighbours_count = current_cell.count_neighbours(self.cells_board)

                self.apply_game_rules(neighbours_count, current_cell)

    def run(self, kwargs) -> None:
        """Runs the whole game"""
        self.print_iter()
        while self.running:
            start_time = datetime.now()
            self.compute_iter()
            self.update_board()
            elapsed_time = self.measure_iter_time(start_time)
            self.print_iter()
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

    def print_iter(self) -> None:
        """Prints current iteration array"""
        board_repr = [[self.cells_board[row, col].state for col in range(self.cells_board.shape[1])]
                      for row in range(self.cells_board.shape[0])]
        print('\n'.join([str(x) for x in board_repr]))


class GUI(QDialog):
    def __init__(self):
        super().__init__()
        self.title = 'Game of Life'
        self.left = 200
        self.top = 200
        self.width = 200
        self.engine = GameEngine('./config.json')
        self.height = 150
        self.initUI()
        self.worker = Worker(self.engine.run, update_gui_func=self.update_grid_colors)

    def initUI(self):
        self.buttons = []
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.vLayout = QVBoxLayout()
        self.create_grid_layout()
        window_layout = QVBoxLayout()
        window_layout.addWidget(self.horizontal_group_box)

        self.control_box = QGroupBox('Control Panel')
        control_box_layout = QGridLayout()

        self.start_button = QPushButton('Start')
        self.btn_group = QButtonGroup()
        self.btn_group.setExclusive(True)
        self.btn_group.addButton(self.start_button)
        control_box_layout.addWidget(self.start_button, 0, 0)

        self.btn_group.buttonClicked.connect(self.on_click)

        self.info_area = QTextEdit()
        self.info_area.setObjectName('Console logs')
        self.info_area.setReadOnly(True)

        control_box_layout.addWidget(self.info_area, 1, 0)

        self.control_box.setLayout(control_box_layout)
        window_layout.addWidget(self.control_box, alignment=Qt.AlignBottom)
        self.setLayout(window_layout)
        self.show()

    def on_click(self, btn):
        if btn.text() == 'Start':
            self.start_button.setEnabled(False)
            self.engine.running = True
            self.compute_iteration()

    def update_grid_colors(self, iter_time):
        for row in range(self.buttons.shape[0]):
            for col in range(self.buttons.shape[1]):
                color = 'black' if self.engine.cells_board[row, col].state == 1 else 'white'
                self.buttons[row, col].setStyleSheet(f'background-color : {color}')
        self.info_area.append(f'Iter time: {iter_time} [\u03BCs]')
        self.info_area.ensureCursorVisible()

    def create_grid_layout(self):
        self.horizontal_group_box = QGroupBox('Current generation')
        layout = QGridLayout()
        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)

        temp_buttons = []
        for row in range(self.engine.cells_board.shape[0]):
            for col in range(self.engine.cells_board.shape[1]):
                cell = self.engine.cells_board[row, col]

                btn = QPushButton()
                btn.setFixedSize(QSize(20, 20))
                btn_color = 'black' if cell.state == 1 else 'white'
                btn.setStyleSheet(f'background-color : {btn_color}')
                btn.setEnabled(False)
                layout.addWidget(btn, cell.row, cell.col)
                temp_buttons.append(btn)

        self.buttons = np.array(temp_buttons).reshape(self.engine.cells_board.shape[0],
                                                      self.engine.cells_board.shape[1])
        self.horizontal_group_box.setLayout(layout)

    def compute_iteration(self) -> None:
        """Threading to avoid GUI freezing"""

        # Create a QThread object
        self.thread = QThread()
        #  Create a worker object
        self.worker = self.worker
        # Move worker to the thread
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Start the thread
        self.thread.start()


def main():
    app = QApplication([])
    window = GUI()
    app.exec()

    # game.run()


if __name__ == "__main__":
    main()
