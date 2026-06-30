# main.py
"""
Main entry point for Neutron star model.
User may edit gamma, pC, K, and output_type.
"""

from driver_neutron import compute_neutron_star
from plot_neutron import plot_neutron

if __name__ == "__main__":

    # Example values (user may overwrite)
    gamma = 5.0 / 3.0
    pC = 1e34            # central pressure (Pa)
    K = 1e-15            # polytropic constant (SI)
    output_type = "Pressure"   # "Pressure", "Density", or "Mass"

    data = compute_neutron_star(gamma, pC, K)
    plot_neutron(data, output_type)
