"""
plot_orbit.py

Plotting routine for Orbit.
Displays the orbital trajectory with equal axis scaling.
"""

import matplotlib.pyplot as plt


def plot_orbit(xs, ys):
    plt.figure(figsize=(8, 8))
    plt.plot(xs, ys, linewidth=2, color="red", label="Orbit")
    plt.scatter([0], [0], color="orange", label="Central mass")
    plt.xlabel("x (meters)")
    plt.ylabel("y (meters)")
    plt.title("Orbit — Newtonian Planetary Motion")
    plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.show()
