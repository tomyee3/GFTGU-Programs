"""
MercPert driver module.

Solves the restricted three-body problem using a fixed-step RK4 integrator.
Produces structured output for plotting.
"""

from dataclasses import dataclass
from typing import List

from physics_mercpert import mercpert_derivatives


@dataclass
class MercPertResult:
    t: List[float]
    x_sun: List[float]
    y_sun: List[float]
    x_planet: List[float]
    y_planet: List[float]
    x_merc: List[float]
    y_merc: List[float]


def rk4_step(f, t, y, dt, *args):
    k1, aux1 = f(t, y, *args)
    y2 = [yi + 0.5 * dt * k1i for yi, k1i in zip(y, k1)]
    k2, aux2 = f(t + 0.5 * dt, y2, *args)
    y3 = [yi + 0.5 * dt * k2i for yi, k2i in zip(y, k2)]
    k3, aux3 = f(t + 0.5 * dt, y3, *args)
    y4 = [yi + dt * k3i for yi, k3i in zip(y, k3)]
    k4, aux4 = f(t + dt, y4, *args)

    y_next = [
        yi + dt * (k1i + 2 * k2i + 2 * k3i + k4i) / 6.0
        for yi, k1i, k2i, k3i, k4i in zip(y, k1, k2, k3, k4)
    ]

    # We only need auxiliary data from the final evaluation for plotting
    return y_next, aux4


def run_mercpert(
    m_sun_solar: float,
    m_planet_solar: float,
    binary_separation: float,
    x_init_merc: float,
    y_init_merc: float,
    vx_init_merc: float,
    vy_init_merc: float,
    dt: float,
    max_steps: int,
) -> MercPertResult:
    """
    Integrate Mercury's orbit in the MercPert setup.
    """

    t = 0.0
    state = [x_init_merc, y_init_merc, vx_init_merc, vy_init_merc]

    t_list = []
    x_sun_list = []
    y_sun_list = []
    x_planet_list = []
    y_planet_list = []
    x_merc_list = []
    y_merc_list = []

    for _ in range(max_steps):
        t_list.append(t)
        # Get current auxiliary positions for plotting
        _, (x_sun, y_sun, x_planet, y_planet) = mercpert_derivatives(
            t, state, m_sun_solar, m_planet_solar, binary_separation
        )
        x_sun_list.append(x_sun)
        y_sun_list.append(y_sun)
        x_planet_list.append(x_planet)
        y_planet_list.append(y_planet)
        x_merc_list.append(state[0])
        y_merc_list.append(state[1])

        # Advance one RK4 step
        state, _ = rk4_step(
            mercpert_derivatives,
            t,
            state,
            dt,
            m_sun_solar,
            m_planet_solar,
            binary_separation,
        )
        t += dt

    return MercPertResult(
        t=t_list,
        x_sun=x_sun_list,
        y_sun=y_sun_list,
        x_planet=x_planet_list,
        y_planet=y_planet_list,
        x_merc=x_merc_list,
        y_merc=y_merc_list,
    )
