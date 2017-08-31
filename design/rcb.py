""" Generate a randomized complete block design """
import numpy as np


def rcb(treatments, reps, seed=None):
    """ Generate a Randomized Complete Block Design

    In a randomized complete block design, subjects are randomized to
    treatments in such a way that each treatment is used once before any
    treatment is used again.

    Args:
        treatments: A list of treatments subjects will be randomized to.
        reps: The number of times each treatment is to be replicated
        seed: The seed for used by numpy.random.seed()

    Returns:
        ndarray: The design matrix whose columns are the block number and the
            treatment.
    """
    if seed is not None:
        np.random.seed(seed)
    n_trt = len(treatments)
    block = []
    treatment = []
    for r in range(reps):
        np.random.shuffle(treatments)
        treatment.extend(treatments)
        block.extend([r + 1] * n_trt)
    design_matrix = np.transpose(np.array([block, treatment]))
    return design_matrix
