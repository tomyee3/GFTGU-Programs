"""
MercPert plotting module.

Takes MercPertResult and produces orbit plots.
"""

import matplotlib.pyplot as plt
from driver_mercpert import MercPertResult


def plot_orbits(result: MercPertResult):
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.plot(result.x_sun, result.y_sun, color="red", label="Sun")
    ax.plot(result.x_planet, result.y_planet, color="green", label="Planet")
    ax.plot(result.x_merc, result.y_merc, color="blue", label="Mercury")

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("MercPert orbits")

    ax.legend()
    ax.grid(True)
    ax.set_aspect("equal", "box")

    # Scientific notation on axes for large distances
    ax.ticklabel_format(style="sci", axis="both", scilimits=(0, 0))

    plt.tight_layout()
    plt.show()
