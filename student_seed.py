"""
AI 321 / EE 298 -- Personalized Exercise Parameters
----------------------------------------------------
Run this once, at the very top of every machine exercise notebook or
script this term. It derives a seed and a few small parameters that are
unique and deterministic for YOUR official student number -- two
students will never get the same values by chance. Use the returned
dict wherever an exercise's "Personalize this exercise" box tells you
to (a subset size, a start offset, a random seed, a choice among
several provided variants, ...).

This is not a security mechanism. It exists so that (a) copied or
shared submissions are easy to spot, since two students' "correct"
numbers will not match, and (b) a generic AI-generated answer visibly
will not match your specific numbers unless it was actually run
against your specific values -- which requires you to have supplied
them and understood what came back.
"""
import hashlib
import numpy as np


def get_my_params(student_number):
    digest = hashlib.sha256(str(student_number).strip().encode()).hexdigest()
    seed = int(digest[:8], 16)
    return {
        "student_number": str(student_number).strip(),
        "seed": seed,                     # use as your master RNG seed
        "rng": np.random.default_rng(seed),
        "offset_small": seed % 30,        # e.g. a day/index offset, range 0-29
        "offset_large": seed % 3000,      # e.g. a row/index offset into a long series
        "subset_size": 30 + (seed % 21),  # e.g. 30-50, for "sample N series" tasks
        "choice_of_8": seed % 8,          # e.g. selecting 1 of 8 provided variants
    }


if __name__ == "__main__":
    # Example -- replace with your own official student number.
    params = get_my_params("2021-00000")
    for k, v in params.items():
        print(f"{k}: {v}")
