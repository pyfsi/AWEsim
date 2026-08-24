"""
Kinematic functionality for rigid body motion of a vehicle in 3D space.
This module provides functions to update the Direction Cosine Matrix (DCM) based on angular velocity and time step, as well as to convert a DCM to Euler angles.

CAUTION: AI generated functions
"""

import numpy as np

#TODO: function not used, built general function for states
def dcm_to_state(R, state):
    """
    Store a 3x3 DCM in the state vector.

    State convention:
        [e1_x, e1_y, e1_z,
         e2_x, e2_y, e2_z,
         e3_x, e3_y, e3_z]
    """
    state[7:16] = R.T.reshape(9)
    return state

def update_dcm(R, omega, dt):      
    """
    Omega is the angular velocity vector in the body frame, and R is the current direction cosine matrix (DCM) representing the orientation of the body frame relative to the inertial frame.
    The function updates the DCM using the angular velocity and time step, ensuring that the resulting DCM remains a valid rotation matrix by re-orthogonalizing it after the update.
    This approach is numerically more stable than directly integrating the DCM using the angular velocity, which can lead to a loss of orthogonality and inaccuracies in the representation of the rotation.
    The update is performed using the explicit Euler method, followed by re-orthogonalization of the DCM using Singular Value Decomposition (SVD) to maintain its properties as a rotation matrix.
    
    Note: Direct integration of the DCM using angular velocity can lead to numerical instability and loss of orthogonality, which can result in an invalid rotation matrix. This is because the DCM must always satisfy the orthogonality condition (R^T * R = I) and the determinant condition (det(R) = 1) to represent a valid rotation. When integrating the DCM directly, small numerical errors can accumulate over time, causing the DCM to deviate from these conditions. This can lead to incorrect orientation representation and potential issues in subsequent calculations that rely on the DCM. To mitigate this, it is recommended to use alternative methods for updating the DCM, such as Rodrigues' rotation formula or the matrix exponential of the skew-symmetric angular-rate matrix, which are more robust and maintain the orthogonality of the DCM. These methods provide a more accurate and stable way to update the orientation of the body frame based on angular velocity, ensuring that the resulting DCM remains a valid rotation matrix.   
    """
        
    # Construct the skew-symmetric matrix Omega from the angular velocity vector omega
    Omega = np.array([
        [0, -omega[2], omega[1]],
        [omega[2], 0, -omega[0]],
        [-omega[1], omega[0], 0]
    ])

    # Calculate the derivative of the DCM
    R_dot = R @ Omega

    # Update R using the explicit Euler method
    R_next = R + R_dot * dt

    # Re-orthogonalize R to maintain it as a rotation matrix
    U, _, Vt = np.linalg.svd(R_next)
    R_next = U @ Vt

    return R_next


def dcm_to_euler(R):
    """
    Convert a Direction Cosine Matrix (DCM) to Euler angles.

    Convention:
        ZYX rotation sequence:
            yaw   = psi
            pitch = theta
            roll  = phi

    Parameters
    ----------
    R : np.ndarray, shape (3, 3)
        DCM transforming vectors from body frame to inertial frame.

    Returns
    -------
    phi : float
        Roll angle [rad]
    theta : float
        Pitch angle [rad]
    psi : float
        Yaw angle [rad]
    """

    # Numerical protection against values slightly outside [-1, 1]
    r20 = np.clip(R[2, 0], -1.0, 1.0)

    theta = -np.arcsin(r20)

    phi = np.arctan2(R[2, 1], R[2, 2])

    psi = np.arctan2(R[1, 0], R[0, 0])

    return phi, theta, psi