# physics_neutron.py
"""
Neutron star structure physics module
Faithful port of Bernard Schutz's Neutron.java (Gravity From the Ground Up),
Creative Commons BY-NC-SA 1.0.

Contains only physical constants and the relativistic hydrostatic equilibrium
equation (TOV-like form used in Schutz’s simplified model).
"""

import math

# Physical constants (SI)
G = 6.672e-11          # Newton's gravitational constant
c2 = 8.98755e16        # speed of light squared

def eos_density(p, K, gamma):
    """Polytropic equation of state: rho = (p/K)^(1/gamma)."""
    return (p / K) ** (1.0 / gamma)

def tov_pressure_step(p, rho, m, r, dr):
    """
    Relativistic hydrostatic equilibrium (Schutz simplified TOV form):

    dp/dr = - G (rho + p/c^2) ( m + 4π r^3 p/c^2 ) / ( r ( r - 2Gm/c^2 ) )
    """
    numerator = G * (rho + p / c2) * (m + 4.0 * math.pi * r**3 / c2)
    denominator = r * (r - 2.0 * G * m / c2)
    return p - numerator * dr / denominator

def mass_step(m, rho, r, dr):
    """dm/dr = 4π r^2 rho."""
    return m + 4.0 * math.pi * r**2 * rho * dr
