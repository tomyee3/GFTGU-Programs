"""
MercPert physics module (ported from Bernard F. Schutz, Gravity from the Ground Up).

Encodes the restricted three-body problem:
- A circular binary (Sun + massive planet) in the x–y plane.
- A test particle ("Mercury") moving under their gravity.

Only physical constants are literal numbers here.
"""

import math

# Physical constants
G = 6.6726e-11          # Newton's gravitational constant (SI)
M_SUN = 1.98847e30      # Solar mass (kg)
AU = 1.495978707e11     # Astronomical unit (m)


def binary_parameters(m_sun_solar: float, m_planet_solar: float, binary_separation: float):
    """
    Compute binary radii and angular velocity for a circular binary.

    m_sun_solar, m_planet_solar: masses in units of solar masses.
    binary_separation: distance between the two bodies (m).
    """
    k_gravity = G * M_SUN  # same convention as Schutz: kGravity = G * M_sun

    m_sun = m_sun_solar
    m_planet = m_planet_solar

    r_sun = m_planet / (m_sun + m_planet) * binary_separation
    r_planet = binary_separation - r_sun

    omega = math.sqrt(k_gravity * (m_sun + m_planet) / binary_separation**3)

    return k_gravity, r_sun, r_planet, omega


def mercpert_derivatives(
    t: float,
    state: list[float],
    m_sun_solar: float,
    m_planet_solar: float,
    binary_separation: float,
):
    """
    Compute time derivatives for Mercury in the MercPert problem.

    state = [x_merc, y_merc, vx_merc, vy_merc]
    masses in solar units, separation in meters.
    """
    x_merc, y_merc, vx_merc, vy_merc = state

    k_gravity, r_sun, r_planet, omega = binary_parameters(
        m_sun_solar, m_planet_solar, binary_separation
    )

    # Binary positions at time t (circular orbits)
    c1 = math.cos(omega * t)
    s1 = math.sin(omega * t)

    x_sun = -r_sun * c1
    y_sun = -r_sun * s1

    x_planet = r_planet * c1
    y_planet = r_planet * s1

    # Displacement vectors from Sun and Planet to Mercury
    x_merc_sun = x_merc - x_sun
    y_merc_sun = y_merc - y_sun

    x_merc_planet = x_merc - x_planet
    y_merc_planet = y_merc - y_planet

    r_merc_sun = math.sqrt(x_merc_sun**2 + y_merc_sun**2)
    r_merc_planet = math.sqrt(x_merc_planet**2 + y_merc_planet**2)

    r_merc_sun3 = r_merc_sun**3
    r_merc_planet3 = r_merc_planet**3

    m_sun = m_sun_solar
    m_planet = m_planet_solar

    # Acceleration of Mercury: sum of contributions from Sun and Planet
    ax_merc = -k_gravity * (
        m_sun * x_merc_sun / r_merc_sun3 + m_planet * x_merc_planet / r_merc_planet3
    )
    ay_merc = -k_gravity * (
        m_sun * y_merc_sun / r_merc_sun3 + m_planet * y_merc_planet / r_merc_planet3
    )

    # Derivatives
    dxdt = vx_merc
    dydt = vy_merc
    dvxdt = ax_merc
    dvydt = ay_merc

    return [dxdt, dydt, dvxdt, dvydt], (x_sun, y_sun, x_planet, y_planet)
