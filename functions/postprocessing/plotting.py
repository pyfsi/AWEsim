import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# Global plotting settings
# =============================================================================

font = {"family": "sans-serif", "weight": "normal", "size": 12}
plt.rc("font", **font)

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

    # Deflection keys
    def_keys = {
        "da": (["delta10_da", "x_delta10_da_0", "x_delta10_da"], ["delta10_da", "x_delta10_da_0", "x_delta10_da"]),
        "de": (["delta10_de", "x_delta10_de_0", "x_delta10_de"], ["delta10_de", "x_delta10_de_0", "x_delta10_de"]),
        "dr": (["delta10_dr", "x_delta10_dr_0", "x_delta10_dr"], ["delta10_dr", "x_delta10_dr_0", "x_delta10_dr"]),
    }

    # Rate keys
    rate_keys = {
        "da": (["ddelta10_da", "x_ddelta10_da_0", "x_ddelta10_da"], ["ddelta10_da", "x_ddelta10_da_0", "x_ddelta10_da"]),
        "de": (["ddelta10_de", "x_ddelta10_de_0", "x_ddelta10_de"], ["ddelta10_de", "x_ddelta10_de_0", "x_ddelta10_de"]),
        "dr": (["ddelta10_dr", "x_ddelta10_dr_0", "x_ddelta10_dr"], ["ddelta10_dr", "x_ddelta10_dr_0", "x_ddelta10_dr"]),
    }

    fig, axs = plt.subplots(3, 2, figsize=(12, 10), sharex=True)

    labels = [("Aileron", "da"), ("Elevator", "de"), ("Rudder", "dr")]

    for i, (label, key) in enumerate(labels):
        # deflection
        ax_def = axs[i, 0]
        ref_def = _get_first(reference, def_keys[key][0])
        sim_def = _get_first(states, def_keys[key][1])
        if ref_def is not None:
            ax_def.plot(t_ref, ref_def, linestyle="--", color="black", label="REF")
        if sim_def is not None:
            ax_def.plot(t_mpc, sim_def, color="green", label="SIM")
        ax_def.set_ylabel(f"{label} deflection")
        ax_def.grid(True)
        if i == 0:
            ax_def.legend()

        # rate
        ax_rate = axs[i, 1]
        ref_rate = _get_first(reference, rate_keys[key][0])
        sim_rate = _get_first(states, rate_keys[key][1])
        if ref_rate is not None:
            ax_rate.plot(t_ref, ref_rate, linestyle="--", color="black", label="REF")
        if sim_rate is not None:
            ax_rate.plot(t_mpc, sim_rate, color="green", label="SIM")
        ax_rate.set_ylabel(f"{label} rate")
        ax_rate.grid(True)
        if i == 0:
            ax_rate.legend()

    for ax in axs[-1]:
        ax.set_xlabel("Time [s]")

    fig.suptitle("Control surface deflections and rates")
    fig.tight_layout()
    plt.show()