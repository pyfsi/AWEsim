import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# Global plotting settings
#TODO
# =============================================================================

font = {"family": "sans-serif", "weight": "normal", "size": 15}
plt.rc("font", **font)

# # === Use LaTeX-style fonts globally ===
# rcParams['font.family'] = 'serif'
# rcParams['font.size'] = 10
# rcParams['text.usetex'] = True
# rcParams['axes.labelsize'] = 14
# rcParams['legend.fontsize'] = 10

# =============================================================================
# Plot aerodynamic coefficients
# =============================================================================

def plot_aerodynamic_coefficients(time, force_coeff, moment_coeff, force_coeff_sd, moment_coeff_sd):
    
    """Plot CFD and stability-derivative force/moment coefficients."""

    fig, axs = plt.subplots(3, 2, figsize=(10, 8), sharex=True)

    coefficients = [
        (force_coeff[:, 0], force_coeff_sd[:, 0], r"$C_x$", None),
        (force_coeff[:, 1], force_coeff_sd[:, 1], r"$C_y$", (-0.1, 0.1)),
        (force_coeff[:, 2], force_coeff_sd[:, 2], r"$C_z$", None),
        (moment_coeff[:, 0], moment_coeff_sd[:, 0], r"$C_l$", (-0.04, 0.04)),
        (moment_coeff[:, 1], moment_coeff_sd[:, 1], r"$C_m$", None),
        (moment_coeff[:, 2], moment_coeff_sd[:, 2], r"$C_n$", (-0.02, 0.02)),
    ]

    axes = [
        axs[0, 0],
        axs[1, 0],
        axs[2, 0],
        axs[0, 1],
        axs[1, 1],
        axs[2, 1],
    ]

    for ax, (cfd, sd, ylabel, ylim) in zip(axes, coefficients):

        ax.plot(time, cfd, label="CFD")
        ax.plot(time, sd, label="SD")

        ax.set_ylabel(ylabel)
        ax.grid(True)

        if ylim is not None:
            ax.set_ylim(ylim)

    axs[2, 0].set_xlabel("Time [s]")
    axs[2, 1].set_xlabel("Time [s]")

    axs[0, 0].legend()

    fig.tight_layout()
    plt.show()

# =============================================================================
# Plot trajectory
# =============================================================================

def plot_trajectory(reference, states):
    """Plot the reference and MPC trajectories in 3D."""
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    trajectories = (
        (
            reference["x_q10_0"],
            reference["x_q10_1"],
            reference["x_q10_2"],
            "black",
            "REF",
        ),
        (
            states["q10_x"],
            states["q10_y"],
            states["q10_z"],
            "green",
            "MPC",
        ),
    )

    for x, y, z, color, label in trajectories:
        ax.plot(x, y, z, color=color, label=label)
        ax.plot(x[0], y[0], z[0], "*", color=color)

    ax.set(
        title="Trajectory",
        xlim=(300, 600),
        ylim=(-100, 200),
        zlim=(50, 350),
        xlabel="x [m]",
        ylabel="y [m]",
        zlabel="z [m]",
    )

    ax.legend()
    fig.tight_layout()
    plt.show()

# =============================================================================
# Plot translational motion
#TODO Check error calculation
# =============================================================================

