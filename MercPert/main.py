"""
MercPert main module (non-RK45 version)

Example entry point for running the MercPert simulation
and plotting the orbits.

All parameters here are examples that users can overwrite.
"""

from physics_mercpert import (
    BinarySystemParams,
    MercuryInitialConditions,
    AU,
)
from driver_mercpert import MercPertRunParams, run_mercpert
from plot_mercpert import plot_orbits


def main():
    # Example binary system: Sun + super-Jupiter closer than Jupiter,
    # roughly at Venus's distance (~0.7 AU).
    binary_params = BinarySystemParams(
        m_sun_solar=1.0,          # Sun-like central star
        m_planet_solar=0.1,      # ~100 times Jupiter's mass
        binary_separation=0.7 * AU,
    )

    # Example initial conditions for "Mercury"
    # These are illustrative; users can adjust to reproduce
    # the book's figures or explore chaotic behavior.
    merc_ic = MercuryInitialConditions(
        x_init=1.0 * AU,         # start outside the binary
        y_init=0.0,
        vx_init=0.0,
        vy_init=15000.0,         # some tangential velocity (m/s)
    )

    # Driver parameters, echoing Schutz's style:
    run_params = MercPertRunParams(
        dt=2000.0,       # initial time-step (s), as in examples
        max_steps=150000,
        eps1=0.05,       # time-step halving threshold
        eps2=0.01,       # predictor-corrector convergence threshold
    )

    output = run_mercpert(binary_params, merc_ic, run_params)
    plot_orbits(output, title="MercPert orbits (non-RK45)")


if __name__ == "__main__":
    main()
