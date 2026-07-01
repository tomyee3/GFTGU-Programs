"""
plot_star.py — Plotting routines for the Star program.

This module takes the structured output from driver.integrate_star
and produces graphs of stellar structure using matplotlib.
"""

from typing import Dict

import matplotlib.pyplot as plt


def plot_star_structure(result: Dict):
    """
    Plot the chosen quantity versus radius.

    The result dictionary is expected to contain:
      - "radius"
      - "pressure"
      - "density"
      - "temperature"
      - "mass"
      - "output_type"
    """
    radius = result["radius"]
    output_type = result.get("output_type", "pressure")

    if output_type == "pressure":
        y = result["pressure"]
        ylabel = "Pressure [Pa]"
    elif output_type == "density":
        y = result["density"]
        ylabel = "Density [kg/m³]"
    elif output_type == "temperature":
        y = result["temperature"]
        ylabel = "Temperature [K]"
    elif output_type == "mass":
        y = result["mass"]
        ylabel = "Enclosed mass [kg]"
    else:
        raise ValueError(f"Unknown output_type: {output_type}")

    plt.figure()
    plt.plot(radius, y)
    plt.xlabel("Radius [m]")
    plt.ylabel(ylabel)
    plt.title(f"Stellar structure: {output_type} vs radius")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
