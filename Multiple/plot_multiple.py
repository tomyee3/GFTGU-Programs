"""
Multiple: plotting module

Separates all plotting from the physics/driver logic.
"""

from typing import Dict, Any

import matplotlib.pyplot as plt
import numpy as np


def plot_trajectories(result: Dict[str, Any]) -> None:
    """
    Plot x-y trajectories of all bodies.
    """
    times = result["times"]
    positions = result["positions"]  # shape (n_steps, n_bodies, 3)
    n_steps, n_bodies, _ = positions.shape

    fig, ax = plt.subplots()
    colors = ["red", "green", "blue", "orange", "purple", "brown"]

    for i in range(n_bodies):
        body_pos = positions[:, i, :]
        x = body_pos[:, 0]
        y = body_pos[:, 1]
        color = colors[i % len(colors)]
        ax.plot(x, y, color=color, label=f"Body {i}")

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("Multiple orbits (trajectories)")
    ax.legend()
    ax.set_aspect("equal", "box")
    plt.tight_layout()
    plt.show()


def plot_current_positions(result: Dict[str, Any]) -> None:
    """
    Plot current positions at the last snapshot (x-y projection).
    """
    snapshots = result["snapshots"]
    if not snapshots:
        print("No snapshots to plot.")
        return

    last = snapshots[-1]
    positions = last["positions"]  # (n_bodies, 3)
    n_bodies = positions.shape[0]

    fig, ax = plt.subplots()
    colors = ["red", "green", "blue", "orange", "purple", "brown"]

    for i in range(n_bodies):
        x, y = positions[i, 0], positions[i, 1]
        color = colors[i % len(colors)]
        ax.scatter(x, y, color=color, label=f"Body {i}")

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(f"Multiple: current positions at t = {last['time']:.3e} s")
    ax.legend()
    ax.set_aspect("equal", "box")
    plt.tight_layout()
    plt.show()
