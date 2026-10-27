from pathlib import Path
import matplotlib.pyplot as plt

#AWEsim functionalities
from AWEsim.functions.data_exchange import load_simulation_data_pumping
from AWEsim.functions.postprocessing.compute import calculate_aerodynamic_properties, calculate_power
from AWEsim.functions.postprocessing.visuals_pumping import (create_single_visual, create_animation_frames)
from AWEsim.functions.postprocessing.create_video import create_video

# =============================================================================
# Main settings
# =============================================================================

FILE_DIR = Path(__file__).resolve().parent
CASE_DIR = FILE_DIR.parent
SIM_DIR = CASE_DIR / "SIM_Restart2400"
RESULTS_DIR = SIM_DIR / "CFD" / "Results"
ANIMATION_DIR =  FILE_DIR / "Animations" / "Animation_Restart2400"

SAVE = False
FLOW_PROPERTY = "P" # (P) pressure, (CP) pressure coefficient, (F) friction, (V) velocity, (CS) control surfaces, (N) nothing
VIEW = "I2" # (I) inertial, (I2) inertial centred at CG, (B) body, (A) aerodynamic
TRAJECTORY = "loop" # (loop) colored per loop, (power) colored by power, (None) not shown
TRAJECTORY_START = 4000 # first timestep of the plotted trajectory
TIME_OFFSET = 20 # [s] subtracted from the displayed time
SHOW_WAKE = True
COLORBAR = False
CAMERA = None # overrides of the view settings, e.g. {"limit": 12, "elevation": 20, "azimuth": 45}

# =============================================================================
# Load simulation data
# =============================================================================

reference, states, forces_mpc, forces_cfd = load_simulation_data_pumping(SIM_DIR)

# =============================================================================
# Postprocess simulation data
# =============================================================================

aero = calculate_aerodynamic_properties(states)
power = calculate_power(states, forces_cfd)

# =============================================================================
# Aircraft components
# =============================================================================

COMPONENTS = [
    "wing",
    "tail",
    "vtail_left",
    "vtail_right",
    "aileron_right",
    "aileron_left",
    "wingtip_left",
    "wingtip_right",
    "aircraft_c",
]

# =============================================================================
# Animation settings
# =============================================================================

START = 4000
STOP = 8000
STEP = 10

FPS = 20
DPI = 600
FRAME_PREFIX = "Pressure_"
VIDEO_NAME = "Pressure.mp4"

# =============================================================================
# Main
# =============================================================================

create_single_visual(
    timestep=6000,
    RESULTS_DIR=RESULTS_DIR,
    COMPONENTS=COMPONENTS,
    reference=reference,
    states=states,
    aero=aero,
    power=power,
    FLOW_PROPERTY=FLOW_PROPERTY,
    VIEW=VIEW,
    TRAJECTORY=TRAJECTORY,
    TRAJECTORY_START=TRAJECTORY_START,
    TIME_OFFSET=TIME_OFFSET,
    SHOW_WAKE=SHOW_WAKE,
    COLORBAR=COLORBAR,
    CAMERA=CAMERA,
    ANIMATION_DIR=ANIMATION_DIR,
    FRAME_PREFIX=FRAME_PREFIX,
    DPI=DPI,
    SAVE=SAVE
)

# create_animation_frames(
#     START=START,
#     STOP=STOP,
#     STEP=STEP,
#     RESULTS_DIR=RESULTS_DIR,
#     COMPONENTS=COMPONENTS,
#     reference=reference,
#     states=states,
#     aero=aero,
#     power=power,
#     FLOW_PROPERTY=FLOW_PROPERTY,
#     VIEW=VIEW,
#     TRAJECTORY=TRAJECTORY,
#     TRAJECTORY_START=TRAJECTORY_START,
#     TIME_OFFSET=TIME_OFFSET,
#     SHOW_WAKE=SHOW_WAKE,
#     COLORBAR=COLORBAR,
#     CAMERA=CAMERA,
#     ANIMATION_DIR=ANIMATION_DIR,
#     FRAME_PREFIX=FRAME_PREFIX,
#     DPI=DPI
# )

#create_video(
    #     input_folder=ANIMATION_DIR,
    #     output_file=ANIMATION_DIR / VIDEO_NAME,
    #     prefix=FRAME_PREFIX,
    #     start=START,
    #     stop=STOP,
    #     step=STEP,
    #     fps=FPS,
    # )
