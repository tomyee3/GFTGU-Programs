"""
RelativisticOrbit – main entry point  (Gravity From the Ground Up)
After Bernard F. Schutz, "Gravity From the Ground Up," Cambridge, 2003.

Edit the parameters below to explore different orbits around a solar-mass
black hole.  All quantities are in SI units (metres, seconds).

Physical context
----------------
The simulation integrates the equatorial geodesic of a test particle in
the Schwarzschild spacetime.  The GR correction adds a term  12K²/(c²r²)
to the Newtonian potential, where K = ½ u_init · x_init is the specific
angular momentum constant of the orbit.

Default initial conditions match Schutz's Java program:
  x_init  = 1.0e11 m   starting x-position (particle begins on the x-axis)
  u_init  = 8862 m/s   starting y-velocity  (gives a mildly relativistic orbit)
  dt      = 500 s      initial time-step; the integrator halves this
                       automatically when accuracy demands it
"""

from driver_relativistic_orbit import (
    integrate_relativistic_orbit,
    RelativisticOrbitParams,
)
from plot_relativistic_orbit import plot_relativistic_orbit

# ---------------------------------------------------------------------------
# Parameters – edit these values to explore different orbits
# ---------------------------------------------------------------------------
params = RelativisticOrbitParams(
    x_init     = 1.0e11,    # initial x-position (m);  start on the x-axis
    u_init     = 8862.0,    # initial y-velocity  (m/s); > 0 → counter-clockwise
    dt         = 500.0,     # initial time-step   (s);  halved automatically near
                            #   periapsis or the horizon
    max_steps  = 2_000_000, # safety cap on total integration steps
    max_orbits = 5,         # stop after this many complete orbits
    eps1       = 1.0e-3,    # fractional acceleration change allowed per step;
                            #   decrease for a smoother, slower run
    eps2       = 1.0e-4,    # corrector-loop convergence tolerance
)

# ---------------------------------------------------------------------------
# Run the integrator and plot the result
# ---------------------------------------------------------------------------
result = integrate_relativistic_orbit(params)

if result.fell_into_hole:
    print(f"Particle crossed the Schwarzschild horizon after "
          f"{result.final_step} steps.")
else:
    print(f"Integration complete: {result.n_orbits:.0f} orbit(s) "
          f"in {result.final_step} steps.")

plot_relativistic_orbit(result)
