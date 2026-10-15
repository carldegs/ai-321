"""AI 321 / EE 298 -- APRBS (Amplitude-modulated Pseudo-Random Binary
Sequence) generator, companion to generate_aprbs.m.

An APRBS generalizes a PRBS: instead of switching between just two fixed
+-1 levels, it holds a random amplitude level for a random duration, then
switches to a new random level, repeated for the full signal length.
"""
import numpy as np


def generate_aprbs(N, hold_range, amp_range, rng=None):
    """Generate an N-sample APRBS signal.

    Parameters
    ----------
    N : int
        Number of samples to generate.
    hold_range : (int, int)
        (min_hold, max_hold) segment length in samples; each segment's
        length is drawn uniformly (integer, inclusive) from this range.
    amp_range : (float, float)
        (min_amp, max_amp) amplitude level; each segment's amplitude is
        drawn uniformly (continuous) from this range.
    rng : numpy.random.Generator, optional
        Pass your own seeded generator (e.g. from get_my_params) for
        reproducibility. Defaults to an unseeded generator.

    Returns
    -------
    numpy.ndarray, shape (N,)

    Examples
    --------
    Small-amplitude APRBS (gentle excitation near a nominal operating
    point):
        u_small = generate_aprbs(2001, (20, 150), (-0.2, 0.2))

    Large-amplitude APRBS (more aggressive excitation across a wider
    range, matching the scale used to build your assigned s#.mat's own
    APRBS column):
        u_large = generate_aprbs(2001, (20, 150), (-1.0, 1.0))

    Then simulate your assigned system's response to either signal
    using python-control (or scipy.signal.lsim / your own state-space
    stepper), after loading your sys#.mat with e.g. scipy.io.loadmat.
    """
    if rng is None:
        rng = np.random.default_rng()
    u = np.zeros(N)
    idx = 0
    while idx < N:
        seglen = int(rng.integers(hold_range[0], hold_range[1] + 1))
        amp = rng.uniform(amp_range[0], amp_range[1])
        seg_end = min(idx + seglen, N)
        u[idx:seg_end] = amp
        idx = seg_end
    return u


if __name__ == "__main__":
    u_small = generate_aprbs(2001, (20, 150), (-0.2, 0.2))
    u_large = generate_aprbs(2001, (20, 150), (-1.0, 1.0))
    print("small-amplitude APRBS: min=%.3f max=%.3f" % (u_small.min(), u_small.max()))
    print("large-amplitude APRBS: min=%.3f max=%.3f" % (u_large.min(), u_large.max()))
