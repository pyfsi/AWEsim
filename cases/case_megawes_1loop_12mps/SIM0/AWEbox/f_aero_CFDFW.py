#!/usr/bin/python3
"""
External aerodynamic forces from FLUENT
:authors: Niels Pynaert
:date: 31/01/2024

INPUT:
- x: states
- u: controls

OUTPUT:
- F_ext  (external force in inertial frame)
- M_ext (external moment in body-fixed frame)

"""

import numpy as np
import casadi as ca
from rigid_body_motion_fluent import rigid_body_motion_fluent
import time
from convert_files import convert_files
import json

# Load the JSON file
with open("../parameters.json", "r") as file:
    data = json.load(file)

# Extract values from the "settings" section
#N_steps = data["settings"]["number_of_timesteps"]
#dt = data["settings"]["delta_t"]
start_from_timestep = data["settings"]["timestep_start"]
#restart_save_step  = data["settings"]["save_restart"]

def update_dcm(R, omega, dt): #source: ChatGPT TODO: test expicitely (am I not updating the inverse?)
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

def F_aero_CFDFW(x,u,time_step):
    # print("current time_step:" + str(time_step))
    # 1. Send states/controls to fluent with rigid_body_motion_fluent.py
    if time_step > 0:
        q10 = np.array([x[0], x[1], x[2]]).flatten()
        dq10 = np.array([x[3], x[4], x[5]]).flatten()
        omega10 = np.array([x[6], x[7], x[8]]).flatten()  # rad or deg?
        r10 = np.array([[x[9], x[10], x[11]], [x[12], x[13], x[14]], [x[15], x[16], x[17]]]).reshape(3, 3)  # CHECK
        delta10 = np.array([x[18], x[19], x[20]]).flatten()
        ddelta10 = np.array([u[6], u[7], u[8]]).flatten()

    else:  # Timestep 0: ADAPT TO CASE! #TODO: not hardcoded; divergeert met non-hardcoded IC?
        q10 = np.array([513.38555833148, 4.93462364092737, 353.2429941775]).flatten()
        dq10 = np.array([1.24587640682482, -44.9508805361432, -1.18275216178422]).flatten()
        omega10 = np.array([0.11144075488565, 0.070175387757908, 0.310001456349632]).flatten()
        r10 = np.array([[0.224405358721682, 0.971127008661446, -0.080960286935378],
                        [-0.34857229047486, 0.157573682131974, 0.923941498778012],
                        [0.91002175445493, -0.179116911118311, 0.373868344286924]]).reshape(3, 3)
        delta10 = np.array([-0.083812489134005, -0.028522705746199, 0.130899693899575]).flatten()
        ddelta10 = np.array([-0.004611638362343, -0.004829888436948, 5.86607862020155E-10]).flatten()

    rigid_body_motion_fluent(time_step, q10, dq10, np.transpose(r10), omega10, ddelta10)

    # 3. Wait for new timestep in force_coefficients.out
    new_timestep = False
    file_check1 = False
    F_ext = 0
    M_ext = 0

    while not new_timestep:
        #Check first if there is not already a force_coefficient file, if so delete
        if time_step == start_from_timestep and not file_check1:
            try:
                convert_files(time_step)
                data = np.genfromtxt('../CFD/force_coefficients2.out', skip_header=3)
                print("AWEbox: WARNING: force_coefficients.out not deleted")
                # TODO: delete force_coefficients
            except:
                file_check1 = True
        # Check if there is a new force_coefficient file and a TS1
        elif time_step == start_from_timestep:
            try: #TODO: avoid try, make a function to process forces
                convert_files(time_step)
                data = np.genfromtxt('../CFD/force_coefficients2.out', skip_header=3)
                time_step_list = data[:, 0]
                new_timestep = True
                #rigid_body_motion_fluent(time_step, q10, dq10, r10, omega10, ddelta10) #Can this be deleted?

                K = 0.5 * 1.225 * 80 ** 2 * 150.45  # 0.5*rho*v^2*S #reference values from fluent
                Km = 0.5 * 1.225 * 80 ** 2 * 150.45 * 3.5425  # 0.5*rho*v^2*S*c

                data = np.genfromtxt('../CFD/force_coefficients2.out', skip_header=3)
                Fx = data[-1, 2] * K
                Fy = data[-1, 3] * K
                Fz = data[-1, 4] * K
                Mx = data[-1, 5] * Km  # inertial frame --> convert to body-frame
                My = data[-1, 6] * Km
                Mz = data[-1, 7] * Km

                F = np.array([Fx, Fy, Fz])
                M = np.array([Mx, My, Mz])
                
                q10_fl = np.array([q10[0] + dq10[0]*0.005,q10[1] + dq10[1]*0.005,q10[2] + dq10[2]*0.005]).flatten() #TS HARDCODED
                r10_fl = update_dcm(r10, omega10, 0.005)

                M = M - np.cross(q10_fl, F)
                M_b = np.matmul(r10_fl,M) #earth to body

                F_ext = ca.DM([Fx, Fy, Fz])
                M_ext = ca.DM([M_b[0], M_b[1], M_b[2]])

            except:
                donothing = 0
        else:
            try:
                convert_files(time_step)
            except:
                donothing = 0
            data = np.genfromtxt('../CFD/force_coefficients2.out', skip_header=3)
            time_step_list = data[:, 0]
            #check for new time step
            if time_step_list[-1] > time_step: #Mismatch timestep?
                new_timestep = True
                K = 0.5 * 1.225 * 80 ** 2 * 150.45  # 0.5*rho*v^2*S #reference values from fluent
                Km = 0.5 * 1.225 * 80 ** 2 * 150.45 * 3.5425  # 0.5*rho*v^2*S*c
                
                data = np.genfromtxt('../CFD/force_coefficients2.out', skip_header=3)
                Fx = data[-1, 2] * K
                Fy = data[-1, 3] * K
                Fz = data[-1, 4] * K
                Mx = data[-1, 5] * Km  # inertial frame --> convert to body-frame
                My = data[-1, 6] * Km
                Mz = data[-1, 7] * Km

                F = np.array([Fx, Fy, Fz])
                M = np.array([Mx, My, Mz])
                
                q10_fl = np.array([q10[0] + dq10[0]*0.005,q10[1] + dq10[1]*0.005,q10[2] + dq10[2]*0.005]).flatten() #TS HARDCODED
                r10_fl = update_dcm(r10, omega10, 0.005) #TS HARDCODED

                M = M - np.cross(q10_fl, F)
                M_b = np.matmul(r10_fl,M) #earth to body

                F_ext = ca.DM([Fx, Fy, Fz])
                M_ext = ca.DM([M_b[0], M_b[1], M_b[2]])

    return  {'F_ext': F_ext, 'M_ext': M_ext}
