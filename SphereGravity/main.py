from driver_spheregravity import run_spheregravity
from plot_spheregravity import plot_spheregravity

radius, accel = run_spheregravity(nDiv=500, outputType="relative difference")
plot_spheregravity(radius, accel, outputType="relative difference")
