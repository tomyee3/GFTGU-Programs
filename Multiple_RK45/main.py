# main.py
"""
Main entry point for Multiple (Gravity From the Ground Up).
User sets parameters here.
"""

import numpy as np
from driver_multiple import run_simulation
from plot_multiple import plot_trajectories, plot_positions


if __name__ == "__main__":

    # -----------------------------
    # Example initial conditions
    # (faithful to Schutz’s defaults)
    # -----------------------------

    nBodies = 3

    masses = np.array([
        1.0 * 1.989e30,   # Sun
        1.0 * 1.989e30,   # Sun-like
        1.0 * 1.989e30    # Sun-like
    ])

    xInit = np.array([4.6e10, -4.6e10, 0.0])
    yInit = np.array([0.0, 0.0, 4.6e10])
    zInit = np.array([0.0, 0.0, 0.0])

    vInit = np.array([0.0, 0.0, -30000.0])
    uInit = np.array([30000.0, -30000.0, 0.0])
    wInit = np.array([0.0, 0.0, 0.0])

    # Simulation parameters
    t_max = 3.0e7        # total time (seconds)
    dt_output = 2.0e4    # spacing between output samples

    # Run simulation
    times, trajectories = run_simulation(
        masses, xInit, yInit, zInit,
        vInit, uInit, wInit,
        t_max, dt_output
    )

    # Plot trajectories
    labels = ["Body 1", "Body 2", "Body 3"]
    plot_trajectories(trajectories, labels)
