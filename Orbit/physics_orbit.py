"""
physics_orbit.py

Physics routines for Orbit, rewritten from Bernard Schutz's Triana Java
program under the Creative Commons BY-NC-SA 1.0 license.

State vector:
    x, y  — position (meters)
    vx, vy — velocity (m/s)

Gravity:
    Acceleration = -k * (x/r^3, y/r^3)
    where k = G*M (Newton's gravitational constant times central mass)
"""

import numpy as np


def compute_acceleration(x, y, k):
    """
    Compute Newtonian gravitational acceleration components.

    Equivalent to Schutz's Java code:
        r2 = x*x + y*y
        r = sqrt(r2)
        r3 = r * r2
        ax = -k * x / r3
        ay = -k * y / r3
    """
    r2 = x*x + y*y
    r = np.sqrt(r2)
    r3 = r * r2
    ax = -k * x / r3
    ay = -k * y / r3
    return ax, ay
