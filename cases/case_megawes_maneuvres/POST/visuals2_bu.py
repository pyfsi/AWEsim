from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from functions.postprocessing.create_video import create_video


# =============================================================================
# Settings
# =============================================================================

FLOW_PROPERTY = "P"
VIEW = "I2"

FILE_DIR = Path(__file__).resolve().parent
CASE_DIR = FILE_DIR.parent
SIM_DIR = CASE_DIR / "SIM_test_rates2"

RESULTS_DIR = SIM_DIR / "CFD" / "Results"
ANIMATION_DIR = FILE_DIR / "Animations" / "Animation_main"


# =============================================================================
# CFD data
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


def get_cfd_data(component, timestep):
    """Load CFD surface data for one aircraft component."""

    filename = RESULTS_DIR / f"data_{component}-" / f"{timestep:04d}"

    data = np.genfromtxt(
        filename,
        delimiter=",",
        skip_header=1,
    )

    return {
        "x": data[:, 1],
        "y": data[:, 2],
        "z": data[:, 3],
        "pressure": data[:, 4],
        "cp": data[:, 5],
        "velocity": data[:, 6],
        "vx": data[:, 7],
        "vy": data[:, 8],
        "vz": data[:, 9],
        "shear": data[:, 10],
        "shear_x": data[:, 11],
        "shear_y": data[:, 12],
        "shear_z": data[:, 13],
    }


def get_cfd_data_all(timestep):
    """Load and combine CFD data for the complete aircraft."""

    components = [
        get_cfd_data(component, timestep)
        for component in COMPONENTS
    ]

    data = {}

    for variable in components[0]:
        data[variable] = np.concatenate(
            [component[variable] for component in components]
        )

    return data


# =============================================================================
# Dynamic simulation data
# =============================================================================

def get_state_data():
    """Load aircraft state data."""

    states = np.genfromtxt(
        SIM_DIR / "states.out",
        delimiter=",",
    )

    return {
        "time": states[:, 0],
        "position": states[:, 1:4],
        "velocity": states[:, 4:7],
        "rotation": states[:, 10:19].reshape(-1, 3, 3),
    }


# =============================================================================
# Plotting
# =============================================================================

def plot_timestep(timestep, show=True):
    """Create the CFD plot for one timestep."""

    cfd = get_cfd_data_all(timestep)
    states = get_state_data()

    # State at current timestep
    i = timestep - 1

    position = states["position"][i]

    # Coordinates relative to aircraft CG
    x = cfd["x"] - position[0]
    y = cfd["y"] - position[1]
    z = cfd["z"] - position[2]

    # -------------------------------------------------------------------------
    # Figure
    # -------------------------------------------------------------------------

    plt.close("all")

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(projection="3d")

    # Axis limits
    limit = 15

    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_zlim(-limit, limit)

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_zlabel("z [m]")

    ax.elev = 30
    ax.azim = 0

    ax.grid(False)
    ax.set_axis_off()

    # -------------------------------------------------------------------------
    # Pressure
    # -------------------------------------------------------------------------

    ax.scatter(
        x,
        y,
        z,
        c=cfd["pressure"] / 1000,
        s=5,
        cmap="coolwarm",
        vmin=-20,
        vmax=9,
    )

    # -------------------------------------------------------------------------
    # Trajectory
    # -------------------------------------------------------------------------

    trajectory = states["position"] - position

    ax.plot(
        trajectory[:, 0],
        trajectory[:, 1],
        trajectory[:, 2],
        linestyle="dotted",
        color="grey",
    )

    ax.plot(
        trajectory[:timestep, 0],
        trajectory[:timestep, 1],
        trajectory[:timestep, 2],
        color="purple",
    )

    # -------------------------------------------------------------------------
    # Time
    # -------------------------------------------------------------------------

    time = states["time"][i]

    ax.text2D(
        0.05,
        0.95,
        f"Time = {time:.2f} s",
        fontsize=12,
        transform=ax.transAxes,
    )

    plt.tight_layout()

    if show:
        plt.show()

    return fig, ax


# =============================================================================
# Save animation frames
# =============================================================================

def create_animation_frames(
    start=5,
    stop=405,
    step=5,
    dpi=300,
):
    """Create PNG frames for the animation."""

    ANIMATION_DIR.mkdir(parents=True, exist_ok=True)

    for timestep in range(start, stop, step):

        fig, _ = plot_timestep(timestep, show=False)

        filename = (
            ANIMATION_DIR
            / f"Pressure_{timestep:04d}.png"
        )

        fig.savefig(
            filename,
            dpi=dpi,
            bbox_inches="tight",
        )

        plt.close(fig)

        print(f"Saved {filename}")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    # Single timestep
    timestep = 250

    fig, _ = plot_timestep(timestep)
    fig.savefig(
        ANIMATION_DIR / f"Pressure_{timestep:04d}.png",
        dpi=300,
        bbox_inches="tight",
    )

    # Create all animation frames
    # create_animation_frames(
    #     start=5,
    #     stop=405,
    #     step=5,
    #     dpi=300,
    # )

    # Create video
    # create_video(
    #     input_folder=ANIMATION_DIR,
    #     output_file=ANIMATION_DIR / "Pressure.mp4",
    #     prefix="Pressure_",
    #     start=5,
    #     stop=405,
    #     step=5,
    #     fps=20,
    # )