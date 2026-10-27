import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from mpl_toolkits.mplot3d.art3d import Line3DCollection

#AWEsim
from AWEsim.functions.data_exchange import get_cfd_data


# =============================================================================
# Plot settings
# =============================================================================

FIGURE_SIZE = (5, 3)

POINT_SIZE = 1e-1
WAKE_POINT_SIZE = 5e-4

TIME_FONTSIZE = 12
COLORBAR_FONTSIZE = 8

CMAP_pressure = "coolwarm"
CMAP_velocity = "RdYlBu_r"
CMAP_friction = "seismic_r"
CMAP_power = LinearSegmentedColormap.from_list("red_white_green", ["red", "white", "green"])

PRESSURE_VMIN = -7
PRESSURE_VMAX = 4

VELOCITY_VMIN = 40
VELOCITY_VMAX = 70

FRICTION_VMIN = -1
FRICTION_VMAX = 1

COLORBAR_LABELS = {
    "P": "Static pressure [kPa]",
    "CP": "Pressure coefficient [-]",
    "V": "Velocity [m/s]",
    "F": "Wall shear x (body frame) [Pa]",
}

# Component colors for the control surface visualization (CS)
COMPONENT_COLORS = {
    "wing": "grey",
    "aileron_left": "blue",
    "aileron_right": "blue",
    "vtail_left": "purple",
    "vtail_right": "purple",
    "tail": "green",
}

# Trajectory colored per loop
LOOP_LENGTH = 4000 # timesteps
LOOP_COLORS = ["purple", "green", "blue"]

# Wake filter
WAKE_X_MIN = 500 # [m]
WAKE_DISTANCE_MIN = 50 # [m] distance to the aircraft

# Axis limit of the inertial view, relative to the lateral extent of the reference trajectory
REFERENCE_MARGIN = 1.25


# =============================================================================
# View settings
# =============================================================================
#   I  : inertial frame
#   I2 : inertial frame, centred at the aircraft CG
#   B  : body frame
#   A  : aerodynamic frame (sideslip neglected)
#
#   limit = None scales the axes to the reference trajectory.
#   span_crop only keeps the CFD nodes with |y| < span_crop.

VIEW_SETTINGS = {
    "I": {
        "limit": None, "elevation": 20, "azimuth": 225, "ortho": False, "span_crop": None,
        "point_size": 1e-9, "line_width": 1, "tether_width": 0.2,
    },
    "I2": {
        "limit": 14, "elevation": 0, "azimuth": 0, "ortho": False, "span_crop": None,
        "point_size": POINT_SIZE, "line_width": 1.5, "tether_width": 1,
    },
    "B": {
        "limit": 14, "elevation": 80, "azimuth": 0, "ortho": False, "span_crop": None,
        "point_size": POINT_SIZE, "line_width": 1.5, "tether_width": 1,
    },
    "A": {
        "limit": 8, "elevation": 0, "azimuth": -90, "ortho": True, "span_crop": 4.7,
        "point_size": POINT_SIZE, "line_width": 1.5, "tether_width": 1,
    },
}


def get_view_settings(view, reference_path, camera=None):
    """Combine the default settings of the view with the camera overrides."""

    if view not in VIEW_SETTINGS:
        raise ValueError(f"Unknown view: {view}")

    settings = {**VIEW_SETTINGS[view], **(camera or {})}

    settings.setdefault("center", reference_path.mean(axis=0) if view == "I" else np.zeros(3))

    if settings["limit"] is None:
        settings["limit"] = REFERENCE_MARGIN * np.abs(reference_path[:, 1]).max()

    return settings


# =============================================================================
# Reference frames
# =============================================================================

#TODO: include sideslip in the aerodynamic rotation matrix
def aerodynamic_rotation(alpha):
    """Rotation from body to aerodynamic frame (alpha in degrees, sideslip neglected)."""

    alpha = np.radians(alpha)

    return np.array([[ np.cos(alpha), 0, np.sin(alpha)],
                     [ 0            , 1, 0            ],
                     [-np.sin(alpha), 0, np.cos(alpha)]])


def transform_to_view(points, view, position, rotation, alpha):
    """Transform earth-frame points (N, 3) to the frame of the selected view."""

    if view == "I":
        return points

    points = points - position

    if view == "I2":
        return points

    if view == "B":
        return points @ rotation.T

    if view == "A":
        return points @ (aerodynamic_rotation(alpha) @ rotation).T

    raise ValueError(f"Unknown view: {view}")


# =============================================================================
# Data
# =============================================================================

def get_wake_data(results_dir, timestep):
    """Load the wake points (N, 3) from a Fluent export file."""

    data = np.genfromtxt(results_dir / f"wake_back-{timestep:04d}", delimiter=",", skip_header=1)

    return data[:, 1:4]


def get_cfd_points(cfd):
    """Node coordinates (N, 3) of the CFD data."""

    return np.column_stack([cfd["x"], cfd["y"], cfd["z"]])


def merge_components(cfd):
    """Combine the CFD data of all aircraft components."""

    components = list(cfd.values())

    return {variable: np.concatenate([component[variable] for component in components]) for variable in components[0]}


