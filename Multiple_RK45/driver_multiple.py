# driver_multiple.py
"""
Driver module for Multiple (Gravity From the Ground Up).
Uses RK45 (solve_ivp) to integrate the N-body system.

Follows Schutz’s Java structure closely, but replaces
predictor–corrector + time-step halving with solve_ivp.
"""

import numpy as np
from scipy.integrate import solve_ivp
from physics_multiple import accelerations


def run_simulation(masses, xInit, yInit, zInit,
                   vInit, uInit, wInit,
                   t_max, dt_output):
    """
    Integrate the N-body system using RK45.

    Parameters
    ----------
    masses : array of masses (kg)
    xInit, yInit, zInit : initial positions
    vInit, uInit, wInit : initial velocities
    t_max : total simulation time (seconds)
    dt_output : time spacing between output samples

    Returns
    -------
    times : array of output times
    trajectories : list of arrays, one per body:
        each array has shape (len(times), 3)
    """

    n = len(masses)

    # Build initial state vector
    state0 = np.zeros(6 * n)
    for i in range(n):
        state0[6*i + 0] = xInit[i]
        state0[6*i + 1] = yInit[i]
        state0[6*i + 2] = zInit[i]
        state0[6*i + 3] = vInit[i]
        state0[6*i + 4] = uInit[i]
        state0[6*i + 5] = wInit[i]

    # Output times
    times = np.arange(0, t_max, dt_output)

    # Integrate
    sol = solve_ivp(
        fun=lambda t, y: accelerations(t, y, masses),
        t_span=(0, t_max),
        y0=state0,
        t_eval=times,
        method="RK45",
        rtol=1e-9,
        atol=1e-9
    )

    # Extract trajectories
    trajectories = []
    for i in range(n):
        xyz = sol.y[6*i:6*i+3, :].T
        trajectories.append(xyz)

    return times, trajectories
