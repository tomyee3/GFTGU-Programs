"""
Main entry point for Atmosphere (Python port)

User sets parameters here; they can overwrite the example values.
"""

from driver_atmosphere import AtmosphereParameters, AtmosphereModel, extract_output
from plot_atmosphere import plot_atmosphere


def main():
    # Example: Earth's atmosphere, rough values
    planet_name = "Earth"
    g_accel = 9.81          # m/s^2
    mu = 28.97              # mean molecular weight ~ air (proton masses)
    p0 = 1.013e5            # surface pressure ~ 1 atm (Pa)

    # Simple temperature profile: (altitude, temperature) pairs
    # You can replace these with more detailed data (e.g., from Table 7.1).
    h_points = [
        0.0,
        5_000.0,
        10_000.0,
        20_000.0,
        30_000.0,
        40_000.0,
    ]
    T_points = [
        288.0,  # ~15°C at sea level
        255.0,
        223.0,
        217.0,
        226.0,
        250.0,
    ]

    # Choose what to output: "Pressure", "Density", or "Temperature"
    output_type = "Pressure"

    params = AtmosphereParameters(
        planet_name=planet_name,
        g_accel=g_accel,
        mu=mu,
        p0=p0,
        h_points=h_points,
        T_points=T_points,
        output_type=output_type,
    )

    model = AtmosphereModel(params)
    result = model.run()
    curve_data = extract_output(result)
    plot_atmosphere(curve_data)


if __name__ == "__main__":
    main()
