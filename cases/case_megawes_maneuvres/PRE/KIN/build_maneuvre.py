import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# AWEsim functionalities
from data.megawes.megawes import megawes
from functions.kinematics.DCM import update_dcm, dcm_to_euler
from functions.kinematics.maneuvre_to_states import maneuver_to_states
from functions.kinematics.rigid_body_motion_fluent import rigid_body_motion_fluent

# TODO
# Plot aircraft in 3D trajectory

# File directions
FILE_DIR = Path(__file__).resolve().parent
CASE_DIR = FILE_DIR.parent.parent
SIM_DIR = CASE_DIR / "SIM_0"

# Settings
write_SIM = True  # Write SIM files for Fluent simulation
print_VWE_dim = False

# Reference dimensions aircraft
b = megawes["wing_span"]
c = megawes["reference_chord"]

#
# Functions to build maneuvre
#

# Ramp function to smoothly transition between two values over a specified time interval
def ramp(t, t_start, t_end):
    return np.clip((t - t_start) / (t_end - t_start), 0.0, 1.0)

#
# Define maneuvre
#

# Nominal/starting condition
Vw = 10  # Present wind to stabilize CFD simulation
Va0 = 80  # Apparent wind speed [m/s]
alpha0 = np.deg2rad(5)  # Angle of attack [rad]
beta0 = 0
omega_x0 = np.deg2rad(1e-9)  # Roll rate [rad/s] 10
omega_y0 = np.deg2rad(0)  # Pitch rate [rad/s] 15
omega_z0 = np.deg2rad(0)     # Yaw rate [rad/s]  30  
delta_a0 = 0
delta_e0 = 0
delta_r0 = 0

# Time settings
time_maneuvre = 9  # [s] Should be same as in SIM!
dt = 0.01  # Time step [s] Should be same as in SIM!
N = int(time_maneuvre / dt)
time = np.arange(0, N * dt + dt, dt)

# Maneuvre settings
delta_Va = 30
delta_alpha = np.deg2rad(5)
delta_beta = np.deg2rad(10)
delta_CSD = np.deg2rad(3)
t_m1 = 1
t_m2 = 3.5
t_m3 = 6
dt_m = 2

#
# Build maneuvre matrix
#

maneuvre = np.zeros((N + 1, 10))  # time, Va, alpha, beta, omega_x, omega_y,omega_z, delta_a, delta_e,delta_r

# Fill in nominal condition
maneuvre[:, 0] = time
maneuvre[:, 1] = Va0
maneuvre[:, 2] = alpha0
maneuvre[:, 3] = beta0
maneuvre[:, 4] = omega_x0
maneuvre[:, 5] = omega_y0
maneuvre[:, 6] = omega_z0
maneuvre[:, 7] = delta_a0
maneuvre[:, 8] = delta_e0
maneuvre[:, 9] = delta_r0

# Fill in excitation
maneuvre[:, 4] = omega_x0 + np.deg2rad(40)*ramp(time,0.05,0.5) 
# maneuvre[:, 1] = Va0 + delta_Va*ramp(time,t_ail,t_ail+0.1) -2*delta_Va*ramp(time,t_ail+0.3,t_ail+0.5) + delta_Va*ramp(time,t_ail+0.7,t_ail+0.8)
# maneuvre[:, 2] = alpha0 + delta_alpha*ramp(time,t_ele,t_ele+0.1) -2*delta_alpha*ramp(time,t_ele+0.3,t_ele+0.5) + delta_alpha*ramp(time,t_ele+0.7,t_ele+0.8)
# maneuvre[:, 3] = beta0 + delta_beta*ramp(time,t_rud,t_rud+0.1) -2*delta_beta*ramp(time,t_rud+0.3,t_rud+0.5) + delta_beta*ramp(time,t_rud+0.7,t_rud+0.8)
#maneuvre[:, 4] = omega_x0 + delta*ramp(time,t_ail,t_ail+0.1) -2*delta*ramp(time,t_ail+0.3,t_ail+0.5) + delta*ramp(time,t_ail+0.7,t_ail+0.8)
#maneuvre[:, 5] = omega_y0 + delta*ramp(time,t_ele,t_ele+0.1) -2*delta*ramp(time,t_ele+0.3,t_ele+0.5) + delta*ramp(time,t_ele+0.7,t_ele+0.8)
#maneuvre[:, 6] = omega_z0 + delta*ramp(time,t_rud,t_rud+0.1) -2*delta*ramp(time,t_rud+0.3,t_rud+0.5) + delta*ramp(time,t_rud+0.7,t_rud+0.8)
maneuvre[:, 7] = delta_a0 + delta_CSD*ramp(time,t_m1,t_m1+1/8*dt_m) -2*delta_CSD*ramp(time,t_m1+3/8*dt_m,t_m1+5/8*dt_m) + delta_CSD*ramp(time,t_m1+7/8*dt_m,t_m1+dt_m)
maneuvre[:, 8] = delta_e0 + delta_CSD*ramp(time,t_m2,t_m2+1/8*dt_m) -2*delta_CSD*ramp(time,t_m2+3/8*dt_m,t_m2+5/8*dt_m) + delta_CSD*ramp(time,t_m2+7/8*dt_m,t_m2+dt_m)
maneuvre[:, 9] = delta_r0 + delta_CSD*ramp(time,t_m3,t_m3+1/8*dt_m) -2*delta_CSD*ramp(time,t_m3+3/8*dt_m,t_m3+5/8*dt_m) + delta_CSD*ramp(time,t_m3+7/8*dt_m,t_m3+dt_m)

