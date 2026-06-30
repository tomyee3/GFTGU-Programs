"""
Main entry point for Binary orbit simulation.

Example parameters are set to values that roughly
produce an elliptical binary orbit of two equal-mass
stars. Users can overwrite these values as desired.

Based on Bernard F. Schutz, Gravity from the Ground Up,
Binary.java (CC license).
"""

from driver_binary import integrate_binary
from plot_binary import plot_binary, OutputType


def main():
    # Example initial conditions (SI units)
    # Two equal-mass bodies, symmetric positions and velocities.
    MA = 2.0e30  # kg
    MB = 2.0e30  # kg

    # Positions (meters)
    xInitA = -1.0e11
    yInitA = 0.0
    xInitB = 1.0e11
    yInitB = 0.0

    # Velocities (m/s) chosen to give a bound, non-circular orbit
    vInitA = 0.0
    uInitA = 1.5e4
    vInitB = 0.0
    uInitB = -1.5e4

    # Time-step and accuracy parameters
    dt = 1.0e4          # base time-step (s)
    max_steps = 5000    # maximum number of steps
    eps1 = 1.0e-2       # time-step accuracy threshold
    eps2 = 1.0e-3       # predictor–corrector accuracy threshold

    # Choose output type (can be changed by user)
    output_type: OutputType = "orbits"

    result = integrate_binary(
        MA=MA,
        MB=MB,
        xInitA=xInitA,
        yInitA=yInitA,
        vInitA=vInitA,
        uInitA=uInitA,
        xInitB=xInitB,
        yInitB=yInitB,
        vInitB=vInitB,
        uInitB=uInitB,
        dt=dt,
        max_steps=max_steps,
        eps1=eps1,
        eps2=eps2,
    )

    plot_binary(result, output_type)


if __name__ == "__main__":
    main()
