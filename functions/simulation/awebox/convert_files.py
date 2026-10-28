import numpy as np
import json

# Load the JSON file
with open("../parameters.json", "r") as file:
    data = json.load(file)

# Extract values from the "settings" section
dt = data["settings"]["delta_t"]
start_from_timestep = data["settings"]["timestep_start"]

def convert_files(time_step_ref):
    # Define the input and output files
    input_file1 = "../CFD/forces.frp"
    input_file2 = "../CFD/moments.frp"
    output_file = "../CFD/force_coefficients2.out"

    # Define the time increment between force reports (Adjust this based on your simulation time step increment)
    time_increment = dt
    time_step1 = start_from_timestep
    time_step_list = []
    flow_time_list = []
    cx_list = []
    cy_list = []
    cz_list = []
    cmx_list = []
    cmy_list = []
    cmz_list = []

    # Open the input and output files
    with open(input_file1, "r") as infile:
        # Loop through each line of the input file
        for line in infile:
            # Search for the "Net" line under "Forces - Direction Vector (1 0 0)"
            if line.strip().startswith("Net"):
                # The next three values are Total coefficients (Cx, Cy, Cz)
                forces = line.split()
                if forces[1].startswith('('):
                    cx = float(forces[16].strip('()'))
                    cy = float(forces[17].strip('()'))
                    cz = float(forces[18].strip('()'))

                    cx_list.append(cx)
                    cy_list.append(cy)
                    cz_list.append(cz)

                    # Increment the time step for the next set of forces
                    time_step1 += 1

    time_step2 = start_from_timestep
    with open(input_file2, "r") as infile:
        # Loop through each line of the input file
        for line in infile:
            # Search for the "Net" line under "Forces - Direction Vector (1 0 0)"
            if line.strip().startswith("Net"):
                # The next three values are Total coefficients (Cx, Cy, Cz)
                forces = line.split()
                if forces[1].startswith('('):
                    cmx = float(forces[16].strip('()'))
                    cmy = float(forces[17].strip('()'))
                    cmz = float(forces[18].strip('()'))

                    time_step_list.append(time_step2) #moments file is written last, so timestep of this file is taken
                    flow_time_list.append(time_step2*time_increment)

                    cmx_list.append(cmx)
                    cmy_list.append(cmy)
                    cmz_list.append(cmz)

                    # Increment the time step for the next set of forces
                    time_step2 += 1

    # Open the input and output files
    #TODO:only write next timestep, now whole file is rewritten
    if time_step2 > time_step_ref and time_step1 == time_step2: #write only if new timestep and same count for forces and moments
        with open(output_file, "w") as outfile:
            # Write header to the output file
            outfile.write("\"force_coefficients\"\n")
            outfile.write("\"Time Step\" \"flow-time etc..\"\n")
            outfile.write("(\"Time Step\" \"flow-time\" \"cx\" \"cy\" \"cz\" \"cmx\" \"cmy\" \"cmz\")\n")
            for i in np.arange(len(time_step_list)):
                # Write the extracted data to the output file
                outfile.write(f"{time_step_list[i]}\t{flow_time_list[i]:.6f}\t{cx_list[i]}\t{cy_list[i]}\t{cz_list[i]}\t{cmx_list[i]}\t{cmy_list[i]}\t{cmz_list[i]}\n")

    return

