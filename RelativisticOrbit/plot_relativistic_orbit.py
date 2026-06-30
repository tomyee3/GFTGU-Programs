"""
RelativisticOrbit plot module (Gravity From the Ground Up)

This module takes the structured output from the driver and produces
a 2D plot of the orbit and the horizon, similar in spirit to SGTGrapher.
"""

import matplotlib.pyplot as plt
from driver_relativistic_orbit import RelativisticOrbitResult


def plot_relativistic_orbit(result: RelativisticOrbitResult) -> None:
    """
    Plot the relativistic orbit and the Schwarzschild horizon.
    """

    fig, ax = plt.subplots(figsize=(6, 6))

    # Orbit
    ax.plot(result.x, result.y, label="Orbit", color="blue")

    # Horizon
    ax.plot(result.horizon_x, result.horizon_y, label="Horizon", color="red")

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("RelativisticOrbit (Schwarzschild test particle)")

    ax.set_aspect("equal", "box")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.show()
