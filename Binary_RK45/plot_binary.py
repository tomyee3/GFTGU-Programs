# plot_binary.py
"""
Plot module for Schutz-style binary orbits.
Creative Commons BY-NC-SA 1.0 — faithful to Schutz's original Java output style.
"""

import matplotlib.pyplot as plt

def plot_orbits(data):
    xA, yA = data["xA"], data["yA"]
    xB, yB = data["xB"], data["yB"]

    plt.figure(figsize=(8, 8))
    plt.plot(xA, yA, label="Body A")
    plt.plot(xB, yB, label="Body B")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Binary Orbits (RK45)")
    plt.legend()
    plt.axis("equal")
    plt.grid(True)
    plt.show()
