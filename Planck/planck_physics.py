"""
planck_physics.py

Faithful Python port of Bernard Schutz's Planck program (Gravity From the Ground Up),
Creative Commons BY‑NC‑SA 1.0.

Contains only the physics: the Planck function and its small‑x and large‑x
approximations.
"""

import math

# ---------------------------------------------------------------------
# Planck function and approximations
# ---------------------------------------------------------------------

def planck_small_x(x: float) -> float:
    """
    Small‑x approximation used by Schutz:
        y = x^4
    """
    return x**4


def planck_large_x(x: float) -> float:
    """
    Large‑x approximation used by Schutz:
        y = exp(5 ln x − x)
    """
    return math.exp(5.0 * math.log(x) - x)


def planck_exact(x: float) -> float:
    """
    Full Planck function used by Schutz:
        y = x^5 / (exp(x) − 1)
    """
    return x**5 / (math.exp(x) - 1.0)
