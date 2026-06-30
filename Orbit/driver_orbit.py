"""
driver_orbit.py

Driver for the Orbit simulation.
Follows the structure of Bernard Schutz's Triana Java program closely,
including variable names, adaptive time-step logic, predictor-corrector
iteration, and orbit-closure detection.
"""

import numpy as np
from physics_orbit import compute_acceleration


def run_orbit(
    xInit=4.6e10, yInit=0.0,
    vxInit=0.0, vyInit=58980.0,
    k=1.327e20,          # GM for the Sun
    dt0=1e4,             # initial time-step
    maxSteps=20000,
    eps1=0.05,           # time-step accuracy threshold
    eps2=1e-4,           # predictor-corrector accuracy threshold
    output="orbit"       # "orbit", "velocity", "position_time", "velocity_time", "energy"
):
    """
    Run the Orbit simulation.

    Parameters match Schutz's Java program:
        xInit, yInit   — initial position
        vxInit, vyInit — initial velocity
        k              — GM of central mass
        dt0            — initial time-step
        maxSteps       — maximum number of steps
        eps1           — threshold for time-step reduction
        eps2           — threshold for predictor-corrector convergence
        output         — type of output data

    Returns:
        Data arrays depending on output mode.
    """

    # Initial state
    x = xInit
    y = yInit
    vx = vxInit
    vy = vyInit

    # Arrays for storing trajectory
    xs = np.zeros(maxSteps)
    ys = np.zeros(maxSteps)
    xs[0] = x
    ys[0] = y

    # Initial time-step
    dt1 = dt0

    # Orbit closure detection
    anglePrev = np.arctan2(y, x)
    halfOrbit = False
    fullOrbit = False
    nOrbits = 0

    j = 1
    while j < maxSteps and nOrbits < 1:
        # Compute acceleration at beginning of step
        ax0, ay0 = compute_acceleration(x, y, k)

        # Predictor step: constant acceleration assumption
        dv = ax0 * dt1
        du = ay0 * dt1
        dx = vx * dt1
        dy = vy * dt1

        ddx0 = dv * dt1 / 2
        ddy0 = du * dt1 / 2

        x1 = x + dx + ddx0
        y1 = y + dy + ddy0

        # Acceleration at predicted position
        ax1, ay1 = compute_acceleration(x1, y1, k)

        # Time-step adjustment test
        if abs(ax1 - ax0) + abs(ay1 - ay0) > eps1 * (abs(ax0) + abs(ay0)):
            dt1 /= 2
            continue

        # Predictor-corrector iteration
        testPrediction = abs(ddx0) + abs(ddy0)
        ddx1 = ddx0
        ddy1 = ddy0

        for _ in range(10):
            dv = (ax0 + ax1) * dt1 / 2
            du = (ay0 + ay1) * dt1 / 2

            ddx1 = dv * dt1 / 2
            ddy1 = du * dt1 / 2

            if abs(ddx1 - ddx0) + abs(ddy1 - ddy0) > eps2 * testPrediction:
                ddx0 = ddx1
                ddy0 = ddy1

                x1 = x + dx + ddx0
                y1 = y + dy + ddy0

                ax1, ay1 = compute_acceleration(x1, y1, k)
            else:
                break

        # Commit step
        x += dx + ddx1
        y += dy + ddy1
        vx += dv
        vy += du

        xs[j] = x
        ys[j] = y

        # Orbit closure detection using angle
        angleNow = np.arctan2(y, x)
        if angleNow > np.pi:
            angleNow -= 2*np.pi
        elif angleNow < -np.pi:
            angleNow += 2*np.pi

        if not halfOrbit:
            halfOrbit = (angleNow < 0)
        else:
            fullOrbit = (angleNow > 0)

        if fullOrbit:
            nOrbits += 1
            fullOrbit = False
            halfOrbit = False

        j += 1

    # Trim arrays
    xs = xs[:j]
    ys = ys[:j]

    # Output modes
    if output == "orbit":
        return xs, ys

    elif output == "velocity":
        return vx, vy

    elif output == "position_time":
        ts = np.arange(j) * dt1
        return ts, xs, ys

    elif output == "velocity_time":
        ts = np.arange(j) * dt1
        return ts, vx, vy

    elif output == "energy":
        ts = np.arange(j) * dt1
        r = np.sqrt(xs*xs + ys*ys)
        v2 = vx*vx + vy*vy
        KE = 0.5 * v2
        PE = -k / r
        TE = KE + PE
        return ts, KE, PE, TE

    else:
        return xs, ys
