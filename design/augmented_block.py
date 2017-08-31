""" Generate an Augmented Block Design """
import numpy as np


def augmented_block(treatments_1, treatments_2, reps,
                    randomize=None, seed=None):
    """ Generate an Augmented Block Design

    An augmented block design is a block design for `treatment_1` augmented by
    single runs from `treatment_2`.

    Args:
        treatment_1: A list of treatments to be blocked
        treatment_2: A list of treatments to be run in single runs
        reps: The number of reps each treatment from treatment_1 is run
        randomize: A boolean indicating if the order of treatments should be
            randomized.  If this is for an actual trial, this should be True
        seed: The seed for used by numpy.random.seed()

    Returns:
        ndarray: The design matrix whose columns are the block number and the
            treatment.
    """
    if seed is not None:
        np.random.seed(seed)

    n_trt_1 = len(treatments_1)
    n_trt_2 = len(treatments_2)

    treatment = []
    block = []
    for r in range(reps):
        if randomize:
            np.random.shuffle(treatments_1)
        treatment.extend(treatments_1)
        block.extend([r + 1] * n_trt_1)

    if randomize:
        np.random.shuffle(treatments_2)

    treatment.extend(treatments_2)

    for idx in range(n_trt_2):
        block.append((idx % reps) + 1)

    design_matrix = np.transpose(np.array([block, treatment]))

    # Sort by block
    design_matrix = design_matrix[design_matrix[:, 0].argsort()]
    return design_matrix
