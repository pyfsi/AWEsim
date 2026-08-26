import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

#awesim functionalities
from AWEsim.aircraft.megawes.megawes import megawes
from AWEsim.functions.aerodynamics.aero_from_SD import force_coefficients_from_states, moment_coefficients_from_states 

# File directions
FILE_DIR = Path(__file__).resolve().parent
CASE_DIR = FILE_DIR.parent
SIM_DIR = CASE_DIR / "SIM_rolling_CSD_test2"

C = 0 # = 1 if completed, 0 is not completed. TODO:fix

# Reference dimensions aircraft
b = megawes["wing_span"]
c = megawes["reference_chord"]

#
# Import data and convert to force and moment coefficients
#

states = np.genfromtxt(SIM_DIR / "states.out", delimiter=',')
maneuvre = np.genfromtxt(SIM_DIR / "maneuvres.out", delimiter=',') 
CFD_coeff = np.genfromtxt(SIM_DIR / "CFD" / "force_coefficients.out", skip_header=3)  

K = 0.5 * 1.225 * 80 ** 2 * 150.45  # 0.5*rho*v^2*S #reference values from fluent (TODO get from megawes.py)
Km = 0.5 * 1.225 * 80 ** 2 * 150.45 * 3.5425  # 0.5*rho*v^2*S*c

timesteps =  CFD_coeff[:, 0]
time =  CFD_coeff[:, 1]

Cx = np.array([])
Cy = np.array([])
Cz = np.array([])
Cl = np.array([])
Cm = np.array([])
Cn = np.array([])

Cx_SD = np.array([])
Cy_SD = np.array([])
Cz_SD = np.array([])
Cl_SD = np.array([])
Cm_SD = np.array([])
Cn_SD = np.array([])

for i in np.arange(len(CFD_coeff[:, 0])):
    Fx =  CFD_coeff[i, 2] * K
    Fy =  CFD_coeff[i, 3] * K
    Fz =  CFD_coeff[i, 4] * K
    Mx =  CFD_coeff[i, 5] * Km  # inertial frame --> convert to body-frame
    My =  CFD_coeff[i, 6] * Km
    Mz =  CFD_coeff[i, 7] * Km

    F = np.array([Fx, Fy, Fz])
    M = np.array([Mx, My, Mz])

    q = np.array([states[i, 1], states[i, 2], states[i, 3]]).flatten()
    R = states[i, 10:19].reshape(3, 3).T

    M = M - np.cross(q, F)
    M_b = np.matmul(R.T, M)  # earth to body 
    F_b = np.matmul(R.T, F)  # earth to body

    Va = maneuvre[i, 1]

    Cl_i = M_b[0] / (0.5 * 1.225 * Va ** 2 * 150.45 * b)
    Cm_i = M_b[1] / (0.5 * 1.225 * Va ** 2 * 150.45 * c)
    Cn_i = M_b[2] / (0.5 * 1.225 * Va ** 2 * 150.45 * b)

    Cx_i = F_b[0] / (0.5 * 1.225 * Va ** 2 * 150.45)
    Cy_i = F_b[1] / (0.5 * 1.225 * Va ** 2 * 150.45)
    Cz_i = F_b[2] / (0.5 * 1.225 * Va ** 2 * 150.45)

    Cx = np.append(Cx, Cx_i)
    Cy = np.append(Cy, Cy_i)
    Cz = np.append(Cz, Cz_i)
    Cl = np.append(Cl, Cl_i)
    Cm = np.append(Cm, Cm_i)
    Cn = np.append(Cn, Cn_i)

    # Reconstructed forces and moments from SD
    Cf_tot, Cf_angles, Cf_rot, Cf_CS, Cf_alpha, Cf_beta, Cf_p, Cf_q, Cf_r, Cf_CSda, Cf_CSde, Cf_CSdr = force_coefficients_from_states(
        maneuvre[:, 1][i], maneuvre[:, 2][i], maneuvre[:, 3][i], maneuvre[:, 4][i], maneuvre[:, 5][i],
        maneuvre[:, 6][i], maneuvre[:, 7][i], maneuvre[:, 8][i], maneuvre[:, 9][i])
    Cm_tot, Cm_angles, Cm_rot, Cm_CS, Cm_alpha, Cm_beta, Cm_p, Cm_q, Cm_r, Cm_CSda, Cm_CSde, Cm_CSdr = moment_coefficients_from_states(
        maneuvre[:, 1][i], maneuvre[:, 2][i], maneuvre[:, 3][i], maneuvre[:, 4][i], maneuvre[:, 5][i],
        maneuvre[:, 6][i], maneuvre[:, 7][i], maneuvre[:, 8][i], maneuvre[:, 9][i])

    Cx_SD = np.append(Cx_SD, Cf_tot[0])
    Cy_SD = np.append(Cy_SD, Cf_tot[1])
    Cz_SD = np.append(Cz_SD, Cf_tot[2])
    Cl_SD = np.append(Cl_SD, Cm_tot[0])
    Cm_SD = np.append(Cm_SD, Cm_tot[1])
    Cn_SD = np.append(Cn_SD, Cm_tot[2])

#
# Plot Reconstructed force and moment coefficients
#

# Create a 3x2 figure
fig, axs = plt.subplots(3, 2, figsize=(10, 8), sharex=True)

# Force coefficients
axs[0, 0].plot(time[C:], Cx)
axs[0, 0].plot(time[C:], Cx_SD)
axs[0, 0].set_ylabel(r'$C_x$')
axs[0, 0].grid(True)

axs[1, 0].plot(time[C:], Cy)
axs[1, 0].plot(time[C:], Cy_SD)
axs[1, 0].set_ylabel(r'$C_y$')
axs[1, 0].set_ylim([-0.1, 0.1])
axs[1, 0].grid(True)

axs[2, 0].plot(time[C:], Cz)
axs[2, 0].plot(time[C:], Cz_SD)
axs[2, 0].set_ylabel(r'$C_z$')
axs[2, 0].set_xlabel('Time [s]')
axs[2, 0].grid(True)

# Moment coefficients
axs[0, 1].plot(time[C:], Cl)
axs[0, 1].plot(time[C:], Cl_SD)
axs[0, 1].set_ylabel(r'$C_l$')
axs[0, 1].set_ylim([-0.04, 0.04])
axs[0, 1].grid(True)

axs[1, 1].plot(time[C:], Cm)
axs[1, 1].plot(time[C:], Cm_SD)
axs[1, 1].set_ylabel(r'$C_m$')
# axs[1, 1].set_ylim([-0.1,0.1])
axs[1, 1].grid(True)

axs[2, 1].plot(time[C:], Cn)
axs[2, 1].plot(time[C:], Cn_SD)
axs[2, 1].set_ylabel(r'$C_n$')
axs[2, 1].set_xlabel('Time [s]')
axs[2, 1].set_ylim([-0.02, 0.02])
axs[2, 1].grid(True)

plt.tight_layout()

plt.show()

