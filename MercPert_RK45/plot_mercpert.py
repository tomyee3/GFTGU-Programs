"""
MercPert plot module.

Renders the trajectories of all three bodies (Sun, Planet, Mercury) in the
xy-plane from a MercPertResult produced by run_mercpert().
"""

import matplotlib.pyplot as plt

from driver_mercpert import MercPertResult


def plot_orbits(result: MercPertResult, title: str = "MercPert Orbits (RK45)") -> None:
    """
    Plot the trajectories of the Sun, Planet, and Mercury.

    Parameters
    ----------
    result : MercPertResult returned by run_mercpert().
    title  : Figure title string.
    """
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.plot(result.x_sun,    result.y_sun,    color="red",   linewidth=0.8,
            label="Sun")
    ax.plot(result.x_planet, result.y_planet, color="green", linewidth=0.8,
            label="Planet")
    ax.plot(result.x_merc,   result.y_merc,   color="blue",  linewidth=0.6,
            label="Mercury")

    # Mark initial positions
    ax.plot(result.x_sun[0],    result.y_sun[0],    "ro", markersize=5)
    ax.plot(result.x_planet[0], result.y_planet[0], "go", markersize=5)
    ax.plot(result.x_merc[0],   result.y_merc[0],   "bo", markersize=5)

    ax.set_aspect("equal")
    ax.ticklabel_format(style="sci", axis="both", scilimits=(0, 0))
    ax.set_xlabel("x  [m]")
    ax.set_ylabel("y  [m]")
    ax.set_title(title)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, linewidth=0.4, alpha=0.5)

    plt.tight_layout()
    plt.show()