def plot_motion(reference, states):
    """Plot position, position error, velocity, and acceleration."""
    t_ref = np.asarray(reference["time"])
    t_mpc = np.asarray(states["time"])

    fig, ax = plt.subplots(3, 4, figsize=(16, 10), sharex="col")

    for i, axis in enumerate("xyz"):
        position = np.asarray(states[f"q10_{axis}"])
        velocity = np.asarray(states[f"dq10_v{axis}"])
        ref_position = np.asarray(reference[f"x_q10_{i}"])

        # np.gradient returns an array with the same length as t_mpc.
        acceleration = np.gradient(velocity, t_mpc)
        position_error = position - np.interp(t_mpc, t_ref, ref_position)

        ax[i, 0].plot(t_ref, ref_position, color="black", label="REF")
        ax[i, 0].plot(t_mpc, position, color="green", label="MPC")

        ax[i, 1].plot(t_mpc, position_error, color="green", label="MPC − REF")
        ax[i, 1].axhline(0, color="black", linewidth=0.7)

        ax[i, 2].plot(
            t_ref, reference[f"x_dq10_{i}"], color="black", label="REF"
        )
        ax[i, 2].plot(t_mpc, velocity, color="green", label="MPC")

        ax[i, 3].plot(
            t_ref,
            reference[f"outputs_xdot_from_var_ddq10_{i}"],
            color="black",
            label="REF",
        )
        ax[i, 3].plot(t_mpc, acceleration, color="green", label="MPC")

        ax[i, 0].set_ylabel(f"{axis} [m]")
        ax[i, 1].set_ylabel(f"e{axis} [m]")
        ax[i, 2].set_ylabel(f"v{axis} [m/s]")
        ax[i, 3].set_ylabel(f"a{axis} [m/s²]")

    for column in ax[-1]:
        column.set_xlabel("Time [s]")

    ax[0, 0].legend()
    fig.suptitle("Motion (translational)")
    fig.tight_layout()
    plt.show()

# =============================================================================
# Plot power
# =============================================================================

def plot_power(reference, states, P_mpc):

    t_ref = np.asarray(reference["time"])
    t_mpc = np.asarray(states["time"])

    P_avg = np.average(np.array(reference['outputs_performance_p_current_0']))
    P_avg_MPC = np.average(P_mpc)

    fig, ax = plt.subplots(1)
    
    ax.plot(t_ref, np.array(reference['outputs_performance_p_current_0'])/1e6,  linestyle='--', color = "black", label = "REF")
    ax.hlines([P_avg/1e6],0,20, linestyle=':', color = "black", label= "Average")

    ax.plot(t_mpc[:-1], P_mpc/1e6,  color = 'purple', label = "AWEsim")
    ax.hlines([P_avg_MPC/1e6],0,20, linestyle=':', color = "purple", label=f"_Avg AWEsim ({P_avg_MPC/1e6:.2f} MW)")

    ax.set_ylabel(r'Power (MW)', fontsize=15)
    ax.set_xlabel(r'Time (s)', fontsize=15)
    ax.grid(True)
    ax.legend(fontsize=15)
    ax.tick_params(axis='both', which='major', labelsize=15)  

    fig.suptitle("Power")
    fig.tight_layout()
    plt.show()


def plot_tether(reference, states, tension):
    """Plot tether length, speed, and tension for reference and simulation.

    Parameters
    - reference: dict-like with reference arrays (time, x_dl_t_0, x_l_t_0, outputs_local_performance_tether_force10_0)
    - states: dict-like with simulation arrays (time, dl_t, l_t). May contain `tension` already.
    """

    t_ref = np.asarray(reference.get("time"))
    t_mpc = np.asarray(states.get("time"))

    # helper to try multiple possible keys
    def _get_first(d, keys):
        for k in keys:
            if k in d:
                return np.asarray(d[k])
        return None

    # Reference values (try common AWEsim keys)
    l_ref = _get_first(reference, ["x_l_t_0", "l_t", "x_l_t"])
    dl_ref = _get_first(reference, ["x_dl_t_0", "dl_t"])  # tether speed
    Ft_ref = _get_first(reference, ["outputs_local_performance_tether_force10_0", "outputs_local_performance_tether_force10", "outputs_local_performance_tether_force_0"])

    # Simulation values
    l_sim = _get_first(states, ["l_t", "x_l_t_0", "x_l_t"])  # tether length
    dl_sim = _get_first(states, ["dl_t", "x_dl_t_0", "x_dl_t"])  # tether speed

    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)

    # Length
    ax = axes[0]
    if l_ref is not None:
        ax.plot(t_ref, l_ref, linestyle="--", color="black", label="REF")
    if l_sim is not None:
        ax.plot(t_mpc, l_sim, color="green", label="SIM")
    ax.set_ylabel("Tether length [m]")
    ax.grid(True)
    ax.legend()

    # Speed
    ax = axes[1]
    if dl_ref is not None:
        ax.plot(t_ref, dl_ref, linestyle="--", color="black", label="REF")
    if dl_sim is not None:
        ax.plot(t_mpc, dl_sim, color="green", label="SIM")
    ax.set_ylabel("Tether speed [m/s]")
    ax.grid(True)
    ax.legend()

    # Tension
    ax = axes[2]
    if Ft_ref is not None:
        ax.plot(t_ref, Ft_ref, linestyle="--", color="black", label="REF")
    if tension is not None:
        # If tension has same length as t_mpc-1 (from forward diff), align to t_mpc[:-1]
        if len(tension) == len(t_mpc) - 1:
            ax.plot(t_mpc[:-1], tension, color="green", label="SIM")
        else:
            ax.plot(t_mpc, tension, color="green", label="SIM")
    ax.set_ylabel("Tether tension [N]")
    ax.set_xlabel("Time [s]")
    ax.grid(True)
    ax.legend()

    fig.suptitle("Tether parameters")
    fig.tight_layout()
    plt.show()


