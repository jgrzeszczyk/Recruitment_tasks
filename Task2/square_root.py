from typing import Union
import numpy as np
from datetime import datetime
from prettytable import PrettyTable


def calculate_square_root(params: dict,
                          method: str = 'newton') -> tuple:
    """Calcutes squre root of n using selected method
    Currently supports bisection and Newton-Raphson methods
    with termination condition: error <= eps or steps > max_iter
    within selected range [a, b]
    starting from x1"""

    n = params['n']
    eps = params['epsilon']
    max_iters = params['max iterations']
    search_range = params['search range']
    x1 = params['starting point']

    run_info = PrettyTable()
    run_info.title = f'Calculating square root of n={n} using {method} method'
    run_info.field_names = ['Epsilon', 'Max iters', 'Starting Point', 'Search range']
    run_info.add_row([eps, max_iters, x1, search_range])
    print(run_info)

    validate_search_range(n, search_range)
    error = np.abs(square_root(n) - x1 ** 2)  # initial error
    iter = 0
    prev_x = x1
    init_time = datetime.now()

    while eps <= error or iter > max_iters:
        if method == 'newton':
            next_x = newton_method(n, prev_x)
        else:
            next_x = bisection_method(search_range)
            search_range = [next_x, search_range[1]] if (next_x ** 2 - n) < 0 else [search_range[0], next_x]

        error = np.abs(square_root(n) - next_x)
        prev_x = next_x
        print(f'Iter: {iter}, X: {next_x}, error: {error}')
        iter += 1

    elapsed_time = (datetime.now() - init_time).microseconds

    if error <= eps:
        print(f'Algorithm converged within {iter} iterations. Final error: {error}. \n')
    else:
        print('Algorithm failed to converge: amount of steps exceeded max iter. \n')
    return error, elapsed_time, iter


def validate_search_range(n: Union[int, float], search_range: list):
    """Validates if square root of n is in the search space
    and if metod's conditon about sign is met"""

    n_in_range = search_range[0] <= square_root(n) <= search_range[1]
    if (search_range[0]**2 - n) * (search_range[1]**2 - n) >= 0 or not n_in_range:
        raise Exception(f'Root in selected range {search_range} does not exist!')
    return True


def newton_method(n: Union[float, int], x: Union[float, int]) -> float:
    """Returns x calculated using newton method"""
    return 0.5 * (x + n / x)


def square_root(x: Union[int, float]) -> Union[float, int]:
    """Returns square root of x"""
    return np.sqrt(x)


def bisection_method(search_range: list) -> Union[float, int]:
    """Returns x calculated using bisection method"""
    return np.sum(search_range) / 2


def collect_user_input() -> dict:
    """Collects input entered by user"""
    n = float(input('Enter number for square root calculation: \n'))

    eps = float(input('Expected maximum error: \n'))
    max_iter = float(input('Maximum number of iteratrions: \n'))

    a, b = tuple(map(float, input('Enter search range separated by ",": \n').split(',')))
    x1 = float(input('Enter starting point: \n'))
    return {
        'n': n,
        'epsilon': eps,
        'max iterations': max_iter,
        'search range': [a, b],
        'starting point': x1
    }


def validate_user_input(data: dict):
    # TODO: implemend validation for user input data
    raise NotImplementedError


def main():
    parameters = collect_user_input()

    summary = PrettyTable()
    summary.title = 'Summary'
    summary.field_names = ['Numerical method', 'Convergence time [\u03BCs]', 'Total iters', 'Error']

    for method in ['newton', 'bisection']:
        error, elapsed_time, iters = calculate_square_root(params=parameters,
                                                           method=method)
        summary.add_row([method, elapsed_time, iters, error])

    print(summary)


if __name__ == "__main__":
    main()
