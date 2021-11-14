from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QDialog, QGroupBox, QGridLayout, QButtonGroup, QTextEdit
from PyQt5.QtCore import Qt, QSize
import numpy as np

from Utils.utils import Worker, CustomThread
from game_of_life import GameEngine


class GUI(QDialog):
    def __init__(self, console_logs):
        super().__init__()
        self.title = 'Game of Life'
        self.left = 200
        self.top = 200
        self.width = 200
        self.height = 150
        self.engine = GameEngine('./config.json', console_logs=console_logs)
        self.worker = Worker(self.engine.run, update_gui_func=self.update_grid_colors)
        self.threading = CustomThread(worker=self.worker)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_grid_layout()
        window_layout = QVBoxLayout()
        window_layout.addWidget(self.horizontal_group_box)

        self.start_button = QPushButton('Start')
        self.btn_group = QButtonGroup()
        self.btn_group.setExclusive(True)
        self.btn_group.addButton(self.start_button)
        self.btn_group.buttonClicked.connect(self.on_click)

        self.control_box = QGroupBox('Control Panel')
        control_box_layout = QGridLayout()
        control_box_layout.addWidget(self.start_button, 0, 0)

        self.info_area = QTextEdit()
        self.info_area.setObjectName('Console logs')
        self.info_area.setReadOnly(True)

        control_box_layout.addWidget(self.info_area, 1, 0)
        self.control_box.setLayout(control_box_layout)
        window_layout.addWidget(self.control_box, alignment=Qt.AlignBottom)
        self.setLayout(window_layout)
        self.show()

    def on_click(self, btn):
        """Defines what happens when button is clicked"""
        if btn.text() == 'Start':
            self.start_button.setEnabled(False)
            self.engine.running = True
            self.threading.run_task()  # runs iteration computation

    def update_grid_colors(self, iter_time):
        """Updates cells' colors according to the actual state"""
        for row in range(self.buttons.shape[0]):
            for col in range(self.buttons.shape[1]):
                color = 'black' if self.engine.cells_board.board[row, col].state == 1 else 'white'
                self.buttons[row, col].setStyleSheet(f'background-color : {color}')
        self.info_area.append(f'Iter time: {iter_time} [\u03BCs]')
        self.info_area.ensureCursorVisible()

    def create_grid_layout(self):
        """Creates grid layout for cells"""
        # Setting layout
        self.horizontal_group_box = QGroupBox('Current generation')
        layout = QGridLayout()
        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)

        # Adding cells represented as non-clickable buttons to the layout
        temp_buttons = []
        for row in range(self.engine.cells_board.board.shape[0]):
            for col in range(self.engine.cells_board.board.shape[1]):
                cell = self.engine.cells_board.board[row, col]

                btn = QPushButton()
                btn.setFixedSize(QSize(20, 20))
                btn_color = 'black' if cell.state == 1 else 'white'
                btn.setStyleSheet(f'background-color : {btn_color}')
                btn.setEnabled(False)
                layout.addWidget(btn, cell.row, cell.col)
                temp_buttons.append(btn)

        self.buttons = np.array(temp_buttons).reshape(self.engine.cells_board.board.shape[0],
                                                      self.engine.cells_board.board.shape[1])
        self.horizontal_group_box.setLayout(layout)
