import numpy as np
import matplotlib.pyplot as plt


# =============================================================================
# Plot settings
# =============================================================================

FIGURE_SIZE = (10, 6)

PLOT_LIMIT = 15

POINT_SIZE = 5

PRESSURE_VMIN = -20
PRESSURE_VMAX = 9

AXIS_ELEVATION = 30
AXIS_AZIMUTH = 0


# =============================================================================
# CFD data
# =============================================================================

def get_cfd_data(filename):
    """
    Load CFD surface data from a Fluent export file.

    Parameters
    ----------
    filename : str or Path
        CFD data file.

    Returns
    -------
    dict
        CFD data.
    """

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


def get_cfd_data_all(results_dir, components, timestep):
    """
    Load and combine CFD data for all aircraft components.
    """

    component_data = []

    for component in components:

        filename = (
            results_dir
            / f"data_{component}-{timestep:04d}"
        )

        component_data.append(
            get_cfd_data(filename)
        )

    data = {}

    for variable in component_data[0]:

        data[variable] = np.concatenate(
            [
                component[variable]
                for component in component_data
            ]
        )

    return data


# =============================================================================
# State data
# =============================================================================

def get_state_data(filename):
    """
    Load aircraft state data.
    """

    states = np.genfromtxt(
        filename,
        delimiter=",",
    )

    return {
        "time": states[:, 0],
        "position": states[:, 1:4],
        "velocity": states[:, 4:7],
        "rotation": states[:, 10:19].reshape(-1, 3, 3),
    }


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

def plot_flow_property(
    ax,
    cfd,
    x,
    y,
    z,
    flow_property,
):
    """Plot the selected CFD flow property."""

    if flow_property == "P":

        values = cfd["pressure"] / 1000

        return ax.scatter(
            x,
            y,
            z,
            c=values,
            s=POINT_SIZE,
            cmap="coolwarm",
            vmin=PRESSURE_VMIN,
            vmax=PRESSURE_VMAX,
        )

    if flow_property == "CP":

        return ax.scatter(
            x,
            y,
            z,
            c=cfd["cp"],
            s=POINT_SIZE,
            cmap="coolwarm",
        )

    if flow_property == "V":

        return ax.scatter(
            x,
            y,
            z,
            c=cfd["velocity"],
            s=POINT_SIZE,
            cmap="viridis",
        )

    if flow_property == "F":

        return ax.scatter(
            x,
            y,
            z,
            c=cfd["shear"],
            s=POINT_SIZE,
            cmap="viridis",
        )

    if flow_property == "N":

        return ax.scatter(
            x,
            y,
            z,
            color="grey",
            s=POINT_SIZE,
        )

    raise ValueError(
        f"Unknown flow property: {flow_property}"
    )


# =============================================================================
# Main plotting function
# =============================================================================

def plot_timestep(
    timestep,
    cfd,
    states,
    flow_property="P",
):
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

    i = timestep - 1

    position = states["position"][i]

    # Coordinates relative to aircraft CG
    x = cfd["x"] - position[0]
    y = cfd["y"] - position[1]
    z = cfd["z"] - position[2]

    # Create figure
    fig, ax = create_3d_axis()

    # Plot flow property
    plot_flow_property(
        ax,
        cfd,
        x,
        y,
        z,
        flow_property,
    )

    # -------------------------------------------------------------------------
    # Aircraft trajectory
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

    return fig