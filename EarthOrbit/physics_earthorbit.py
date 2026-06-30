"""
physics_earthorbit.py

Physics routines for EarthOrbit, rewritten from Bernard Schutz's
Triana Java program under the Creative Commons BY-NC-SA 1.0 license.

State vector:
    x  — x-position (meters)
    y  — y-position (meters)
    u  — x-velocity (m/s)
    v  — y-velocity (m/s)

Gravity:
    Magnitude g = 9.8 m/s^2 (constant, as in the original program)
    Direction always points toward the center of the Earth.
"""

import numpy as np

# Acceleration of gravity near Earth's surface (m/s^2)
g = 9.8

# Radius of Earth (meters)
rEarth = 6_378_200.0


def compute_acceleration(x, y):
    """
    Compute acceleration components toward Earth's center.

    Equivalent to Schutz's Java code:
        r = sqrt(x*x + y*y)
        ax = -g * x / r
        ay = -g * y / r
    """
    r = np.sqrt(x*x + y*y)
    ax = -g * x / r
    ay = -g * y / r
    return ax, ay
