from driver_earthorbit import run_earth_orbit
from plot_earthorbit import plot_earth_orbit

xs, ys, xEarth, yEarth = run_earth_orbit(
    h0=300.0,
    uInit=0.0,
    vInit=7900.0,
    dt=0.4,
    maxSteps=15000
)

plot_earth_orbit(xs, ys, xEarth, yEarth)