def plot_control_surfaces(reference, states):
    """Plot control-surface deflections and their rates in a 3x2 grid.

    Rows: aileron (da), elevator (de), rudder (dr).
    Columns: deflection, rate.

    Both `reference` and `states` are dict-like; function will try common
    AWEsim key names and plot reference (dashed black) vs simulation (green).
    """

    t_ref = np.asarray(reference.get("time"))
    t_mpc = np.asarray(states.get("time"))

    def _get_first(d, keys):
        for k in keys:
            if k in d:
                return np.asarray(d[k])
        return None

    # Deflection keys: reference, simulation
    def_keys = {
        "da": (["x_delta10_0"], ["delta10_da"]),
        "de": (["x_delta10_1"], ["delta10_de"]),
        "dr": (["x_delta10_2"], ["delta10_dr"]),
    }

    # Rate keys
    rate_keys = {
        "da": (["u_ddelta10_0"], ["ddelta10_da" ]),
        "de": (["u_ddelta10_1"], ["ddelta10_de" ]),
        "dr": (["u_ddelta10_2"], ["ddelta10_dr"]),
    }

    fig, axs = plt.subplots(3, 2, figsize=(12, 10), sharex=True)

    labels = [("Aileron", "da"), ("Elevator", "de"), ("Rudder", "dr")]

    for i, (label, key) in enumerate(labels):
        # deflection
        ax_def = axs[i, 0]
        ref_def = _get_first(reference, def_keys[key][0])
        sim_def = _get_first(states, def_keys[key][1])
        if ref_def is not None:
            ax_def.plot(t_ref, np.rad2deg(ref_def), linestyle="--", color="black", label="REF")
        if sim_def is not None:
            ax_def.plot(t_mpc, np.rad2deg(sim_def), color="green", label="SIM")
        ax_def.set_ylabel(f"{label} deflection [deg]")
        ax_def.grid(True)
        if i == 0:
            ax_def.legend()

        # rate
        ax_rate = axs[i, 1]
        ref_rate = _get_first(reference, rate_keys[key][0])
        sim_rate = _get_first(states, rate_keys[key][1])
        if ref_rate is not None:
            ax_rate.plot(t_ref, np.rad2deg(ref_rate), linestyle="--", color="black", label="REF")
        if sim_rate is not None:
            ax_rate.plot(t_mpc, np.rad2deg(sim_rate), color="green", label="SIM")
        ax_rate.set_ylabel(f"{label} rate [deg/s] ")
        ax_rate.grid(True)
        if i == 0:
            ax_rate.legend()

    for ax in axs[-1]:
        ax.set_xlabel("Time [s]")

    fig.suptitle("Control surface deflections and rates")
    fig.tight_layout()
    plt.show()