#
# Build states matrix
#

states = maneuver_to_states(maneuvre, Vw)  # time, q (3), q_dot(3), R(9), omega(3), delta(3); TODO Use same definition as AWEbox!

#
# Plot maneuvre and states
#
# TODO: Make general function to plot maneuvre and states, and call it from here and from POST/plot_maneuvre.py

#   Plot traject
plt.close('all')
q = np.array([states[:, 1], states[:, 2], states[:, 3]])

# Create figure
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Plot
ax.plot(q[0][0], q[1][0], q[2][0], '*')
ax.plot(q[0], q[1], q[2])

# Labels
ax.set_box_aspect([1, 1, 1])  # equal scaling for x, y, z axes
w = Va0 * time_maneuvre
ax.set_xlim(-w, 0)
ax.set_ylim(-w / 2, w / 2)
ax.set_zlim(-w / 2, w / 2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

#  Plot maneuvre
fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

# ==============================================================
# (1) Airspeed + aerodynamic angles
# ==============================================================
ax1 = axs[0]
ax1b = ax1.twinx()

l1 = ax1.plot(maneuvre[:, 0], maneuvre[:, 1], lw=2, label=r'$V_a$', color='tab:blue')
l2 = ax1b.plot(maneuvre[:, 0], np.rad2deg(maneuvre[:, 2]), lw=2, label=r'$\alpha$', color='tab:orange')
l3 = ax1b.plot(maneuvre[:, 0], np.rad2deg(maneuvre[:, 3]), lw=2, label=r'$\beta$', color='tab:green')

ax1.set_ylabel(r'$V_a$ [m/s]', color='tab:blue')
ax1b.set_ylabel('Angle [deg]')
ax1.grid(True)

lines = l1 + l2 + l3
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='best')

# ==============================================================
# (2) Control surface deflections
# ==============================================================
axs[1].plot(maneuvre[:, 0], np.rad2deg(maneuvre[:, 7]), lw=2, label=r'$\delta_a$')
axs[1].plot(maneuvre[:, 0], np.rad2deg(maneuvre[:, 8]), lw=2, label=r'$\delta_e$')
axs[1].plot(maneuvre[:, 0], np.rad2deg(maneuvre[:, 9]), lw=2, label=r'$\delta_r$')

axs[1].set_ylabel('Deflection [deg]')
axs[1].grid(True)
axs[1].legend(loc='best')

# ==============================================================
# (3) Angular rates
# ==============================================================
axs[2].plot(maneuvre[:, 0], np.rad2deg(maneuvre[:, 4]), lw=2, label=r'$\omega_x$')
axs[2].plot(maneuvre[:, 0], np.rad2deg(maneuvre[:, 5]), lw=2, label=r'$\omega_y$')
axs[2].plot(maneuvre[:, 0], np.rad2deg(maneuvre[:, 6]), lw=2, label=r'$\omega_z$')

axs[2].set_ylabel('Rate [deg/s]')
axs[2].set_xlabel('Time [s]')
axs[2].grid(True)
axs[2].legend(loc='best')

plt.tight_layout()

#  Plot euler angles
phi = np.array([])
theta = np.array([])
psi = np.array([])

for i in range(len(states[:, 7])):
    R = states[i, 7:16].reshape(3, 3).T
    phi_i, theta_i, psi_i = dcm_to_euler(R)

    phi = np.append(phi, phi_i)
    theta = np.append(theta, theta_i)
    psi = np.append(psi, psi_i)

