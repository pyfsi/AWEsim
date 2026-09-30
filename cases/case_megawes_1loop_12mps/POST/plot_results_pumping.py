import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# AWEsim
from AWEsim.functions.data_exchange import load_simulation_data, load_simulation_data_pumping
from AWEsim.functions.postprocessing.compute import *
from AWEsim.functions.aerodynamics.aero_from_SD import compute_sd_coefficients, reconstruct_body_coefficients
from AWEsim.functions.postprocessing.plotting import *


# =============================================================================
# Settings
# =============================================================================

FILE_DIR = Path(__file__).resolve().parent
CASE_DIR = FILE_DIR.parent
SIM_DIR = CASE_DIR / "SIM_test"

# =============================================================================
# Load simulation data
# =============================================================================

reference, states, forces_mpc, forces_cfd = load_simulation_data_pumping(SIM_DIR)

# =============================================================================
# Postprocess simulation data
# =============================================================================

tether_tension = calculate_tether_tension(states, forces_cfd)
power = calculate_power(states, forces_cfd)


aero = calculate_aerodynamic_properties(states)

body_ref = calculate_reference_body_coefficients(reference)

body_mpc = calculate_body_coefficients(reference, states, forces_mpc, properties=aero)
body_cfd = calculate_body_coefficients(reference, states, forces_cfd, properties=aero)

wind_mpc = calculate_lift_drag_coefficients(reference, states, forces_mpc, properties=aero, body_coefficients=body_mpc)
wind_cfd = calculate_lift_drag_coefficients(reference, states, forces_cfd, properties=aero, body_coefficients=body_cfd)

reconstructed = reconstruct_body_coefficients(states)

# =============================================================================
# Plot results
# =============================================================================

# plot_trajectory(reference, states)
#plot_motion(reference, states)
# plot_power(reference, states, power)
plot_tether(reference, states, tether_tension)
# plot_control_surfaces(reference, states)
# plot_angular_rates(reference, states)
#plot_aerodynamic_properties(reference,aero)
plot_body_coefficients(body_ref, body_mpc, body_cfd)
# plot_lift_drag_coefficients(reference, wind_mpc, wind_cfd)

#plot_coefficient_contributions(reconstructed, contributions=["total", "angles", "rotation", "control_surfaces"])

