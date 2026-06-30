import matplotlib.pyplot as plt
from atmosphere_plot import plot_atmosphere

if __name__ == "__main__":
    # Simple Earth-like example (you can replace with Table 7.1 values)
    temperature_pairs = [
        (0.0, 288.0),
        (11000.0, 216.0),
        (20000.0, 216.0),
        (32000.0, 228.0),
        (47000.0, 270.0),
        (51000.0, 270.0),
        (71000.0, 214.0),
        (84852.0, 186.0),
    ]

    # Example measured data arrays (altitude in m, pressure in Pa, density in kg/m^3)
    # Replace with your actual book data if desired.
    measured_alt = [0.0, 10000.0, 20000.0, 30000.0, 40000.0, 50000.0, 60000.0, 70000.0]
    measured_pressure = [1.0e5, 2.6e4, 5.5e3, 1.2e3, 3.0e2, 8.0e1, 2.0e1, 5.0]
    measured_density = [1.2, 0.41, 0.088, 0.018, 0.004, 0.001, 3e-4, 1e-4]

    # Pressure plot with overlay
    fig_p, ax_p = plot_atmosphere(
        planet_name="Earth",
        g_accel=9.81,
        mu=28.97,  # mean molecular weight ~ air
        p0=1.013e5,
        temperature_pairs=temperature_pairs,
        output_type="Pressure",
        measured_alt=measured_alt,
        measured_values=measured_pressure,
        log_y=True,
    )

    # Density plot with overlay
    fig_rho, ax_rho = plot_atmosphere(
        planet_name="Earth",
        g_accel=9.81,
        mu=28.97,
        p0=1.013e5,
        temperature_pairs=temperature_pairs,
        output_type="Density",
        measured_alt=measured_alt,
        measured_values=measured_density,
        log_y=True,
    )

    plt.show()
