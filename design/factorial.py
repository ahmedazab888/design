import numpy as np
import math


def factorial_2(k, p=None, contrasts=None):
    """ Generate :math:`2^{k}` and :math:`2^{k-p}` factorial designs



    For the 2^{8 - 3}, we set k=8 and p=3.

    There are three contrasts that we need to define (p).  Each contrast is a
    list

    Args:
        k: The number of factors in the design
        p: The number of contrasts to be observed
        contrast: A list of lists indicating the interactions of interest.
            Suppose we are interested in the following interactions:
                x_3 + x_4 + x_5,
                x_1 + x_2 + x_4 + x_5,
                x_1 + x_2 + x_3 + x_5,
            We would define contrast as:
            [[3, 4, 5], [1, 2, 4, 5], [1, 2, 3, 5]]

    Raises:
        ValueError: If `k` is not an integer or if `p` is not None and it is
            not an integer in [0, 7] whose length length is equal to the length
            of contrasts.

    Returns:
        ndarray: The design matrix whose columns are the variables/interactions
            in the design
        int: The resolution of the design.
    """
    if not isinstance(k, int):
        raise ValueError('`k` ({}) must be an interger.'.format(k))
    if p is not None:
        if p < 0 or p > 7:
            raise ValueError('`p` ({}) must be in [0, 7]'.format(p))
        if not isinstance(p, int):
            raise ValueError('`p` ({}) must be an integer in [0, 7]'.format(p))

        if p != len(contrasts):
            raise ValueError('`p` ({}) must be equal to the length of `contrasts` ({})'.format(p, len(contrasts)))

    # Generate for k - p
    design = []

    # resolution = min(length of word)
    word_lengths = [len(contrast) for contrast in contrasts]
    resolution = min(word_lengths)

    # Create the contrast columns
    contrast_columns = []
    for contrast in contrasts:
        contrast_column = design[contrast[0]]
        for col in contrast.pop(0):
            contrast_column = [math.copysign(1, col) * x * y for
                               x, y in zip(contrast_column, design[abs(col)])]
        contrast_columns.append(contrast_column)

    design_matrix = np.transpose(np.array([design, contrast_columns]))
    return design_matrix, resolution
