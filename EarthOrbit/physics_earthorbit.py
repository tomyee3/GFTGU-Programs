"""
physics_earthorbit.py

Physical constants and gravitational acceleration law for the EarthOrbit
simulation (Newton's Cannon thought experiment).

The only literal numbers in this module are universal physical constants
and Earth's measured surface parameters.

Force law: a = g * (R_Earth / r)^2  directed toward center
           = g * R_Earth^2 / r^2    (correct inverse-square law)

This equals g = 9.8 m/s^2 at the surface (r = R_Earth) and falls off
correctly with altitude, producing closed elliptical orbits.
"""

import math

# Physical constants / Earth parameters
G_SURFACE = 9.8            # gravitational acceleration at Earth's surface (m/s^2)
R_EARTH   = 6_378_200.0   # mean radius of the Earth (m)

# Composite constant: k = g * R^2  (analogous to GM in the Orbit program)
# Numerically equals GM_Earth ≈ 3.987e14 m^3/s^2
_K = G_SURFACE * R_EARTH * R_EARTH


def compute_acceleration(x: float, y: float) -> tuple[float, float]:
    """
    Compute the gravitational acceleration components at position (x, y).

    Uses the correct inverse-square law:
        |a| = g * (R_Earth / r)^2 = k / r^2

    so that the acceleration equals g at the surface and falls off as 1/r^2,
    producing closed Keplerian ellipses for all eccentricities.

    Parameters
    ----------
    x, y : float
        Position of the projectile in metres (origin = Earth's centre).

    Returns
    -------
    ax, ay : float
        Acceleration components in m/s^2.
    """
    r2 = x * x + y * y
    r  = math.sqrt(r2)
    r3 = r * r2                  # r^3

    ax = -_K * x / r3
    ay = -_K * y / r3

    return ax, ay
