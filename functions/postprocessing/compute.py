import numpy as np

from AWEsim.aircraft.megawes.megawes import megawes

# =============================================================================
# Settings TODO: get from simulation input
# =============================================================================

RHO = 1.225          # [kg/m³] 

B_REF = megawes["wing_span"]
S_REF = megawes["reference_area"]
C_REF = megawes["reference_chord"]
V_REF = megawes["reference_velocity"]

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
