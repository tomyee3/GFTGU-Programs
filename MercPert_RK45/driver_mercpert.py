"""
MercPert driver module.

Integrates Mercury's orbit in the restricted three-body (Sun + Planet + Mercury)
problem using scipy.integrate.solve_ivp with method='RK45'.

The binary members move on analytically prescribed circular orbits; Mercury is
a Newtonian test particle.  After integration the binary positions are
reconstructed at every output time point from the analytical formulae so that
all three trajectories can be plotted.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List

from scipy.integrate import solve_ivp

from physics_mercpert import (
    mercpert_rhs,
    binary_parameters,
    binary_positions,
)


# ── Output container ────────────────────────────────────────────────────────

@dataclass
class MercPertResult:
    """
    Trajectory data for all three bodies at every output time point.

    All position arrays are in metres; t is in seconds.
    """
    t:        List[float] = field(default_factory=list)
    x_sun:    List[float] = field(default_factory=list)
    y_sun:    List[float] = field(default_factory=list)
    x_planet: List[float] = field(default_factory=list)
    y_planet: List[float] = field(default_factory=list)
    x_merc:   List[float] = field(default_factory=list)
    y_merc:   List[float] = field(default_factory=list)


# ── Integration driver ───────────────────────────────────────────────────────

def run_mercpert(
    m_sun_solar:       float,
    m_planet_solar:    float,
    binary_separation: float,
    x_init_merc:       float,
    y_init_merc:       float,
    vx_init_merc:      float,
    vy_init_merc:      float,
    t_max:             float,
    dt_output:         float = 2000.0,
    rtol:              float = 1e-9,
    atol:              float = 1e-9,
) -> MercPertResult:
    """
    Integrate Mercury's orbit using the RK45 adaptive integrator.

    Parameters
    ----------
    m_sun_solar       : Sun mass in solar-mass units.
    m_planet_solar    : Planet mass in solar-mass units.
    binary_separation : Centre-to-centre binary separation [m].
    x_init_merc       : Mercury initial x-position [m].
    y_init_merc       : Mercury initial y-position [m].
    vx_init_merc      : Mercury initial x-velocity [m/s].
    vy_init_merc      : Mercury initial y-velocity [m/s].
    t_max             : Total simulation time [s].
    dt_output         : Output sampling interval [s].
                        solve_ivp uses t_eval = np.arange(0, t_max, dt_output).
                        The integrator's internal adaptive steps are independent
                        of this spacing and are chosen automatically to satisfy
                        the rtol/atol tolerances.
    rtol              : Relative error tolerance for solve_ivp.
    atol              : Absolute error tolerance for solve_ivp.

    Returns
    -------
    MercPertResult with positions of all three bodies at every output point.
    """

    y0     = [x_init_merc, y_init_merc, vx_init_merc, vy_init_merc]
    t_span = (0.0, t_max)
    t_eval = np.arange(0.0, t_max, dt_output)

    args = (m_sun_solar, m_planet_solar, binary_separation)

    sol = solve_ivp(
        mercpert_rhs,
        t_span,
        y0,
        method='RK45',
        t_eval=t_eval,
        args=args,
        rtol=rtol,
        atol=atol,
        dense_output=False,
    )

    if not sol.success:
        raise RuntimeError(f"solve_ivp failed: {sol.message}")

    # Reconstruct binary positions analytically at every output time
    _, r_sun, r_planet, omega = binary_parameters(
        m_sun_solar, m_planet_solar, binary_separation
    )
    xs, ys, xp, yp = binary_positions(sol.t, r_sun, r_planet, omega)

    return MercPertResult(
        t        = sol.t.tolist(),
        x_sun    = xs.tolist(),
        y_sun    = ys.tolist(),
        x_planet = xp.tolist(),
        y_planet = yp.tolist(),
        x_merc   = sol.y[0].tolist(),
        y_merc   = sol.y[1].tolist(),
    )