def plot_angular_rates(reference, states):
    """Plot angular velocities in a 3x1 grid.

    Rows: roll, pitch, yaw.
    """

    t_ref = np.asarray(reference.get("time"))
    t_mpc = np.asarray(states.get("time"))

    def _get_first(d, keys):
        for k in keys:
            if k in d:
                return np.asarray(d[k])
        return None

    omega_keys = {
        "x": (["x_omega10_0", "omega10_x"], ["omega10_x", "omega_x"]),
        "y": (["x_omega10_1", "omega10_y"], ["omega10_y", "omega_y"]),
        "z": (["x_omega10_2", "omega10_z"], ["omega10_z", "omega_z"]),
    }

    fig, axs = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
    labels = [("Roll", "x"), ("Pitch", "y"), ("Yaw", "z")]

    for i, (label, axis) in enumerate(labels):
        ax_vel = axs[i]
        ref_vel = _get_first(reference, omega_keys[axis][0])
        sim_vel = _get_first(states, omega_keys[axis][1])
        if ref_vel is not None:
            ax_vel.plot(t_ref, np.rad2deg(ref_vel), linestyle="--", color="black", label="REF")
        if sim_vel is not None:
            ax_vel.plot(t_mpc, np.rad2deg(sim_vel), color="green", label="SIM")
        ax_vel.set_ylabel(f"{label} rate [deg/s]")
        ax_vel.grid(True)
        if i == 0:
            ax_vel.legend()

    axs[-1].set_xlabel("Time [s]")

    fig.suptitle("Angular velocities")
    fig.tight_layout()
    plt.show()


def plot_aerodynamic_properties(reference, properties):
    """Plot reference and current aerodynamic properties in a 2 × 2 layout."""
    time_ref = np.asarray(reference["time"])
    Va_ref = np.asarray(reference["outputs_aerodynamics_airspeed1_0"])
    alpha_ref = np.asarray(reference["outputs_aerodynamics_alpha1_0"])
    beta_ref = np.asarray(reference["outputs_aerodynamics_beta1_0"])

    time = np.asarray(properties["time"])

    fig, ax = plt.subplots(2, 2, figsize=(12, 8), sharex=True)

    ax[0, 0].plot(time_ref, Va_ref, color="black", linestyle="--", label="REF")
    ax[0, 1].plot(time_ref, np.rad2deg(alpha_ref), color="black", linestyle="--", label="REF")
    ax[1, 1].plot(time_ref, np.rad2deg(beta_ref), color="black", linestyle="--", label="REF")

    panels = (
        (ax[0, 0], "Va", "Airspeed [m/s]"),
        (ax[0, 1], "alpha", "Angle of attack [deg]"),
        (ax[1, 1], "beta", "Sideslip angle [deg]"),
        (ax[1, 0], "Re", "Reynolds number [-]"),
    )

    for axis, key, ylabel in panels:
        if key in properties:
            axis.plot(time, np.asarray(properties[key]), color="green", label="SIM")
        axis.set_ylabel(ylabel)
        axis.grid(True)
        if key in properties or (f"{key}_ref" in reference):
            axis.legend()

    ax[1, 0].set_xlabel("Time [s]")
    ax[1, 1].set_xlabel("Time [s]")
    fig.suptitle("Aerodynamic properties")
    fig.tight_layout()
    plt.show()


def plot_body_coefficients(body_ref, body_mpc, body_cfd):
    """Plot body-frame force and moment coefficients in a 3 × 2 layout."""
    fig, ax = plt.subplots(3, 2, figsize=(13, 10), sharex=True)

    rows = (
        ("Cx", "Cmx"),
        ("Cy", "Cmy"),
        ("Cz", "Cmz"),
    )

    for i, (force_key, moment_key) in enumerate(rows):
        for j, key in enumerate((force_key, moment_key)):
            axis = ax[i, j]
            axis.plot(
                body_ref["time"], body_ref[key],
                color="black", linestyle="--", label="REF",
            )
            axis.plot(
                body_mpc["time"], body_mpc[key],
                color="green", label="MPC",
            )
            axis.plot(
                body_cfd["time"], body_cfd[key],
                color="blue", label="CFD",
            )
            axis.set_ylabel(key)
            axis.grid(True)

    ax[0, 0].set_title("Force coefficients")
    ax[0, 1].set_title("Moment coefficients")
    ax[0, 0].legend()

    for axis in ax[-1]:
        axis.set_xlabel("Time [s]")

    fig.suptitle("Body-frame aerodynamic coefficients")
    fig.tight_layout()
    plt.show()


