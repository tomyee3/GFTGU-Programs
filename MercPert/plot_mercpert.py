"""
MercPert plotting module

Separates plotting from physics and driver logic.
"""

import matplotlib.pyplot as plt
from driver_mercpert import MercPertOutput


def plot_orbits(output: MercPertOutput,
                title: str = "MercPert orbits") -> None:
    """
    Plot the orbits of Sun, Planet, and Mercury in the x-y plane.
    """

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.plot(output.sun_x, output.sun_y, color="red", label="Sun")
    ax.plot(output.planet_x, output.planet_y, color="green", label="Planet")
    ax.plot(output.merc_x, output.merc_y, color="blue", label="Mercury")

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(title)
    ax.legend()
    ax.set_aspect("equal", "box")

    # Use scientific notation for axes
    ax.ticklabel_format(style="sci", axis="both", scilimits=(0, 0))

    plt.tight_layout()
    plt.show()
