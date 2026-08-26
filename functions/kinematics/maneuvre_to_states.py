import numpy as np

#awesim functionalities
from AWEsim.functions.kinematics.DCM import update_dcm, dcm_to_euler

def maneuver_to_states(maneuver, Vw):
    """
    Convert prescribed aerodynamic maneuver inputs into AWEbox-style states.

    Parameters
    ----------
    maneuver : ndarray, shape (N+1, 10)
        Prescribed maneuver data with columns:
            0 : time
            1 : apparent airspeed Va [m/s]
            2 : angle of attack alpha [rad]
            3 : sideslip angle beta [rad]
            4 : roll rate omega_x [rad/s]
            5 : pitch rate omega_y [rad/s]
            6 : yaw rate omega_z [rad/s]
            7 : aileron deflection delta_a [rad]
            8 : elevator deflection delta_e [rad]
            9 : rudder deflection delta_r [rad]

    Vw : float
        Wind speed in the inertial x-direction [m/s].


    Returns
    -------
    states : ndarray, shape (N, 22)
        AWEbox-style state vector:

            [q,
             q_dot,
             R,
             omega,
             delta_dot]

        More specifically:

            0  : time
            1:4  : position q
            4:7  : inertial velocity q_dot
            7:16 : rotation matrix R, COLUMN-MAJOR order (3x3) #TODO: Check if AWEbox uses column-major, for now I assume yes
            16:19: angular velocity omega
            19:22: control-surface rates
    """

    time = maneuver[:, 0]
    dt = time[1] - time[0]
    N = len(time) - 1

    # ------------------------------------------------------------------
    # Allocate state array
    # ------------------------------------------------------------------

    states = np.zeros((N, 22))

    states[:, 0] = time[:-1]

    # Initial orientation: identity matrix
    states[0, 7:16] = np.eye(3).T.reshape(9)

    # ------------------------------------------------------------------
    # Time integration
    # ------------------------------------------------------------------

    for i in range(N):

        # --------------------------------------------------------------
        # Control-surface rates
        # --------------------------------------------------------------

        delta_dot = (
            maneuver[i + 1, 7:10] - maneuver[i, 7:10]
        ) / dt

        # --------------------------------------------------------------
        # Current attitude and angular velocity
        # --------------------------------------------------------------

        omega = maneuver[i, 4:7]

        R = states[i, 7:16].reshape(3, 3).T

        # Integrate attitude
        R_next = update_dcm(R, omega, dt)

        # --------------------------------------------------------------
        # Translational dynamics
        # --------------------------------------------------------------

        Va = maneuver[i, 1]
        alpha = maneuver[i, 2]
        beta = maneuver[i, 3]

        # Apparent velocity expressed in body coordinates
        q_dot_b = Va * np.array([
            -np.cos(alpha) * np.cos(beta),
             np.sin(beta),
            -np.sin(alpha) * np.cos(beta)
        ])

        # Transform to inertial coordinates and add wind
        q_dot = R @ q_dot_b + np.array([Vw, 0.0, 0.0])

        # Integrate position
        q = states[i, 1:4]
        q_next = q + q_dot * dt

        # --------------------------------------------------------------
        # Store current state
        # --------------------------------------------------------------

        states[i, 4:7] = q_dot
        states[i, 16:19] = omega
        states[i, 19:22] = delta_dot

        # --------------------------------------------------------------
        # Store next position and attitude
        # --------------------------------------------------------------

        if i < N - 1:
            states[i + 1, 1:4] = q_next
            states[i + 1, 7:16] = R_next.T.reshape(9)

    return states