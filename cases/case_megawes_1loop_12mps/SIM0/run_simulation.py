import coconut
import subprocess
import json


# Import parameters
parameter_file_name = "parameters.json"
with open(parameter_file_name, 'r') as parameter_file:
    parameters = json.load(parameter_file)

# Run AWEbox
process = subprocess.Popen(["/bin/bash", "-c", "source ~/.bashrc && set_awebox && exec python3 megawes_external_forces_simulation_restart.py"], cwd="./AWEbox/")

# Run CoCoNuT
simulation = coconut.Analysis(parameters)
simulation.run()


