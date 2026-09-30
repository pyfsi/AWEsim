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


# =============================================================================
# Aerodynamics
# =============================================================================


def calculate_aerodynamic_properties(
    states,
    *,
    area=150.45,
    span=42.47,
    dynamic_viscosity=1.81e-5,
    friction_velocity=0.3828883453000257,
    kappa=0.4187,
    roughness=0.0002,
):
    """Return airspeed, Reynolds number, alpha, beta, and supporting arrays.

    Assumes the DCM rows map earth-frame vectors into the body frame.
    Alpha and beta use the same Vz/Vx and Vy/Vx sign convention as the
    original script, with atan replacing the small-angle approximation.
    """
    time = np.asarray(states["time"], dtype=float)
    n = len(time)

    def get_state(name):
        values = np.asarray(states[name], dtype=float)
        if values.shape != (n,):
            raise ValueError(f"states[{name!r}] must contain {n} values")
        return values

    altitude = get_state("q10_z")
    if np.any(altitude + roughness <= 0):
        raise ValueError("Altitude is outside the logarithmic wind profile")

    rotation = np.stack(
        [get_state(f"r10_{i}") for i in range(1, 10)], axis=1
    ).reshape(n, 3, 3)

    velocity_earth = np.column_stack([
        get_state("dq10_vx"),
        get_state("dq10_vy"),
        get_state("dq10_vz"),
    ])

    wind_speed = (
        friction_velocity / kappa
        * np.log((altitude + roughness) / roughness)
    )
    air_velocity_earth = velocity_earth.copy()
    air_velocity_earth[:, 0] -= wind_speed
    air_velocity_body = np.einsum(
        "nij,nj->ni", rotation, air_velocity_earth
    )

    airspeed = np.linalg.norm(air_velocity_body, axis=1)
    if np.any(airspeed <= 0):
        raise ValueError("Airspeed must be greater than zero")

    vx, vy, vz = air_velocity_body.T

    # Principal angles: equivalent to arctan(Vz/Vx) and arctan(Vy/Vx),
    # including when Vx is negative.
    alpha = np.degrees(np.arctan2(vz * np.sign(vx), np.abs(vx)))
    beta = np.degrees(np.arctan2(vy * np.sign(vx), np.abs(vx)))

    chord = area / span
    reynolds = 1.225 * airspeed * chord / dynamic_viscosity #TODO: hardcoded density

    return {
        "time": time,
        "Va": airspeed,               # m/s
        "Re": reynolds,               # based on area / span
        "alpha": alpha,               # degrees
        "beta": beta,                 # degrees
        "chord": chord,               # m
        "rotation": rotation,         # earth -> body
        "air_velocity_body": air_velocity_body,
    }


def calculate_body_coefficients(
    reference,
    states,
    forces,
    *,
    properties=None,
    area=150.45,
    span=42.47,
):
    """Return body-frame force and moment coefficients for one force dataset."""
    if properties is None:
        properties = calculate_aerodynamic_properties(
            reference, states, area=area, span=span
        )

    time = properties["time"]
    force_time = np.asarray(forces["time"], dtype=float)
    if time[0] < force_time[0] or time[-1] > force_time[-1]:
        raise ValueError("Force data do not cover all state timestamps")

    def interpolate_vectors(names):
        return np.column_stack([
            np.interp(time, force_time, np.asarray(forces[name], dtype=float))
            for name in names
        ])

    rotation = properties["rotation"]
    force_earth = interpolate_vectors(("Fx", "Fy", "Fz"))
    force_body = np.einsum(
        "nij,nj->ni", rotation,
        force_earth,
    )

    # Moments are already expressed in the body frame in the force data.
    moment_body = interpolate_vectors(("Mx", "My", "Mz"))

    denominator = 0.5 * 1.225 * properties["Va"]**2 * area #TODO: hardcoded density 
    cx, cy, cz = (force_body / denominator[:, None]).T
    cmx, cmy, cmz = (
        moment_body
        / (denominator[:, None] * np.array([
            span, properties["chord"], span
        ]))
    ).T

    return {
        "time": time,
        "Cx": cx, "Cy": cy, "Cz": cz,
        "Cmx": cmx, "Cmy": cmy, "Cmz": cmz,
        "force_body": force_body,
        "moment_body": moment_body,
    }


def calculate_lift_drag_coefficients(
    reference,
    states,
    forces,
    *,
    properties=None,
    body_coefficients=None,
    area=150.45,
    span=42.47,
):
    """Return drag, side-force, and lift coefficients in wind axes."""
    if properties is None:
        properties = calculate_aerodynamic_properties(
            reference, states, area=area, span=span
        )
    if body_coefficients is None:
        body_coefficients = calculate_body_coefficients(
            reference, states, forces,
            properties=properties, area=area, span=span,
        )

    # Drag points opposite the aircraft velocity relative to the air.
    velocity_direction = (
        properties["air_velocity_body"] / properties["Va"][:, None]
    )
    drag_direction = -velocity_direction

    # Choose lift as the direction closest to positive body z while
    # perpendicular to the relative velocity.
    body_up = np.array([0.0, 0.0, 1.0])
    lift_direction = (
        body_up
        - np.sum(body_up * velocity_direction, axis=1)[:, None]
        * velocity_direction
    )
    lift_norm = np.linalg.norm(lift_direction, axis=1)
    if np.any(lift_norm < 1e-12):
        raise ValueError("Lift direction is undefined for vertical flight")
    lift_direction /= lift_norm[:, None]

    # Complete the orthogonal wind-axis basis.
    side_direction = np.cross(lift_direction, drag_direction)

    force_body = body_coefficients["force_body"]
    denominator = 0.5 * 1.225 * properties["Va"]**2 * area #TODO: hardcoded density

    return {
        "time": properties["time"],
        "CD": np.sum(force_body * drag_direction, axis=1) / denominator,
        "CY": np.sum(force_body * side_direction, axis=1) / denominator,
        "CL": np.sum(force_body * lift_direction, axis=1) / denominator,
    }

def calculate_reference_body_coefficients(reference, *, area=150.45, span=42.47):
    """Calculate reference force and moment coefficients in body axes."""
    time = np.asarray(reference["time"], dtype=float)
    airspeed = np.asarray(
        reference["outputs_aerodynamics_airspeed1_0"], dtype=float
    )
    density = np.mean(
        np.asarray(reference["outputs_aerodynamics_air_density1_0"], dtype=float)
    )

    q_area = 0.5 * density * airspeed**2 * area
    if np.any(q_area == 0):
        raise ValueError("Reference coefficients are undefined at zero airspeed")

    chord = area / span
    result = {"time": time}

    for i, axis in enumerate("xyz"):
        force = np.asarray(
            reference[f"outputs_aerodynamics_f_aero_body1_{i}"],
            dtype=float,
        )
        moment = np.asarray(
            reference[f"outputs_aerodynamics_m_aero_body1_{i}"],
            dtype=float,
        )
        moment_length = chord if axis == "y" else span

        result[f"C{axis}"] = force / q_area
        result[f"Cm{axis}"] = moment / (q_area * moment_length)

    return result