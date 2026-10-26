import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# AWEsim
from AWEsim.functions.data_exchange import load_simulation_data
from AWEsim.functions.postprocessing.compute import compute_cfd_coefficients
from AWEsim.functions.aerodynamics.aero_from_SD import compute_sd_coefficients
from AWEsim.functions.postprocessing.plotting import plot_aerodynamic_coefficients

# =============================================================================
# Settings
# =============================================================================

FILE_DIR = Path(__file__).resolve().parent
CASE_DIR = FILE_DIR.parent
SIM_DIR = CASE_DIR / "SIM_rolling_CSD"

# =============================================================================
# Main
# =============================================================================

states, maneuvre, cfd_coeff = load_simulation_data(SIM_DIR)

time, force_coeff, moment_coeff = compute_cfd_coefficients(states, maneuvre, cfd_coeff)

force_coeff_sd, moment_coeff_sd = compute_sd_coefficients(maneuvre,len(time))

# Axis limits estimated from the image
ylims = [
    [(-0.027, 0.157), (-0.080, 0.000)],  # Cx, Cl
    [(-0.016, 0.016), (-0.133, 0.058)],  # Cy, Cm
    [( 0.850, 1.530), (-0.022, 0.003)],  # Cz, Cn
]

plot_aerodynamic_coefficients(time, force_coeff, moment_coeff, force_coeff_sd, moment_coeff_sd,
                              xlim=(0.0, 9.0), ylims=ylims)