def crop_span(points, cfd, span_crop):
    """Only keep the nodes with |y| < span_crop."""

    if span_crop is None:
        return points, cfd

    mask = np.abs(points[:, 1]) < span_crop

    return points[mask], {variable: values[mask] for variable, values in cfd.items()}


# =============================================================================
# Plot configuration
# =============================================================================

def create_3d_axis(settings):
    """Create and configure the 3D plotting axis of the selected view."""

    fig = plt.figure(figsize=FIGURE_SIZE)
    ax = fig.add_subplot(projection="3d")

    if settings["ortho"]:
        ax.set_proj_type("ortho")

    center = settings["center"]
    limit = settings["limit"]

    ax.set_xlim(center[0] - limit, center[0] + limit)
    ax.set_ylim(center[1] - limit, center[1] + limit)
    ax.set_zlim(center[2] - limit, center[2] + limit)

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_zlabel("z [m]")

    ax.elev = settings["elevation"]
    ax.azim = settings["azimuth"]

    ax.grid(False)
    ax.set_axis_off()

    return fig, ax


# =============================================================================
# Plot flow property
# =============================================================================

def plot_flow_property(ax, cfd, points, flow_property, rotation, point_size):
    """Plot the selected CFD flow property."""

    x, y, z = points.T

    if flow_property == "P":

        values = cfd["pressure"] / 1000

        return ax.scatter(x, y, z, c=values, s=point_size, cmap=CMAP_pressure, vmin=PRESSURE_VMIN, vmax=PRESSURE_VMAX)

    if flow_property == "CP":

        return ax.scatter(x, y, z, c=cfd["cp"], s=point_size, cmap=CMAP_pressure)

    if flow_property == "V":

        return ax.scatter(x, y, z, c=cfd["velocity"], s=point_size, cmap=CMAP_velocity, vmin=VELOCITY_VMIN, vmax=VELOCITY_VMAX)

    if flow_property == "F":

        # Wall shear in body frame
        shear = np.column_stack([cfd["shear_x"], cfd["shear_y"], cfd["shear_z"]]) @ rotation.T

        return ax.scatter(x, y, z, c=shear[:, 0], s=point_size, cmap=CMAP_friction, vmin=FRICTION_VMIN, vmax=FRICTION_VMAX)

    if flow_property == "N":

        return ax.scatter(x, y, z, color="grey", s=point_size)

    raise ValueError(f"Unknown flow property: {flow_property}")


def plot_components(ax, cfd, to_view, span_crop, point_size):
    """Plot the aircraft components, colored to highlight the control surfaces."""

    for component, color in COMPONENT_COLORS.items():

        if component not in cfd:
            continue

        points, _ = crop_span(to_view(get_cfd_points(cfd[component])), cfd[component], span_crop)

        ax.scatter(points[:, 0], points[:, 1], points[:, 2], color=color, s=point_size)


# =============================================================================
# Plot trajectory
# =============================================================================

def plot_trajectory_loops(ax, path, start, line_width):
    """Plot the trajectory with a different color for each loop."""

    loops = np.arange(start, start + len(path)) // LOOP_LENGTH

    for loop in np.unique(loops):

        segment = path[loops == loop]

        ax.plot(segment[:, 0], segment[:, 1], segment[:, 2], linewidth=line_width, color=LOOP_COLORS[loop % len(LOOP_COLORS)])


def plot_trajectory_power(ax, path, power, start, line_width):
    """Plot the trajectory colored by the instantaneous power."""

    segments = np.stack([path[:-1], path[1:]], axis=1)

    # Same color scale for all timesteps, centred at zero
    norm = TwoSlopeNorm(vmin=-power.max(), vcenter=0, vmax=power.max())

    lines = Line3DCollection(segments, cmap=CMAP_power, norm=norm, linewidth=line_width)
    lines.set_array(power[start:start + len(segments)])

    ax.add_collection(lines)


# =============================================================================
# Main plotting function
# =============================================================================

