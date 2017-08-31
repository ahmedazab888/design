""" Generate Latin Squares """
import numpy as np
from math import floor
from design import _unroll

_MAX_ITERATIONS = 10000


def latin_square(k, factor_labels=None, seed=None, unroll=None):
    """ Creates a k by k Latin Square Design

    A Latin Square design is a block design with 2 blocking factors.  Each
    blocking factor has the same number of levels as there are treatments, k.

    This function returns a randomly generated latin square.

    The design is represented as a list of lists.  Each treatment occurs
    once per row and once per column.

    Arguments:
        k: the number of treatments.
        factor_labels: (optional) A list with k elements representing the
            labels applied to the levels of the blocking factor.  The default
            are the first k uppercase Latin letters.
        seed: (optional) The seed for the random number generation.

    Raises:
        ValueError: if k is not an integer greater than 2 or if one of the
            names arguments does not have the correct number of names.

    Returns:
        ndarray: the Latin Square design
    """
    if seed is not None:
        np.random.seed(seed)

    if not isinstance(k, int) or k < 2:
        raise ValueError('k must be an integer greater than 2.')

    if factor_labels is None:
        factor_labels = [chr(ord('A') + i) for i in range(k)]
    elif not isinstance(factor_labels, list) or len(factor_labels) != k:
        raise ValueError('factor_labels must be a list '
                         'of length {}'.format(k))

    latin_square = _create_latin_square(k)
    for row in range(k):
        for col in range(k):
            latin_square[row][col] = factor_labels[latin_square[row][col]]

    latin_square = np.array(latin_square)
    if unroll:
        latin_square = _unroll(latin_square)

    return latin_square


def _cube_to_square(cube, k):
    square = []
    for i in range(k):
        row = []
        for j in range(k):
            row.append(0)
        square.append(row)
    for x in range(k):
        for y in range(k):
            for s in range(k):
                if cube[x][y][s] == 1:
                    square[x][y] = s
                    break
    return square


def _square_to_cube(square, k):
    cube = []
    for i in range(k):
        outer_row = []
        for j in range(k):
            inner_row = []
            for m in range(k):
                inner_row.append(0)
            outer_row.append(inner_row)
        cube.append(outer_row)
    for x in range(k):
        for y in range(k):
            cube[x][y][square[x][y]] = 1
    return cube


def _default_square(k):
    lookup = [0] * (2 * k)
    square = []
    for i in range(k):
        row = []
        for j in range(k):
            row.append(0)
        square.append(row)
    for a in range(2):
        for i in range(k):
            lookup[a * k + i] = i
    for y in range(k):
        for x in range(k):
            square[y][x] = lookup[x + y]
    return square


def _shuffle_cube(cube, k):
    min_iterations = k * k * k
    iterations = 0
    proper = True
    improper_cell = None
    while iterations < min_iterations or not proper:
        iterations += 1
        if iterations > _MAX_ITERATIONS:
            raise Exception()
        if proper:
            t = {
                'x': floor(np.random.random() * k),
                'y': floor(np.random.random() * k),
                'z': floor(np.random.random() * k),
            }
            counter = 0
            while cube[t['x']][t['y']][t['z']] != 0:
                counter += 1
                if counter > 100:
                    raise Exception()
                t['x'] = floor(np.random.random() * k)
                t['y'] = floor(np.random.random() * k)
                t['z'] = floor(np.random.random() * k)
            i = 0
            while cube[i][t['y']][t['z']] == 0:
                i += 1
            x_1 = i

            i = 0
            while cube[t['x']][i][t['z']] == 0:
                i += 1
            y_1 = i

            i = 0
            while cube[t['x']][t['y']][i] == 0:
                i += 1
            z_1 = i
        else:
            t = improper_cell

            skip_next = np.random.random() < 0.5
            for i in range(k):
                if cube[i][t['y']][t['z']] == 1:
                    x_1 = i
                    if not skip_next:
                        break

            skip_next = np.random.random() < 0.5
            for i in range(k):
                if cube[t['x']][i][t['z']] == 1:
                    y_1 = i
                    if not skip_next:
                        break

            skip_next = np.random.random() < 0.5
            for i in range(k):
                if cube[t['x']][t['y']][i] == 1:
                    z_1 = i
                    if not skip_next:
                        break

        cube[t['x']][t['y']][t['z']] += 1
        cube[t['x']][y_1][z_1] += 1
        cube[x_1][y_1][t['z']] += 1
        cube[x_1][t['y']][z_1] += 1

        cube[t['x']][t['y']][z_1] -= 1
        cube[t['x']][y_1][t['z']] -= 1
        cube[x_1][t['y']][t['z']] -= 1
        cube[x_1][y_1][z_1] -= 1

        proper = cube[x_1][y_1][z_1] != -1
        if not proper:
            improper_cell = {
                'x': x_1,
                'y': y_1,
                'z': z_1,
            }
    return cube


def _create_latin_square(k):
    square = _default_square(k)
    cube = _square_to_cube(square, k)
    cube = _shuffle_cube(cube, k)
    square = _cube_to_square(cube, k)
    return square
