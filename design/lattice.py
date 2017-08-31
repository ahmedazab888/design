""" Generates a Lattice Design """
import math
import numpy as np
from design import latin_square


def lattice(treatments, r, randomize=None, seed=None):
    """ Generate a Lattice Design

    Args:
        treatments: The treatments subjects are to be randomized to.
        randomize: A boolean indicating if the order of treatments should be
            randomized.  If this is for an actual trial, this should be True
        seed: The seed for used by numpy.random.seed()

    Returns:
        ndarray: The design matrix whose columns are the block number, the plot
            number, the sub plot number, the plot treatment and the sub plot
            treatment
    """
    n_trt = len(treatments)
    k = math.sqrt(n_trt)
    if r not in [2, 3]:
        raise ValueError('DESCRIPTION')

    if int(k + 0.5) ** 2 != n_trt:
        raise ValueError('SOMETHING ABOUT NEEDING TO HAVE PERFECT SQUARES')

    square_values = list(range(k))
    if randomize:
        np.shuffle(square_values)
    square_1 = [[0] * k] * k
    for r in range(k):
        for c in range(k):
            square_1[r][c] = square_values[k * (r - 1) + c]

    square_1 = np.array(square_1)
    square_2 = np.transpose(square_1)
    latin_square_trt = latin_square(k, seed=seed * 7218, unroll=True)[, 2]
    order = [i[0] for i in sorted(enumerate(latin_square_trt), key=lambda x:x[1])]
    square_3 = np.zeros((k, k))
    for idx, o in enumerate(order):
        r_3 = idx // k
        c_3 = idx % k
        r_1 = o // k
        c_1 = o % k
        square_3[r_3, c_3] = square_1[r_1, c_1]
    square_3 = np.transpose(square_3)

    if randomize:
        np.random.shuffle(square_1)
        np.random.shuffle(square_2)
        np.random.shuffle(square_3)

    rep = [i // n_trt + 1 for i in range(3 * n_trt)]
    block = [i // k + 1 for i in range(3 * n_trt)]

    trt = []
    for square in [square_1, square_2, square_3]:
        for col in range(k):
            trt.extend(square[:, col])
    design_matrix = np.array([block, rep, trt])
    return design_matrix
