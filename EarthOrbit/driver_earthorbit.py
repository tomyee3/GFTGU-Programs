"""
driver_earthorbit.py

Driver for the EarthOrbit simulation.
Follows the structure of Bernard Schutz's Triana Java program closely,
including variable names and loop logic.
"""

import numpy as np
from physics_earthorbit import compute_acceleration, rEarth


def run_earth_orbit(h0=300.0, uInit=0.0, vInit=7900.0,
                    dt=0.4, maxSteps=15000):
    """
    Run the EarthOrbit simulation.

    Parameters:
        h0       — initial height above Earth's surface (meters)
        uInit    — initial vertical velocity (m/s)
        vInit    — initial horizontal velocity (m/s)
        dt       — timestep (seconds)
        maxSteps — maximum number of steps allowed

    Returns:
        xs, ys      — trajectory coordinates
        xEarth, yEarth — coordinates of Earth's surface curve
    """

    # Initial position: on the y-axis at rEarth + h0
    x = 0.0
    y = rEarth + h0

    # Initial velocities
    u0 = uInit
    v0 = vInit

    # Storage arrays (equivalent to xCoordinate[], yCoordinate[])
    xs = np.zeros(maxSteps)
    ys = np.zeros(maxSteps)

    xs[0] = x
    ys[0] = y

    # Compute initial radius
    r = np.sqrt(x*x + y*y)

    j = 1
    while r >= rEarth and j < maxSteps:
        # Acceleration components (Java: ax = -g*x/r, ay = -g*y/r)
        ax, ay = compute_acceleration(x, y)

        # Update velocities (Java: u1 = u0 + ax*dt, v1 = v0 + ay*dt)
        u1 = u0 + ax * dt
        v1 = v0 + ay * dt

        # Update positions using average velocity (Java: x = x + (u0+u1)/2*dt)
        x = x + (u0 + u1) * 0.5 * dt
        y = y + (v0 + v1) * 0.5 * dt

        # Update radius
        r = np.sqrt(x*x + y*y)

        # Store trajectory
        xs[j] = x
        ys[j] = y

        # Prepare for next step
        u0 = u1
        v0 = v1
        j += 1

    # Trim unused entries
    xs = xs[:j]
    ys = ys[:j]

    # Build Earth surface curve (Java used 400 points)
    angleStep = np.pi / 200
    xEarth = np.zeros(401)
    yEarth = np.zeros(401)

    for k in range(400):
        angle = angleStep * k
        xEarth[k] = rEarth * np.cos(angle)
        yEarth[k] = rEarth * np.sin(angle)

    # Close the circle
    xEarth[400] = xEarth[0]
    yEarth[400] = yEarth[0]

    return xs, ys, xEarth, yEarth
