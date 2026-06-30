"""
Binary orbit driver module.

Translated and adapted from Bernard F. Schutz,
Gravity from the Ground Up, Binary.java (CC license).

This module performs the time integration of the
two-body problem using a simple predictor–corrector
scheme and adaptive time-step logic inspired by Schutz.
"""

from dataclasses import dataclass
from typing import List

from physics_binary import BinaryState, accelerations, energies


@dataclass
class BinaryResult:
    times: List[float]
    xA: List[float]
    yA: List[float]
    vA: List[float]
    uA: List[float]
    xB: List[float]
    yB: List[float]
    vB: List[float]
    uB: List[float]
    U: List[float]
    K: List[float]
    E: List[float]


def integrate_binary(
    MA: float,
    MB: float,
    xInitA: float,
    yInitA: float,
    vInitA: float,
    uInitA: float,
    xInitB: float,
    yInitB: float,
    vInitB: float,
    uInitB: float,
    dt: float,
    max_steps: int,
    eps1: float,
    eps2: float,
) -> BinaryResult:
    """
    Integrate the binary orbit using a Schutz-style
    predictor–corrector with adaptive time-step.

    Parameters mirror Binary.java:
        MA, MB      : masses
        xInitA,B    : initial positions
        vInitA,B    : initial velocities (x-components)
        uInitA,B    : initial velocities (y-components)
        dt          : base time-step
        max_steps   : maximum number of steps
        eps1        : time-step accuracy threshold
        eps2        : predictor–corrector accuracy threshold
    """

    # Initial state
    state = BinaryState(
        t=0.0,
        xA=xInitA,
        yA=yInitA,
        vA=vInitA,
        uA=uInitA,
        xB=xInitB,
        yB=yInitB,
        vB=vInitB,
        uB=uInitB,
    )

    dt_work = dt

    times: List[float] = []
    xA_list: List[float] = []
    yA_list: List[float] = []
    vA_list: List[float] = []
    uA_list: List[float] = []
    xB_list: List[float] = []
    yB_list: List[float] = []
    vB_list: List[float] = []
    uB_list: List[float] = []
    U_list: List[float] = []
    K_list: List[float] = []
    E_list: List[float] = []

    for step in range(max_steps):
        # Record current state and energies
        U, K, E = energies(
            MA, MB,
            state.xA, state.yA, state.vA, state.uA,
            state.xB, state.yB, state.vB, state.uB,
        )

        times.append(state.t)
        xA_list.append(state.xA)
        yA_list.append(state.yA)
        vA_list.append(state.vA)
        uA_list.append(state.uA)
        xB_list.append(state.xB)
        yB_list.append(state.yB)
        vB_list.append(state.vB)
        uB_list.append(state.uB)
        U_list.append(U)
        K_list.append(K)
        E_list.append(E)

        # Compute accelerations at current state
        axA, ayA, axB, ayB = accelerations(
            MA, MB,
            state.xA, state.yA,
            state.xB, state.yB,
        )

        # Predictor step: simple Euler
        xA_pred = state.xA + state.vA * dt_work
        yA_pred = state.yA + state.uA * dt_work
        vA_pred = state.vA + axA * dt_work
        uA_pred = state.uA + ayA * dt_work

        xB_pred = state.xB + state.vB * dt_work
        yB_pred = state.yB + state.uB * dt_work
        vB_pred = state.vB + axB * dt_work
        uB_pred = state.uB + ayB * dt_work

        # Accelerations at predicted state
        axA_pred, ayA_pred, axB_pred, ayB_pred = accelerations(
            MA, MB,
            xA_pred, yA_pred,
            xB_pred, yB_pred,
        )

        # Corrector: average accelerations and velocities
        # Iterate until fractional change < eps2
        vA_corr = vA_pred
        uA_corr = uA_pred
        vB_corr = vB_pred
        uB_corr = uB_pred

        for _ in range(10):  # modest iteration cap
            vA_new = state.vA + 0.5 * (axA + axA_pred) * dt_work
            uA_new = state.uA + 0.5 * (ayA + ayA_pred) * dt_work
            vB_new = state.vB + 0.5 * (axB + axB_pred) * dt_work
            uB_new = state.uB + 0.5 * (ayB + ayB_pred) * dt_work

            # Fractional changes
            def frac_change(old, new):
                if old == 0.0:
                    return abs(new)
                return abs((new - old) / old)

            max_change = max(
                frac_change(vA_corr, vA_new),
                frac_change(uA_corr, uA_new),
                frac_change(vB_corr, vB_new),
                frac_change(uB_corr, uB_new),
            )

            vA_corr, uA_corr, vB_corr, uB_corr = vA_new, uA_new, vB_new, uB_new

            if max_change < eps2:
                break

        # Position update using corrected velocities
        xA_new = state.xA + 0.5 * (state.vA + vA_corr) * dt_work
        yA_new = state.yA + 0.5 * (state.uA + uA_corr) * dt_work
        xB_new = state.xB + 0.5 * (state.vB + vB_corr) * dt_work
        yB_new = state.yB + 0.5 * (state.uB + uB_corr) * dt_work

        # Time-step accuracy check (eps1)
        # Use fractional change in accelerations as proxy
        axA_new, ayA_new, axB_new, ayB_new = accelerations(
            MA, MB,
            xA_new, yA_new,
            xB_new, yB_new,
        )

        def frac_change_acc(old, new):
            if old == 0.0:
                return abs(new)
            return abs((new - old) / old)

        max_acc_change = max(
            frac_change_acc(axA, axA_new),
            frac_change_acc(ayA, ayA_new),
            frac_change_acc(axB, axB_new),
            frac_change_acc(ayB, ayB_new),
        )

        if max_acc_change > eps1:
            # Reduce time-step and retry this step
            dt_work *= 0.5
            continue
        else:
            # Accept step; optionally grow dt_work modestly
            dt_work = min(dt_work * 1.1, dt)

        # Commit new state
        state = BinaryState(
            t=state.t + dt_work,
            xA=xA_new,
            yA=yA_new,
            vA=vA_corr,
            uA=uA_corr,
            xB=xB_new,
            yB=yB_new,
            vB=vB_corr,
            uB=uB_corr,
        )

    return BinaryResult(
        times=times,
        xA=xA_list,
        yA=yA_list,
        vA=vA_list,
        uA=uA_list,
        xB=xB_list,
        yB=yB_list,
        vB=vB_list,
        uB=uB_list,
        U=U_list,
        K=K_list,
        E=E_list,
    )
