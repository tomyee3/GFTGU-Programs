"""
MercPert main module.

Sets example parameters (which the user can edit) and runs the simulation.
"""

from physics_mercpert import AU
from driver_mercpert import run_mercpert
from plot_mercpert import plot_orbits


def main():
    # Example parameters inspired by Schutz's MercPert description
    m_sun_solar = 1.0       # Sun mass in solar masses
    m_planet_solar = 0.1    # ~100 Jupiter masses
    binary_separation = 0.7 * AU  # separation between Sun and Planet (m)

    # Example initial conditions for Mercury (user can overwrite)
    x_init_merc = 0.5 * AU
    y_init_merc = 0.0
    vx_init_merc = 0.0
    vy_init_merc = 30000.0  # m/s, rough orbital speed scale

    dt = 2000.0             # time step (s)
    max_steps = 50000       # number of steps

    result = run_mercpert(
        m_sun_solar=m_sun_solar,
        m_planet_solar=m_planet_solar,
        binary_separation=binary_separation,
        x_init_merc=x_init_merc,
        y_init_merc=y_init_merc,
        vx_init_merc=vx_init_merc,
        vy_init_merc=vy_init_merc,
        dt=dt,
        max_steps=max_steps,
    )

    plot_orbits(result)


if __name__ == "__main__":
    main()
