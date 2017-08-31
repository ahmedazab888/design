""" Generate Graeco-Latin Squares """
from design.latin_square import latin_square
from design import _unroll
import numpy as np


_MAX_ITERATIONS = 10000


def greaco_latin_square(k, factor_1_labels=None, factor_2_labels=None, seed=None, unroll=None):
    """ Creates a k by k Greaco-Latin Square Design

    A greaco-latin square is a design comprised of two orthogonal latin
    squares.  Note, there are no designs for k = 6.

    Arguments:
        k: the number of treatments.
        factor_1_names: (optional) A list with k elements containing the
            labels applied to the levels of the first factor.  The default are
            the first k uppercase Latin letters.
        seed: (optional) The seed for the random number generation.

    Raises:
        ValueError: if k is not an integer greater than 2 or if one of the
            names arguments does not have the correct number of names.

    Returns:
        ndarray: the Greaco-Latin Square design

    Note:
        This is not compatible with Python 2 due to the use of ord('α').
    """
    if k < 2 or k == 6:
        raise ValueError('No Greaco-Latin Squares exist for k={}'.format(k))

    if factor_1_labels is None:
        factor_1_labels = [chr(ord('A') + i) for i in range(k)]
    elif not isinstance(factor_1_labels, list) or len(factor_1_labels) != k:
        raise ValueError('factor_1_labels must be a list of length {}}').format(k)

    if factor_2_labels is None:
        factor_2_labels = [chr(ord('α') + i) for i in range(k)]
    elif not isinstance(factor_2_labels, list) or len(factor_2_labels) != k:
        raise ValueError('factor_2_labels must be a list of length {}}').format(k)

    if seed is None or seed == 0:
        seed = 7172

    n_iter = 0
    while True:
        n_iter += 1
        latin_square_1 = latin_square(k,
                                      treatment_names=factor_1_labels,
                                      randomize=True,
                                      seed=seed * n_iter)

        latin_square_2 = latin_square(k,
                                      treatment_names=factor_2_labels,
                                      randomize=True,
                                      seed=35 * seed * n_iter)
        if _is_orthoganal(k, latin_square_1, latin_square_2):
            break
        if n_iter > _MAX_ITERATIONS:
            raise Exception('Maximum number of iterations reached')
    greaco_latin_square = []
    for i in range(k):
        row = []
        for j in range(k):
            row.append((str(latin_square_1[i][j]) +
                        str(latin_square_2[i][j])))
        greaco_latin_square.append(row)

    greaco_latin_square = np.array(greaco_latin_square)
    if unroll:
        greaco_latin_square = _unroll(greaco_latin_square)

    return greaco_latin_square


def _is_orthoganal(k, latin_square_1, latin_square_2):
    symbols = []
    for i in range(k):
        for j in range(k):
            symbol = str(latin_square_1[i][j]) + str(latin_square_2[i][j])
            if symbol in symbols:
                return False
            symbols.append(symbol)
    return True