fig, ax = plt.subplots(3, 1, figsize=(10, 7), sharex=True)

ax[0].plot(states[:, 0], np.rad2deg(phi), label=r'$\phi$')
ax[0].set_ylabel(r'Roll $\phi$ [deg]')
ax[0].grid()
ax[0].legend()

ax[1].plot(states[:, 0], np.rad2deg(theta), label=r'$\theta$')
ax[1].set_ylabel(r'Pitch $\theta$ [deg]')
ax[1].grid()
ax[1].legend()

ax[2].plot(states[:, 0], np.rad2deg(psi), label=r'$\psi$')
ax[2].set_ylabel(r'Yaw $\psi$ [deg]')
ax[2].set_xlabel('Time [s]')
ax[2].grid()
ax[2].legend()

plt.tight_layout()
plt.show()

#
# Write required inputs to SIM directory
#

if write_SIM:
    CFD_DIR = SIM_DIR / "CFD"
    #Check if SIM directory contains no existing files, and if so, create them
    if not (SIM_DIR / "states.out").exists() and not (CFD_DIR / "move_zone_wing_update_timestep1.dat").exists():
        for i in np.arange(len(states[:, 0])):
            time_step = i
            
            # Fluent inputs
            # TODO: make consistent states format, and provide directly to rigid_body_motion_fluent function, instead of unpacking here
            q = np.array([states[i, 1], states[i, 2], states[i, 3]]).flatten()
            dq = np.array([states[i, 4], states[i, 5], states[i, 6]]).flatten()
            omega = np.array([states[i, 16], states[i, 17], states[i, 18]]).flatten()  # rad or deg?
            R = states[i, 7:16].reshape(3, 3).T
            ddelta = np.array([states[i, 19], states[i, 20], states[i, 21]]).flatten()
            rigid_body_motion_fluent(CFD_DIR,time_step, q, dq,  R, omega, ddelta) #TODO: use states as input, instead of unpacking here

            # States for POST-processing TODO: There is probably a more elegant way to write this to file, but this works for now
            f = open(SIM_DIR / "states.out", "a")
            f.write(str(time_step * dt) + ", "
                    + str(q[0]) + ", " + str(q[1]) + ", " + str(q[2]) + ", "  # q 
                    + str(dq[0]) + ", " + str(dq[1]) + ", " + str(dq[2]) + ", "  # dq 
                    + str(omega[0]) + ", " + str(omega[1]) + ", " + str(omega[2]) + ", "  # omega 
                    + str(R[0, 0]) + ", " + str(R[1, 0]) + ", " + str(R[2, 0]) + ", "  # R e1
                    + str(R[0, 1]) + ", " + str(R[1, 1]) + ", " + str(R[2, 1]) + ", "  # R e2
                    + str(R[0, 2]) + ", " + str(R[1, 2]) + ", " + str(R[2, 2]) + ", "  # R e3
                    + "\n")
            f.close()

            # Maneuvres for POST-processing
            f = open(SIM_DIR / "maneuvres.out", "a")
            f.write( str(maneuvre[i, 0] ) + ", " + str(maneuvre[i, 1] ) + ", " + str(maneuvre[i, 2] ) + ", "  
                    + str(maneuvre[i, 3] ) + ", " + str(maneuvre[i, 4] ) + ", " + str(maneuvre[i, 5] ) + ", "  
                    + str(maneuvre[i, 6] ) + ", " + str(maneuvre[i, 7] ) + ", " + str(maneuvre[i, 8] ) + ", " 
                    + str(maneuvre[i, 9] )
                    + "\n")
            f.close()
        
        print("SIM files written")   
    
    else:
        print("SIM files already exist. Please delete them before running this script to avoid overwriting.")

#
# Print required VWE domain size
#

if print_VWE_dim:
    VWE_margin = b / 2 + 15 * c

    x_min = min(q[0]) - VWE_margin
    x_max = max(q[0]) + VWE_margin
    y_min = min(q[1]) - VWE_margin
    y_max = max(q[1]) + VWE_margin
    z_min = min(q[2]) - VWE_margin
    z_max = max(q[2]) + VWE_margin

    print('Required VWE domain:')
    print('xmin: ', x_min)
    print('xmax: ', x_max)
    print('ymin: ', y_min)
    print('ymax: ', y_max)
    print('zmin: ', z_min)
    print('zmin: ', z_max)

