import numpy as np

from AWEsim.aircraft.megawes.megawes import megawes

# =============================================================================
# Settings 
# TODO: get from simulation input
# TODO: Check if these calculated quantities are not already available in the simulation output
# =============================================================================

RHO = 1.225          # [kg/m³] 

B_REF = megawes["wing_span"]
S_REF = megawes["reference_area"]
C_REF = megawes["reference_chord"]
V_REF = megawes["reference_velocity"]

mass = megawes["mass"]

# Gravity
G = 9.81  # m/s²

# =============================================================================
# CFD force and moment coefficients
# =============================================================================

def compute_cfd_coefficients(states, maneuvre, cfd_coeff):
    """
    Convert Fluent force/moment output to body-frame aerodynamic coefficients.

    Returns
    -------
    time : ndarray, shape (N,)
        Simulation time [s].

    force_coeff : ndarray, shape (N, 3)
        Body-frame force coefficients [Cx, Cy, Cz].

    moment_coeff : ndarray, shape (N, 3)
        Body-frame moment coefficients [Cl, Cm, Cn].
    """

    n_samples = min(len(states), len(maneuvre), len(cfd_coeff))

    # if SKIP_LAST_CFD_SAMPLE:
    #     n_samples = min(n_samples, len(cfd_coeff) - 1)

    time = cfd_coeff[:n_samples, 1]

    force_coeff = np.zeros((n_samples, 3))
    moment_coeff = np.zeros((n_samples, 3))

    # Fluent reference values
    q_ref_fluent = 0.5 * RHO * V_REF**2
    force_scale_fluent = q_ref_fluent * S_REF
    moment_scale_fluent = force_scale_fluent * C_REF

    for i in range(n_samples):

        # Recover dimensional forces and moments from Fluent coefficients
        force_earth = cfd_coeff[i, 2:5] * force_scale_fluent
        moment_earth = cfd_coeff[i, 5:8] * moment_scale_fluent

        # Aircraft state
        position = states[i, 1:4]

        # DCM: body -> earth
        R = states[i, 10:19].reshape(3, 3).T


        # Shift moment reference point
        moment_earth -= np.cross(position, force_earth)

        # Earth -> body
        force_body = R.T @ force_earth
        moment_body = R.T @ moment_earth

        # Aerodynamic coefficients using instantaneous airspeed
        airspeed = maneuvre[i, 1]
        q_dynamic = 0.5 * RHO * airspeed**2

        force_coeff[i] = force_body / (q_dynamic * S_REF)
        moment_coeff[i] = moment_body / (q_dynamic * S_REF * np.array([B_REF, C_REF, B_REF]))

    return time, force_coeff, moment_coeff


def calculate_power(states, forces_cfd):

    #TODO: Can we take this directly from AWEbox output? It is already calculated there.

    tension = calculate_tether_tension(states, forces_cfd)
    reel_speed = np.asarray(states["dl_t"], dtype=float)
    power = tension * reel_speed[:-1]

    return power

def calculate_tether_tension(states, forces_cfd):

    #TODO: Can we take this directly from AWEbox output? It is already calculated there.

    acceleration, sample_time = compute_acceleration(states)
    aerodynamic_force = interpolate_aerodynamic_force(sample_time, forces_cfd)
    tether_force = compute_tether_force(acceleration, aerodynamic_force)

    tension = np.linalg.norm(tether_force, axis=1)

    return tension


def compute_acceleration(states):
    """Compute forward-difference acceleration and sample times.

    Returns (acceleration, sample_time, reel_speed).
    """

    time = np.asarray(states["time"], dtype=float)
    if len(time) < 2 or np.any(np.diff(time) <= 0):
        raise ValueError("State times must contain at least two increasing values")

    velocity = np.column_stack([
        states["dq10_vx"],
        states["dq10_vy"],
        states["dq10_vz"],
    ])

    if len(velocity) != len(time) != len(time):
        raise ValueError("State arrays must have the same length as states['time']")

    # Forward difference: acceleration and power are assigned to time[:-1].
    acceleration = np.diff(velocity, axis=0) / np.diff(time)[:, None]
    sample_time = time[:-1]

    return acceleration, sample_time

def interpolate_aerodynamic_force(sample_time, forces_cfd):
    """Interpolate CFD aerodynamic forces onto sample_time.

    Returns ndarray shape (len(sample_time), 3) with Fx,Fy,Fz.
    """

    time_cfd = np.asarray(forces_cfd["time"], dtype=float)
    if len(time_cfd) < 2 or np.any(np.diff(time_cfd) <= 0):
        raise ValueError("CFD force times must contain at least two increasing values")

    aerodynamic_force = np.column_stack([
        np.interp(sample_time, time_cfd, forces_cfd[name])
        for name in ("Fx", "Fy", "Fz")
    ])

    return aerodynamic_force


def compute_tether_force(acceleration, aerodynamic_force):
    """Compute tether force acting on the aircraft (N).

    Uses mass and gravity (module-level). Returns array shape (N,3).
    """

    weight = np.array([0.0, 0.0, -mass * G])
    tether_force = mass * acceleration - aerodynamic_force - weight
    return tether_force



    """Compute instantaneous tether power given tension and reel speed.

    `tension` has length N; `reel_speed` has length N+1 (state length)
    so `reel_speed[:-1]` is used to align with forward-differenced samples.
    """

    return tension * reel_speed[:-1]