"""
plot_spheregravity.py

Plotting routine for SphereGravity.
Displays acceleration or relative difference vs radius.
"""

import matplotlib.pyplot as plt


def plot_spheregravity(radius, acceleration, outputType="acceleration"):
    plt.figure(figsize=(8, 6))
    plt.plot(radius, acceleration, linewidth=2)

    plt.xlabel("Radius r")
    if outputType == "acceleration":
        plt.ylabel("Acceleration (m/s²)")
        plt.title("Gravitational Acceleration of Thin Spherical Shell")
    else:
        plt.ylabel("Relative Difference")
        plt.title("Relative Difference from Newton's Theorem")

    plt.grid(True)
    plt.show()
