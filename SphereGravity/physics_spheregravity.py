"""
physics_spheregravity.py

Physics routines for SphereGravity, rewritten from Bernard Schutz's
Triana Java program under the Creative Commons BY-NC-SA 1.0 license.

The program computes the gravitational acceleration produced by a thin
spherical shell of radius 1 and thickness epsilon, by dividing the shell
into nDiv × nDiv tiles and treating each tile as a point mass.

The gravitational acceleration is computed at 1000 radii from r = 0
to r = 100, skipping r = 1 (the shell radius).
"""

import numpy as np


def compute_shell_mass(nDiv, epsilon=0.001):
    """
    Compute total mass of the spherical shell by summing tile masses.

    Equivalent to Schutz's Java code:
        dm = dTheta * dPhi * cos(theta) * epsilon
        mass += dm * nDiv
    """
    degToRad = np.pi / 180.0
    dPhi = 360.0 * degToRad / nDiv
    dTheta = 0.5 * dPhi

    theta = 0.5 * dTheta - 90 * degToRad
    mass = 0.0

    for _ in range(nDiv):
        dm = dTheta * dPhi * np.cos(theta) * epsilon
        mass += dm * nDiv
        theta += dTheta

    return mass


def compute_acceleration_profile(nDiv, outputType="acceleration", epsilon=0.001):
    """
    Compute gravitational acceleration at 1000 radii.

    Parameters:
        nDiv        — number of angular divisions
        outputType  — "acceleration" or "relative difference"
        epsilon     — shell thickness

    Returns:
        radius[]        — radii at which acceleration is evaluated
        acceleration[]  — computed acceleration or relative difference
    """

    degToRad = np.pi / 180.0
    dPhi = 360.0 * degToRad / nDiv
    dTheta = 0.5 * dPhi

    # Precompute shell mass
    mass = compute_shell_mass(nDiv, epsilon)

    radius = np.zeros(1000)
    acceleration = np.zeros(1000)

    # Loop over radii
    for j in range(1000):
        r = j * 0.1
        radius[j] = r

        if j == 10:  # r = 1 (shell radius)
            acceleration[j] = 0.0
            continue

        accel = 0.0
        theta = 0.5 * dTheta - 90 * degToRad

        # Loop over latitude rings
        for _ in range(nDiv):
            s = np.sin(theta)
            dist = np.sqrt(1 + r*r + 2*r*s)
            dm = dTheta * dPhi * np.cos(theta) * epsilon
            x = r + s
            dAccel = dm * x / (dist**3)
            accel += dAccel * nDiv
            theta += dTheta

        acceleration[j] = accel

    # Relative difference mode
    if outputType == "relative difference":
        # Newtonian prediction outside shell: g = mass / r^2
        newton_outside = mass / (radius[11]**2)

        for j in range(1000):
            r = radius[j]
            if r < 1.0:
                # Inside shell: Newtonian acceleration = 0
                acceleration[j] = acceleration[j] / newton_outside
            else:
                newton = mass / (r*r)
                acceleration[j] = (acceleration[j] - newton) / newton

    return radius, acceleration
