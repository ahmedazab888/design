""" Generate a Youden Square """
import numpy as np
from .utils import _unroll


def youden(treatments, reps=None, randomize=None, seed=None, unroll=None):
    """ Generates a Youden Square

    A Youden square is a Latin Square in which the number of columns does not
    equal the number of rows.

    Args:
        treatments: a list of the treatments to be used in the design
        reps: The number of replications of the design.  If this value is None,
            the design is not replicated.
        randomize: A boolean indicating if the order of treatments should be
            randomized.  If this is for an actual trial, this should be True
        seed: The seed for used by numpy.random.seed()
        unroll: If the design matrix should be a rectangle, or unrolled to have
            each subject on its own row

    Returns:
        design_matrix: A numpy array representing the design.  If `unroll` is
        True, the arrays columns are the row and column of the Youden square
        and the treatment.  Otherwise, it is the Youden square itself.
    """
    if seed is not None:
        np.random.seed(seed)

    if reps is None:
        reps = 1

    n_treatments = len(treatments)
    design_matrix = []

    for j in range(reps):
        row = list(range(j, n_treatments))
        if j > 0:
            tmp = list(range(0, j))
            row.extend(tmp)
        row = [treatments[idx] for idx in row]
        design_matrix.append(row)
    design_matrix = np.transpose(np.array(design_matrix))

    if randomize:
        design_matrix = design_matrix[np.random.permutation(design_matrix.shape[0]), :]
        design_matrix = design_matrix[:, np.random.permutation(design_matrix.shape[1])]

    if unroll:
        design_matrix = _unroll(design_matrix)
    return design_matrix
