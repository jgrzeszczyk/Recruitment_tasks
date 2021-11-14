import numpy as np
from typing import Union, Any
from datetime import datetime
from prettytable import PrettyTable


def print_run_info(data: dict, method: str) -> None:
    run_info = PrettyTable()
    run_info.title = f'Calculating square root of n={data["n"]} using {method} method'
    run_info.field_names = ['Epsilon', 'Max iters', 'Start Point', 'Search range']
    run_info.add_row([data["epsilon"], data["max iterations"], data["start point"], data["search range"]])
    print(run_info)


def calculate_square_root(params: dict,
                          method: str = 'newton') -> tuple:
    """Calculates square root of n using selected method
    with termination condition: error <= eps or steps > max_iter
    within selected range [a, b]
    starting from x1"""

    n = params['n']
    eps = params['epsilon']
    max_iters = params['max iterations']
    search_range = params['search range']
    x1 = params['start point']

    print_run_info(params, method=method)
    assert validate_search_range(n, search_range)

    error = np.abs(square_root(n) - x1 ** 2)  # initial error
    iter_idx = 0
    prev_x = x1
    init_time = datetime.now()

    while error >= eps and iter_idx <= max_iters:
        if method == 'newton':
            next_x = newton_method(n, prev_x)
        else:
            next_x = bisection_method(search_range)
            search_range = [next_x, search_range[1]] if (next_x ** 2 - n) < 0 else [search_range[0], next_x]

        error = np.abs(square_root(n) - next_x)
        prev_x = next_x
        print(f'Iter: {iter_idx}, X: {next_x}, error: {error}')
        iter_idx += 1

    elapsed_time = (datetime.now() - init_time).microseconds

    if error <= eps:
        print(f'Algorithm converged within {iter_idx} iterations. Final error: {error}. \n')
    else:
        print('Algorithm failed to converge: amount of steps exceeded max iterations. \n')
    return error, elapsed_time, iter_idx


def validate_search_range(n: Union[int, float], search_range: list) -> bool:
    """Validates if square root of n is in the search space
    and if method's condition about sign is met"""

    n_in_range = search_range[0] <= square_root(n) <= search_range[1]
    if (search_range[0] ** 2 - n) * (search_range[1] ** 2 - n) >= 0 or not n_in_range:
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
    n = input('Enter number for square root calculation: \n')
    eps = input('Expected maximum error: \n')
    max_iter = input('Maximum number of iterations: \n')
    search_range = input('Enter search range separated by ",": \n')
    x1 = input('Enter start point: \n')

    data = {'n': n,
            'epsilon': eps,
            'max iterations': max_iter,
            'start point': x1,
            'search range': search_range}
    validate_user_input(data)
    return data


def validate_int_or_float(x: Any, var_name: str) -> float:
    """Validates if passed x is of type int or float"""
    try:
        x = float(x)
    except TypeError:
        raise Exception(f'{var_name} should be of type int or float, '
                        f'but found {type(x)}')
    return x


def validate_user_input(data: dict) -> bool:
    parameters_names = ['Number for square root calculation', 'Maximum error', 'Number of max iterations',
                        'Start point for the algorithm']
    for param, param_name in zip(data.keys(), parameters_names):
        data[param] = validate_int_or_float(data[param], param_name)
        if param in ['max iterations', 'epsilon']:
            assert data[param] > 0, f'{param.capitalize()} should be greater than 0!'
        elif param == 'n':
            assert data[param] >= 0, f'Cannot calculate square root of {data["n"]}!'
    try:
        a, b = list(map(float, data['search range'].split(',')))
    except ValueError:
        raise Exception('Please enter two values of type int or float separated by "," for search range parameter')
    data['search range'] = [a, b]

    return True


def main():
    parameters = collect_user_input()

    summary = PrettyTable()
    summary.title = 'Summary'
    summary.field_names = ['Numerical method', 'Convergence time [\u03BCs]', 'Total iters', 'Error']

    for method in ['newton', 'bisection']:
        error, elapsed_time, iterations = calculate_square_root(params=parameters,
                                                                method=method)
        summary.add_row([method, elapsed_time, iterations, error])

    print(summary)


if __name__ == "__main__":
    main()
