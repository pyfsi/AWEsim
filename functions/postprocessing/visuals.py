import numpy as np
import matplotlib.pyplot as plt

#AWEsim
from AWEsim.functions.data_exchange import get_cfd_data_all, get_state_data


# =============================================================================
# Plot settings
# =============================================================================

FIGURE_SIZE = (10, 6)

PLOT_LIMIT = 15

POINT_SIZE = 5

CMAP = "coolwarm"
CMAP_pressure = "coolwarm"
CMAP_velocity = "viridis"

PRESSURE_VMIN = -20
PRESSURE_VMAX = 9

AXIS_ELEVATION = 30
AXIS_AZIMUTH = 0


# =============================================================================
# Plot configuration
# =============================================================================

def create_3d_axis():
    """Create and configure the standard 3D plotting axis."""

    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_subplot(projection="3d")

    ax.set_xlim(-PLOT_LIMIT, PLOT_LIMIT)
    ax.set_ylim(-PLOT_LIMIT, PLOT_LIMIT)
    ax.set_zlim(-PLOT_LIMIT, PLOT_LIMIT)

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_zlabel("z [m]")

    ax.elev = AXIS_ELEVATION
    ax.azim = AXIS_AZIMUTH

    ax.grid(False)
    ax.set_axis_off()

    return fig, ax


# =============================================================================
# Plot flow property
# =============================================================================

def plot_flow_property(ax, cfd, x, y, z, flow_property):

    """Plot the selected CFD flow property."""

    #TODO: replace x,y,x with points

    if flow_property == "P":

        values = cfd["pressure"] / 1000

        return ax.scatter(x, y, z, c=values, s=POINT_SIZE, cmap=CMAP_pressure, vmin=PRESSURE_VMIN,  vmax=PRESSURE_VMAX)

    if flow_property == "CP":

        return ax.scatter(x, y, z, c=cfd["cp"], s=POINT_SIZE,  cmap= CMAP_pressure)

    if flow_property == "V":

        return ax.scatter(x, y, z, c=cfd["velocity"],  s=POINT_SIZE, cmap=CMAP_velocity)

    if flow_property == "F":

        return ax.scatter(x, y, z, c=cfd["shear"], s=POINT_SIZE, cmap=CMAP_velocity)

    if flow_property == "N":

        return ax.scatter(x, y, z, color="grey", s=POINT_SIZE)

    raise ValueError(f"Unknown flow property: {flow_property}")


# =============================================================================
# Main plotting function
# =============================================================================

def plot_timestep(timestep, cfd, states, flow_property= "P"):
    """
    Create a 3D visualization for one timestep.

    Parameters
    ----------
    timestep : int
        CFD timestep.
    cfd : dict
        CFD data.
    states : dict
        Aircraft state data.
    flow_property : str
        Property to visualize: P, CP, F, V or N.

    Returns
    -------
    matplotlib.figure.Figure
        Generated figure.
    """

    i = timestep - 1 #TODO: check if this is correct

    position = states["position"][i]

    # Coordinates relative to aircraft CG
    x = cfd["x"] - position[0]
    y = cfd["y"] - position[1]
    z = cfd["z"] - position[2]

    # Create figure
    fig, ax = create_3d_axis()

    # Plot flow property
    plot_flow_property(ax, cfd, x, y, z, flow_property)

    # Aircraft trajectory
    trajectory = states["position"] - position

    ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2],linestyle="dotted", color="grey")
    ax.plot(trajectory[:timestep, 0], trajectory[:timestep, 1], trajectory[:timestep, 2], color="purple")


    # Time
    time = states["time"][i]

    ax.text2D(0.05, 0.95, f"Time = {time:.2f} s", fontsize=12, transform=ax.transAxes)

    plt.tight_layout()

    return fig

# =============================================================================
# Create single visualization
# =============================================================================

def create_single_visual(timestep, RESULTS_DIR, COMPONENTS, STATES_FILE, FLOW_PROPERTY, ANIMATION_DIR, FRAME_PREFIX, DPI,PLOT = True):
    """Create and save one visualization."""

    #Get state and CFD data
    states = get_state_data(STATES_FILE)
    cfd_data = get_cfd_data_all(RESULTS_DIR, COMPONENTS, timestep)

    #Plot the timestep
    fig = plot_timestep(timestep,cfd_data, states, flow_property=FLOW_PROPERTY)

    #Save and show the figure
    ANIMATION_DIR.mkdir(parents=True, exist_ok=True)
    filename = (ANIMATION_DIR / f"{FRAME_PREFIX}{timestep:04d}.png")
    fig.savefig(filename, dpi=DPI, bbox_inches="tight")
    print(f"Saved: {filename}")
    if PLOT:
        plt.show()

# =============================================================================
# Create animation frames
# =============================================================================

def create_animation_frames( START, STOP, STEP, RESULTS_DIR, COMPONENTS, STATES_FILE, FLOW_PROPERTY, ANIMATION_DIR, FRAME_PREFIX, DPI):
    """Create all PNG frames."""

    for timestep in range(START, STOP, STEP):

        print(f"Processing timestep {timestep}...")

        create_single_visual(
            timestep=timestep,
            RESULTS_DIR=RESULTS_DIR,
            COMPONENTS=COMPONENTS,
            STATES_FILE=STATES_FILE,
            FLOW_PROPERTY=FLOW_PROPERTY,
            ANIMATION_DIR=ANIMATION_DIR,
            FRAME_PREFIX=FRAME_PREFIX,
            DPI=DPI,
            PLOT = False
        )


