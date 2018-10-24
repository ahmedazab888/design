""" Generate a Strip Design """
import numpy as np


def strip(treatments_r, treatments_c, reps, randomize=None, seed=None):
    """ Generate a Strip Plot Design

    Args:
        treatments_r: The treatments to be applied to the rows
        treatments_c: The treatments to be applied to the columns
        reps: The number of times each treatment is replicated
        randomize: A boolean indicating if the order of treatments should be
            randomized.  If this is for an actual trial, this should be True
        seed: The seed for used by numpy.random.seed()

    Returns:
        ndarray: The design matrix whose columns are the block number,  the
            treatment in each row, and the treatment in each column.
    """
    if seed is not None:
        np.random.seed(seed)
    n_1 = len(treatments_r)
    n_2 = len(treatments_c)
    row_treatment = []
    column_treatment = []
    block = []
    row = [list(range(1, n_1 + 1))] * n_2 * reps
    col = []
    for r in range(reps):
        if randomize:
            np.random.shuffle(treatments_r)
            np.random.shuffle(treatments_c)
        for i in range(n_2):
            row_treatment.extend(treatments_r)
            column_treatment.extend(treatments_c[i] * n_1)
            col.append([i + 1] * n_1)
        block.extend([r + 1] * n_1 * n_2)
    col = [val for sublist in col for val in sublist]
    row = [val for sublist in row for val in sublist]
    design_matrix = np.transpose(np.array([block, row, col, row_treatment, column_treatment]))
    return design_matrix
