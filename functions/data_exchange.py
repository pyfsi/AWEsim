from tkinter.font import names

import numpy as np
import csv


# =============================================================================
# Load general simulation data
# =============================================================================

def load_simulation_data(sim_dir):
    """Load states, manoeuvre data and CFD force/moment coefficients."""

    states = np.genfromtxt(sim_dir / "states.out", delimiter=",")
    maneuvre = np.genfromtxt(sim_dir / "maneuvres.out", delimiter=",")
    cfd_coeff = np.genfromtxt(sim_dir / "CFD" / "force_coefficients.out", skip_header=3) 

    return states, maneuvre, cfd_coeff

def load_simulation_data_pumping(sim_dir):
    """Load the reference trajectory and AWEsim simulation outputs.

    Returns
    -------
    reference, states, controls, forces_mpc, forces_cfd : dict
        Each dictionary contains named NumPy arrays. Tether length, speed,
        and acceleration are scaled by 500, as in the original code.
    """

    awebox_dir = sim_dir / "AWEbox"
    reference_file = awebox_dir / "Flight_path" / "megawes_optimised_path_cfd.csv" #TODO: not hardcoded
    if not reference_file.is_file():
        raise FileNotFoundError(f"Reference trajectory is missing: {reference_file}")
    reference = csv2dict(str(reference_file))

    def read_columns(filename, names):
        data = np.genfromtxt(awebox_dir / filename, delimiter=",", ndmin=2)
        if np.isnan(data[:, -1]).all():
            data = data[:, :-1]
        if data.shape[1] != len(names):
            raise ValueError(
                f"{filename}: expected {len(names)} columns, got {data.shape[1]}"
            )
        return dict(zip(names, data.T))

    state_columns = (
        "time q10_x q10_y q10_z dq10_vx dq10_vy dq10_vz "
        "omega10_x omega10_y omega10_z "
        "r10_1 r10_2 r10_3 r10_4 r10_5 r10_6 r10_7 r10_8 r10_9 "
        "delta10_da delta10_de delta10_dr l_t dl_t "
        "ddelta10_da ddelta10_de ddelta10_dr ddl_t"
    ).split()
    states = read_columns("states_controls.out", state_columns)

    for name in ("l_t", "dl_t", "ddl_t"):
        states[name] *= 500 #TODO: avoid hardcoding scaling factor

    force_columns = "time Fx Fy Fz Mx My Mz".split()
    forces_mpc = read_columns("forces_MPC.out", force_columns)
    forces_cfd = read_columns("forces_CFD.out", force_columns)

    return reference, states, forces_mpc, forces_cfd

# =============================================================================
# State data
# =============================================================================

def get_state_data(filename):
    """
    Load aircraft state data.
    """

    states = np.genfromtxt(filename, delimiter=",")

    return {
        "time": states[:, 0],
        "position": states[:, 1:4],
        "velocity": states[:, 4:7],
        "rotation": states[:, 10:19].reshape(-1, 3, 3),
    }

# =============================================================================
# CFD data (Fluent exports)
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

    data = np.genfromtxt(filename, delimiter=",", skip_header=1)

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
# AWEBOX data 
# =============================================================================

#%% Awebox read function
def csv2dict(fname):

    # read csv file
    with open(fname, 'r') as f:
        reader = csv.DictReader(f)

        # get fieldnames from DictReader object and store in list
        headers = reader.fieldnames

        # store data in columns
        columns = {}
        for row in reader:
            for fieldname in headers:
                val = row.get(fieldname).strip('[]')
                if val == '':
                    val = '0.0'
                columns.setdefault(fieldname, []).append(float(val))

    # add periodicity
    for fieldname in headers:
        columns.setdefault(fieldname, []).insert(0, columns[fieldname][-1])
    columns['time'][0] = 0.0

    return columns

#%% Get awebox flight data
def get_awebox_data():
    path = os.getcwd()
    fname = path + "/outputs_megawes_trajectory_cfd_results.csv"
    if not os.path.exists(fname):
        print("ERROR: File is missing. Exit.")
        #exit()
    else:
        data = csv2dict(fname)
        
    #position
    x= np.array(data['x_q10_0'])
    y= np.array(data['x_q10_1'])
    z= np.array(data['x_q10_2'])
    
    #velocity
    vx= data['x_dq10_0']
    vy= data['x_dq10_1']
    vz= data['x_dq10_2']
    
    #angular velocity
    om_x = data['x_omega10_0']
    om_y = data['x_omega10_1']
    om_z = data['x_omega10_2']
    
    # attitude
    phi = data['x_r10_0']
    theta = data['x_r10_1']
    psi = data['x_r10_2']
    
    #aero
    alpha = np.array(data['outputs_aerodynamics_alpha1_0'])
    beta = np.array(data['outputs_aerodynamics_beta1_0'])
    
    return x,y,z,vx,vy,vz,om_x,om_y,om_z,phi,theta,psi,alpha,beta