def plot_lift_drag_coefficients(reference, wind_mpc, wind_cfd):
    """Plot lift, drag, and lift-to-drag ratio in a 3 × 1 layout."""

    time_ref = np.asarray(reference["time"])
    CL_ref = np.asarray(reference["outputs_aerodynamics_CL1_0"])
    CD_ref = np.asarray(reference["outputs_aerodynamics_CD1_0"])

    fig, ax = plt.subplots(3, 1, figsize=(11, 10), sharex=True)

    ax[0].plot(time_ref, CL_ref, linestyle='--', color="black", label="REF")
    ax[1].plot(time_ref, CD_ref, linestyle='--', color="black", label="REF")
    ax[2].plot(time_ref, CL_ref / CD_ref, linestyle='--', color="black", label="REF")

    for data, color, label in (
        (wind_mpc, "green", "MPC"),
        (wind_cfd, "blue", "CFD"),
    ):
        lift = np.asarray(data["CL"])
        drag = np.asarray(data["CD"])

        # Avoid infinite values when drag is zero or very close to zero.
        lift_to_drag = np.divide(
            lift,
            drag,
            out=np.full_like(lift, np.nan, dtype=float),
            where=np.abs(drag) > 1e-12,
        )

        ax[0].plot(data["time"], lift, color=color, label=label)
        ax[1].plot(data["time"], drag, color=color, label=label)
        ax[2].plot(data["time"], lift_to_drag, color=color, label=label)

    for axis, ylabel in zip(ax, ("CL", "CD", "L/D")):
        axis.set_ylabel(ylabel)
        axis.grid(True)

    ax[0].legend()
    ax[-1].set_xlabel("Time [s]")
    fig.suptitle("Wind-axis aerodynamic coefficients")
    fig.tight_layout()
    plt.show()

def plot_coefficient_contributions(
    reconstructed,
    contributions=None,
):
    """Plot selected SD force and moment contributions in a 3 × 2 layout.

    Rows: body x, y, z.
    Columns: force coefficients, moment coefficients.
    """
    force = reconstructed["force"]
    moment = reconstructed["moment"]
    available = tuple(force)

    if contributions is None:
        contributions = available
    elif isinstance(contributions, str):
        contributions = (contributions,)

    unknown = set(contributions) - set(available)
    if unknown:
        raise ValueError(
            f"Unknown contributions: {sorted(unknown)}. "
            f"Available: {list(available)}"
        )

    fig, ax = plt.subplots(
        3, 2, figsize=(14, 10), sharex=True
    )
    time = reconstructed["time"]

    for row, axis_name in enumerate("xyz"):
        for contribution in contributions:
            ax[row, 0].plot(
                time,
                force[contribution][:, row],
                label=contribution,
            )
            ax[row, 1].plot(
                time,
                moment[contribution][:, row],
                label=contribution,
            )

        ax[row, 0].set_ylabel(f"C{axis_name}")
        ax[row, 1].set_ylabel(f"Cm{axis_name}")
        ax[row, 0].grid(True)
        ax[row, 1].grid(True)

    ax[0, 0].set_title("Force coefficients")
    ax[0, 1].set_title("Moment coefficients")
    ax[2, 0].set_xlabel("Time [s]")
    ax[2, 1].set_xlabel("Time [s]")

    # One shared legend keeps the six panels clear.
    handles, labels = ax[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=min(4, len(labels)))
    fig.suptitle("Reconstructed coefficient contributions")
    fig.tight_layout(rect=(0, 0.09, 1, 0.96))
    plt.show()