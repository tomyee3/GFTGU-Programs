"""
main.py — Entry point for the Python port of the Star program.

This module sets example input parameters for a polytropic stellar
model (e.g. a solar-like star) and calls the driver and plot modules.
Users may overwrite these values to explore different stars.
"""

from driver_star import integrate_star
from plot_star import plot_star_structure


def main():
    # Example parameters for a solar-like star.
    # Users are encouraged to modify these.
    p_c = 2.5e16        # central pressure [Pa] (example value)
    T_c = 1.5e7         # central temperature [K] (example value)
    mu = 0.61           # mean molecular weight (solar composition)
    gamma = 5.0 / 3.0   # polytropic exponent (ideal monatomic gas)

    # Choose what to plot: "pressure", "density", "temperature", or "mass"
    output_type = "pressure"

    result = integrate_star(
        p_c=p_c,
        T_c=T_c,
        mu=mu,
        gamma=gamma,
        max_points=2000,
        output_type=output_type,
    )

    plot_star_structure(result)


if __name__ == "__main__":
    main()
