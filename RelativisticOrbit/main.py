"""
RelativisticOrbit main module (Gravity From the Ground Up)

User-facing entry point: set parameters, run the driver, and call the plotter.
Example values are provided and can be edited by the user.
"""

from driver_relativistic_orbit import (
    RelativisticOrbitParams,
    integrate_relativistic_orbit,
)
from plot_relativistic_orbit import plot_relativistic_orbit


def main():
    # Example parameters (close to Schutz defaults)
    params = RelativisticOrbitParams(
        x_init=3.0e3,      # starting radius (m), near horizon for 1 M_sun
        u_init=2.0e7,      # initial tangential velocity (m/s)
        dt=1e-4,           # time step (s)
        max_steps=20000,   # maximum number of steps
        max_orbits=10,     # number of orbits to compute
        eps1=0.05,         # time-step accuracy
        eps2=0.01,         # predictor–corrector accuracy
    )

    result = integrate_relativistic_orbit(params)
    print(f"Completed orbits: {result.n_orbits}")
    print(f"Final step index: {result.final_step}")
    print(f"Fell into hole: {result.fell_into_hole}")

    plot_relativistic_orbit(result)


if __name__ == "__main__":
    main()
