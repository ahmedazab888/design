""" Completely Randomized Design """
import numpy as np


def cr(treatments, reps, seed=None):
    """ Generates a completely randomized design

    A completely randomized design randomizes each treatment `reps` number of
    times to subjects.

    Args:
        treatments: A list of treatments subjects will be randomized to.
        reps: The number of times each treatment will be replicated.  If `reps`
            is an integer, each treatment will be replicated `reps` times.  If
            `reps` is a list, each element is the number of times the
            corresponding treatment is randomized.  In this case, `reps` must
            have as many elements as `treatments`;
        seed: The seed for used by numpy.random.seed()

    Raises:
        ValueError: if `reps` is a list whose length is not the same as
            `treatments` or `reps` is an integer whose value is less than 2 or
            `reps` is neither a list nor an integer

    Returns:
        ndarray: The design matrix whose columns are the repitition number
            and the treatment.
    """
    n_trt = len(treatments)
    if isinstance(reps, list):
        if not n_trt == len(reps):
            raise ValueError('`reps` must have a length of {}'.format(n_trt))
    elif isinstance(reps, int):
        if reps < 2:
            raise ValueError('`reps` ({}) must be greater than 1'.format(reps))
        reps = [reps] * n_trt
    else:
        raise ValueError('`reps` ({}) must an integer greater than 1'.format(reps))

    treatment = []
    rep = []
    for idx, r in enumerate(reps):
        treatment.extend([treatments[idx]] * r)
        rep.extend(list(range(1, r + 1)))

    design_matrix = np.array([rep, treatment])

    if seed:
        np.random.seed(seed)
    np.random.shuffle(design_matrix)

    return design_matrix
