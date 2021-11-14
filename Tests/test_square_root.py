import unittest
from Task2 import square_root


class TestSquareRoot(unittest.TestCase):
    def test_calculate_square_root(self):
        data = {'n': '2', 'epsilon': '0.001', 'max iterations': '100', 'start point': '2', 'search range': '0,3'}
        methods = ['newton', 'bisection']
        self.assertTrue(square_root.validate_user_input(data))

        # checks if error < epsilon and elapsed iterations < max iterations
        for method in methods:
            error, _, iter_idx = square_root.calculate_square_root(data, method)
            self.assertLessEqual(error, data['epsilon'])
            self.assertLessEqual(iter_idx, data['max iterations'])

    def test_validate_search_range(self):
        self.assertTrue(square_root.validate_search_range(2, [0, 4]))
        self.assertTrue(square_root.validate_search_range(8, [0, 4]))

        with self.assertRaises(Exception):
            square_root.validate_search_range(2, [2, 4])

        with self.assertRaises(Exception):
            square_root.validate_search_range(3, [2, 4])

    def test_validate_user_input(self):

        # checks method for correct input data
        parameters = {'n': '2', 'epsilon': '0.001', 'max iterations': '100', 'start point': '2', 'search range': '0,3'}
        self.assertTrue(square_root.validate_user_input(parameters.copy()))

        # checks for Exception if char is entered instead of float or int
        for key in parameters.keys():
            data = parameters.copy()
            data[key] = 'c'
            with self.assertRaises(Exception):
                square_root.validate_user_input(data)

        # checks for value <= 0 for selected parameters except for n
        for key in ['n', 'max iterations', 'epsilon']:
            data = parameters.copy()
            for test_value in ['-2', '0']:
                if key == 'n' and test_value == '0':
                    break
                data[key] = test_value
                with self.assertRaises(AssertionError):
                    square_root.validate_user_input(data)

        # checks for square root of 0
        data = parameters.copy()
        data['n'] = '0'
        self.assertTrue(square_root.validate_user_input(data))


if __name__ == '__main__':
    unittest.main()
