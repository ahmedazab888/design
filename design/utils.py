import numpy as np


def _unroll(design_matrix):
    """ Unrolls a square

    Args:
        design_matrix: the numpy array to unroll

    Returns:
        unrolled_matrix: a numpy array whose columns are the row, column and
            value of the unrolled square.
    """
    row = []
    col = []
    trt = []
    for r in range(design_matrix.shape[0]):
        for c in range(design_matrix.shape[1]):
            row.append(r + 1)
            col.append(c + 1)
            trt.append(design_matrix[r, c])
    unrolled_matrix = np.array([row, col, trt])
    return unrolled_matrix
