"""
MercPert physics module.

Defines physical constants, binary orbit geometry, and the right-hand-side
function for Mercury's equation of motion.  The RHS is written to return a
plain NumPy array so that it can be passed directly to
scipy.integrate.solve_ivp.
"""

import numpy as np

# ── Physical constants ──────────────────────────────────────────────────────
G     = 6.6726e-11          # gravitational constant  [N m^2 kg^-2]
M_SUN = 1.98847e30          # solar mass              [kg]
AU    = 1.495978707e11      # astronomical unit       [m]


# ── Binary orbit geometry ───────────────────────────────────────────────────

def binary_parameters(m_sun_solar: float,
                      m_planet_solar: float,
                      binary_separation: float) -> tuple:
    """
    Compute Keplerian parameters for the Sun–Planet binary.

    Parameters
    ----------
    m_sun_solar      : Sun mass in solar-mass units.
    m_planet_solar   : Planet mass in solar-mass units.
    binary_separation: Centre-to-centre separation [m].

    Returns
    -------
    k_gravity : G * M_sun_SI          [m^3 s^-2]
    r_sun     : Sun's orbital radius about the barycentre   [m]
    r_planet  : Planet's orbital radius about the barycentre [m]
    omega     : Binary angular velocity  [rad s^-1]
    """
    m_sun_si    = m_sun_solar    * M_SUN
    m_planet_si = m_planet_solar * M_SUN
    m_total_si  = m_sun_si + m_planet_si

    k_gravity = G * m_sun_si
    r_sun     = (m_planet_si / m_total_si) * binary_separation
    r_planet  = binary_separation - r_sun
    omega     = np.sqrt(G * m_total_si / binary_separation**3)

    return k_gravity, r_sun, r_planet, omega


def binary_positions(t, r_sun: float, r_planet: float, omega: float):
    """
    Cartesian positions of the Sun and Planet at time t.

    t may be a scalar or a NumPy array; the return values match its shape.

    Convention (matching the original Schutz Java code):
      Sun   starts on the negative x-axis at t = 0.
      Planet starts on the positive x-axis at t = 0.
    """
    phase    = omega * t
    x_sun    = -r_sun    * np.cos(phase)
    y_sun    = -r_sun    * np.sin(phase)
    x_planet =  r_planet * np.cos(phase)
    y_planet =  r_planet * np.sin(phase)
    return x_sun, y_sun, x_planet, y_planet


# ── Right-hand side for scipy.integrate.solve_ivp ──────────────────────────

def mercpert_rhs(t: float,
                 state,
                 m_sun_solar: float,
                 m_planet_solar: float,
                 binary_separation: float) -> np.ndarray:
    """
    Time derivative of Mercury's state vector.

    State vector:  [x, y, vx, vy]
    Returns:       [vx, vy, ax, ay]  as a plain NumPy array.

    This signature is compatible with scipy.integrate.solve_ivp:
        solve_ivp(mercpert_rhs, t_span, y0, args=(...))

    The gravitational acceleration on Mercury is the vector sum of the
    Newtonian pulls from both binary members evaluated at time t.
    """
    x, y, vx, vy = state

    _, r_sun, r_planet, omega = binary_parameters(
        m_sun_solar, m_planet_solar, binary_separation
    )

    m_sun_si    = m_sun_solar    * M_SUN
    m_planet_si = m_planet_solar * M_SUN

    # Binary positions at the current time
    xs, ys, xp, yp = binary_positions(t, r_sun, r_planet, omega)

    # Displacement vectors from each binary member to Mercury
    dx_sun    = x - xs
    dy_sun    = y - ys
    dx_planet = x - xp
    dy_planet = y - yp

    r_sun_merc3    = (dx_sun**2    + dy_sun**2)    ** 1.5
    r_planet_merc3 = (dx_planet**2 + dy_planet**2) ** 1.5

    ax = -G * (m_sun_si    * dx_sun    / r_sun_merc3
             + m_planet_si * dx_planet / r_planet_merc3)
    ay = -G * (m_sun_si    * dy_sun    / r_sun_merc3
             + m_planet_si * dy_planet / r_planet_merc3)

    return np.array([vx, vy, ax, ay])
