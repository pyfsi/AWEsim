import coconut
import subprocess
import json


# Import parameters
parameter_file_name = "parameters.json"
with open(parameter_file_name, 'r') as parameter_file:
    parameters = json.load(parameter_file)

#Run AWEbox
#subprocess.Popen("python3 awesim_path_tracking.py", executable='/bin/bash',shell=True, cwd="./AWEbox/")

#Run CoCoNuT
simulation = coconut.Analysis(parameters)
simulation.run()

#TODO: kill the python (AWEbox)