def plot_timestep(timestep, cfd, states, reference, aero, power=None, wake=None, flow_property="P", view="B",
                  trajectory="loop", trajectory_start=0, time_offset=0, colorbar=False, camera=None):
    """
    Create a 3D visualization for one timestep.

    Parameters
    ----------
    timestep : int
        CFD timestep.
    cfd : dict
        CFD data per aircraft component.
    states : dict
        Aircraft state data (AWEbox states_controls.out).
    reference : dict
        Reference trajectory.
    aero : dict
        Aerodynamic properties, see calculate_aerodynamic_properties.
    power : numpy.ndarray, optional
        Power, required to color the trajectory by power.
    wake : numpy.ndarray, optional
        Wake points (N, 3) in earth frame.
    flow_property : str
        Property to visualize: P, CP, F, V, CS or N.
    view : str
        Reference frame: I, I2, B or A.
    trajectory : str or None
        Trajectory coloring: loop, power or None (not shown).
    trajectory_start : int
        First timestep of the plotted trajectory.
    time_offset : float
        Time [s] subtracted from the displayed time.
    colorbar : bool
        Add a colorbar of the flow property.
    camera : dict, optional
        Overrides of the default view settings.

    Returns
    -------
    matplotlib.figure.Figure
        Generated figure.
    """

    i = timestep - 1 # states start at the first timestep

    path = np.column_stack([states["q10_x"], states["q10_y"], states["q10_z"]])
    reference_path = np.column_stack([reference["x_q10_0"], reference["x_q10_1"], reference["x_q10_2"]])

    position = path[i]
    rotation = aero["rotation"][i]
    alpha = aero["alpha"][i]

    def to_view(points):
        return transform_to_view(points, view, position, rotation, alpha)

    # Create figure
    settings = get_view_settings(view, reference_path, camera)
    fig, ax = create_3d_axis(settings)

    # Plot flow property
    if flow_property == "CS":
        scatter = plot_components(ax, cfd, to_view, settings["span_crop"], settings["point_size"])
    else:
        cfd = merge_components(cfd)
        points, cfd = crop_span(to_view(get_cfd_points(cfd)), cfd, settings["span_crop"])
        scatter = plot_flow_property(ax, cfd, points, flow_property, rotation, settings["point_size"])

    # Wake, away from the aircraft
    if wake is not None:
        wake = wake[wake[:, 0] >= WAKE_X_MIN]
        wake = to_view(wake[np.linalg.norm(wake - position, axis=1) > WAKE_DISTANCE_MIN])

        ax.scatter(wake[:, 0], wake[:, 1], wake[:, 2], s=WAKE_POINT_SIZE, color="blue")

    # Reference trajectory
    reference_path = to_view(reference_path)

    ax.plot(reference_path[:, 0], reference_path[:, 1], reference_path[:, 2], linestyle="dotted", linewidth=settings["line_width"], color="grey")

    # Aircraft trajectory
    trajectory_path = to_view(path[trajectory_start:timestep])

    if trajectory == "loop":
        plot_trajectory_loops(ax, trajectory_path, trajectory_start, settings["line_width"])
    elif trajectory == "power":
        plot_trajectory_power(ax, trajectory_path, power, trajectory_start, settings["line_width"])
    elif trajectory is not None:
        raise ValueError(f"Unknown trajectory coloring: {trajectory}")

    # Tether
    tether = to_view(np.vstack([np.zeros(3), position]))

    ax.plot(tether[:, 0], tether[:, 1], tether[:, 2], linewidth=settings["tether_width"], color="black")

    # Time
    time = states["time"][i] - time_offset

    ax.text2D(0.05, 0.95, f"Time = {time:.2f} s", fontsize=TIME_FONTSIZE, transform=ax.transAxes)

    # Colorbar
    if colorbar and flow_property in COLORBAR_LABELS:
        cbar = fig.colorbar(scatter, location="bottom", shrink=0.6, fraction=0.05, pad=0.15)
        cbar.set_label(COLORBAR_LABELS[flow_property], fontsize=COLORBAR_FONTSIZE)
        cbar.ax.tick_params(labelsize=COLORBAR_FONTSIZE)
    else:
        plt.tight_layout()

    return fig

# =============================================================================
# Create single visualization
# =============================================================================

def create_single_visual(timestep, RESULTS_DIR, COMPONENTS, reference, states, aero, power, ANIMATION_DIR, FRAME_PREFIX, DPI,
                         FLOW_PROPERTY="P", VIEW="B", TRAJECTORY="loop", TRAJECTORY_START=0, TIME_OFFSET=0,
                         SHOW_WAKE=False, COLORBAR=False, CAMERA=None, PLOT=True, SAVE=True):
    """Create one visualization, optionally save and/or show it."""

    #Get CFD data
    cfd = {component: get_cfd_data(RESULTS_DIR / f"data_{component}-{timestep:04d}") for component in COMPONENTS}
    wake = get_wake_data(RESULTS_DIR, timestep) if SHOW_WAKE else None

    #Plot the timestep
    fig = plot_timestep(
        timestep, cfd, states, reference, aero,
        power=power,
        wake=wake,
        flow_property=FLOW_PROPERTY,
        view=VIEW,
        trajectory=TRAJECTORY,
        trajectory_start=TRAJECTORY_START,
        time_offset=TIME_OFFSET,
        colorbar=COLORBAR,
        camera=CAMERA,
    )

    #Save and show the figure
    if SAVE:
        ANIMATION_DIR.mkdir(parents=True, exist_ok=True)
        filename = (ANIMATION_DIR / f"{FRAME_PREFIX}{timestep:04d}.png")
        fig.savefig(filename, dpi=DPI, bbox_inches="tight")
        print(f"Saved: {filename}")
    if PLOT:
        plt.show()
    else:
        plt.close(fig)

# =============================================================================
# Create animation frames
# =============================================================================

def create_animation_frames(START, STOP, STEP, **visual_settings):
    """Create all PNG frames. Keyword arguments are passed to create_single_visual."""

    for timestep in range(START, STOP, STEP):

        print(f"Processing timestep {timestep}...")

        create_single_visual(
            timestep=timestep,
            **visual_settings,
            PLOT=False,
            SAVE=True,
        )
