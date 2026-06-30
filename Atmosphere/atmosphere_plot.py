import matplotlib.pyplot as plt
import numpy as np
from atmosphere_physics import AtmosphereModel


def plot_atmosphere(
    planet_name: str,
    g_accel: float,
    mu: float,
    p0: float,
    temperature_pairs,
    output_type: str = "Pressure",
    measured_alt=None,
    measured_values=None,
    log_y: bool = True,
):
    """
    Plot Atmosphere model curve, optionally overlaying measured data as dots.

    measured_alt, measured_values: arrays of measured altitude (m) and quantity
    (same units as output_type). For the book-style overlay, convert altitude to km.
    """
    model = AtmosphereModel(
        planet_name=planet_name,
        g_accel=g_accel,
        mu=mu,
        p0=p0,
        temperature_pairs=temperature_pairs,
        output_type=output_type,
    )

    alt, y, y_label = model.compute_output_curve()
    alt_km = alt / 1000.0

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(alt_km, y, label=f"{planet_name} model")

    if measured_alt is not None and measured_values is not None:
        ax.scatter(
            np.array(measured_alt) / 1000.0,
            measured_values,
            color="black",
            s=20,
            label="Measured data",
        )

    ax.set_xlabel("Altitude (km)")
    ax.set_ylabel(y_label)

    if log_y:
        ax.set_yscale("log")

    ax.set_title(f"{planet_name} atmosphere: {output_type}")
    ax.grid(True, which="both", ls=":")
    ax.legend()
    plt.tight_layout()
    return fig, ax
