from pathlib import Path
import matplotlib.pyplot as plt

#AWEsim functionalities
from functions.postprocessing.visuals import (get_cfd_data_all,get_state_data,plot_timestep)
from functions.postprocessing.create_video import create_video


# =============================================================================
# Case settings
# =============================================================================

SIM_NAME = "SIM_rolling_CSD"

FLOW_PROPERTY = "P"
VIEW = "I"


# =============================================================================
# Paths
# =============================================================================

FILE_DIR = Path(__file__).resolve().parent
CASE_DIR = FILE_DIR.parent

SIM_DIR = CASE_DIR / SIM_NAME

RESULTS_DIR = SIM_DIR / "CFD" / "Results"
STATES_FILE = SIM_DIR / "states.out"

ANIMATION_DIR = (
    FILE_DIR / "Animations" / "Animation_rolling"
)


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
# Create single visualization
# =============================================================================

def create_single_visual(timestep):
    """Create and save one visualization."""

    cfd = get_cfd_data_all(
        RESULTS_DIR,
        COMPONENTS,
        timestep,
    )

    states = get_state_data(STATES_FILE)

    fig = plot_timestep(
        timestep,
        cfd,
        states,
        flow_property=FLOW_PROPERTY,
    )

    filename = (
        ANIMATION_DIR
        / f"{FRAME_PREFIX}{timestep:04d}.png"
    )

    ANIMATION_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        filename,
        dpi=DPI,
        bbox_inches="tight",
    )

    plt.show()

    print(f"Saved: {filename}")


# =============================================================================
# Create animation frames
# =============================================================================

def create_animation_frames():
    """Create all PNG frames."""

    ANIMATION_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    states = get_state_data(STATES_FILE)

    for timestep in range(START, STOP, STEP):

        print(f"Processing timestep {timestep}...")

        cfd = get_cfd_data_all(
            RESULTS_DIR,
            COMPONENTS,
            timestep,
        )

        fig = plot_timestep(
            timestep,
            cfd,
            states,
            flow_property=FLOW_PROPERTY,
        )

        filename = (
            ANIMATION_DIR
            / f"{FRAME_PREFIX}{timestep:04d}.png"
        )

        fig.savefig(
            filename,
            dpi=DPI,
            bbox_inches="tight",
        )

        plt.close(fig)

        print(f"Saved: {filename}")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    # -------------------------------------------------------------------------
    # Single timestep
    # -------------------------------------------------------------------------

    #create_single_visual(timestep=500)

    # -------------------------------------------------------------------------
    # Animation
    # -------------------------------------------------------------------------

    #create_animation_frames()

    # -------------------------------------------------------------------------
    # Video
    # -------------------------------------------------------------------------

    create_video(
        input_folder=ANIMATION_DIR,
        output_file=ANIMATION_DIR / VIDEO_NAME,
        prefix=FRAME_PREFIX,
        start=START,
        stop=STOP,
        step=STEP,
        fps=FPS,
    )