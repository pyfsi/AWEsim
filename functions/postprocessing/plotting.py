import matplotlib.pyplot as plt

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