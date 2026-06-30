import numpy as np


class AtmosphereModel:
    def __init__(
        self,
        planet_name: str,
        g_accel: float,
        mu: float,
        p0: float,
        temperature_pairs,
        output_type: str = "Pressure",
        power: float = 0.5,
    ):
        """
        temperature_pairs: list of (h, T) in meters and kelvin, e.g. [(0, 288), (11000, 216), ...]
        output_type: "Pressure", "Density", or "Temperature"
        """
        self.planet_name = planet_name
        self.g_accel = g_accel
        self.mu = mu
        self.p0 = p0
        self.output_type = output_type
        self.k = 1.38e-23
        self.mp = 1.67e-27

        # Convert temperature_pairs to arrays h, T
        temperature_pairs = sorted(temperature_pairs, key=lambda x: x[0])
        self.h = np.array([p[0] for p in temperature_pairs], dtype=float)
        self.T = np.array([p[1] for p in temperature_pairs], dtype=float)
        self.measurements = len(self.h)

        # Upper-atmosphere power-law constants
        self.reached_top = False
        self.power = power
        self.beta = None

    def get_temp(self, alt: float, p: float) -> float:
        """
        Interpolate temperature between measured points.
        Above highest measurement, use T = beta * p^power.
        """
        # Below or within measured range: linear interpolation in altitude
        if alt <= self.h[-1]:
            # Find interval
            idx = np.searchsorted(self.h, alt)
            if idx == 0:
                return self.T[0]
            if idx >= self.measurements:
                return self.T[-1]
            h0, h1 = self.h[idx - 1], self.h[idx]
            T0, T1 = self.T[idx - 1], self.T[idx]
            frac = (alt - h0) / (h1 - h0)
            return T0 + frac * (T1 - T0)

        # Above highest measurement: set up beta once
        if not self.reached_top:
            # Use last measured point to fix beta: T_last = beta * p_last^power
            T_last = self.T[-1]
            p_last = p  # pressure at first step above top
            self.beta = T_last / (p_last ** self.power)
            self.reached_top = True

        return self.beta * (p ** self.power)

    def integrate(self, max_steps: int = 1000):
        """
        Integrate hydrostatic equilibrium upward until pressure goes to zero.
        Returns altitude, pressure, density, temperature arrays truncated at top.
        """
        q = self.mp * self.mu / self.k
        rho0 = self.p0 * q / self.T[0]
        scale = self.p0 / self.g_accel / rho0
        dh = scale / 200.0

        alt = np.zeros(max_steps)
        p = np.zeros(max_steps)
        rho = np.zeros(max_steps)
        Temp = np.zeros(max_steps)

        alt[0] = 0.0
        p[0] = self.p0
        Temp[0] = self.T[0]
        rho[0] = rho0

        last_step = 0
        self.reached_top = False

        while last_step == 0:
            for j in range(1, max_steps):
                alt[j] = alt[j - 1] + dh
                p[j] = p[j - 1] - self.g_accel * rho[j - 1] * dh

                if p[j] < 0.0:
                    last_step = j
                    break

                Temp[j] = self.get_temp(alt[j], p[j])
                rho[j] = p[j] * q / Temp[j]

            dh *= 2.0  # if not yet reached top, increase step and repeat

        # Truncate arrays at last_step (excluding negative pressure point)
        alt = alt[:last_step]
        p = p[:last_step]
        rho = rho[:last_step]
        Temp = Temp[:last_step]

        return alt, p, rho, Temp

    def compute_output_curve(self):
        """
        Return (altitude, y, y_label) according to outputType.
        """
        alt, p, rho, Temp = self.integrate()
        if self.output_type == "Pressure":
            return alt, p, "Pressure (Pa)"
        elif self.output_type == "Density":
            return alt, rho, "Density (kg/m^3)"
        elif self.output_type == "Temperature":
            return alt, Temp, "Temperature (K)"
        else:
            raise ValueError(f"Unknown outputType: {self.output_type}")
