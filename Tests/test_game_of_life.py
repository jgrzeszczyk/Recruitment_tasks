import unittest
import numpy as np
from Task3.game_elements import Cell, Board
from Task3.game_of_life import GameEngine


class TestCell(unittest.TestCase):
    def test_count_neighbors(self):
        board = [[1, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0],
                 [0, 0, 1, 0, 0],
                 [0, 1, 1, 0, 0],
                 [1, 0, 0, 0, 1]]
        tested_cells = [Cell(row=0, col=0, state=1), Cell(row=2, col=2, state=1), Cell(row=4, col=0, state=1)]
        neighbours = [2, 3, 3]
        for tested_cell, neighbours_count in zip(tested_cells, neighbours):
            self.assertEqual(tested_cell.count_neighbours(Board(np.array(board)).board), neighbours_count)


class TestGameEngine(unittest.TestCase):
    def test_compute_iter(self):
        board = [[0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0],
                 [0, 0, 1, 0, 0],
                 [0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0]]
        next_iter_board = [[0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 1, 1, 1, 0],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]]
        correct_next_board = Board(np.array(next_iter_board))

        engine = GameEngine('../Task3/config.json')
        engine.cells_board = Board(np.array(board))
        engine.temp_board = Board(np.array(board))

        engine.compute_iter()
        self.assertEqual(repr(engine.temp_board).split('\n'), repr(correct_next_board).split('\n'))


if __name__ == '__main__':
    unittest.main()
