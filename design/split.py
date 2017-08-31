""" Generate a Strip Design """
import numpy as np


def split(fixed_treatments, random_treatments, reps, randomize=None, seed=None):
    """ Generate a Split Plot design

    Args:
        fixed_treatments: The treatments to be applied to each plot
        random_treatments: The treatments to be randomized within a plot
        reps: The number of times each treatment is replicated
        randomize: A boolean indicating if the order of treatments should be
            randomized.  If this is for an actual trial, this should be True
        seed: The seed for used by numpy.random.seed()

    Returns:
        ndarray: The design matrix whose columns are the block number, the plot
            number, the sub plot number, the plot treatment and the sub plot
            treatment
    """
    if seed is not None:
        np.random.seed(seed)
    n_f = len(fixed_treatments)
    n_r = len(random_treatments)
    # Within block n
    n_b = n_f * n_r
    block = []
    plot = []
    sub_plot = [1, 2, 3] * n_f * reps
    plot_treatment = []
    sub_plot_treatment = []
    counter = 0
    for b in range(reps):
        block.extend([b + 1] * n_b)
        if randomize:
            np.random.shuffle(fixed_treatments)
        for p in range(n_f):
            if randomize:
                np.random.shuffle(random_treatments)
            plot_treatment.extend([fixed_treatments[p]] * n_r)
            sub_plot_treatment.extend(random_treatments)
            counter += 1
            plot.extend([counter] * n_r)
    design_matrix = np.array(
        [block, plot, sub_plot, plot_treatment, sub_plot_treatment])
    return design_matrix
