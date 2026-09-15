from pathlib import Path
import matplotlib.pyplot as plt

#AWEsim functionalities
from AWEsim.functions.postprocessing.visuals import (create_single_visual, create_animation_frames)
from AWEsim.functions.postprocessing.create_video import create_video


# =============================================================================
# Main settings
# =============================================================================

FILE_DIR = Path(__file__).resolve().parent
CASE_DIR = FILE_DIR.parent

SIM_NAME = "SIM_rolling_CSD_test"
SIM_DIR = CASE_DIR / SIM_NAME

FLOW_PROPERTY = "P"
VIEW = "B" #TODO: not implemented

RESULTS_DIR = SIM_DIR / "CFD" / "Results"
STATES_FILE = SIM_DIR / "states.out"

ANIMATION_DIR =  FILE_DIR / "Animations" / "Animation_rolling"

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

START = 5
STOP = 905
STEP = 5

FPS = 20
DPI = 300
FRAME_PREFIX = "Pressure_"
VIDEO_NAME = "Pressure.mp4"


# =============================================================================
# Main
# =============================================================================

create_single_visual(
    timestep=100,
    RESULTS_DIR=RESULTS_DIR,
    COMPONENTS=COMPONENTS,
    STATES_FILE=STATES_FILE,
    FLOW_PROPERTY=FLOW_PROPERTY,
    ANIMATION_DIR=ANIMATION_DIR,
    FRAME_PREFIX=FRAME_PREFIX,
    DPI=DPI
)

# create_animation_frames(
#     START=START,
#     STOP=STOP,
#     STEP=STEP,
#     RESULTS_DIR=RESULTS_DIR,
#     COMPONENTS=COMPONENTS,
#     STATES_FILE=STATES_FILE,
#     FLOW_PROPERTY=FLOW_PROPERTY,
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