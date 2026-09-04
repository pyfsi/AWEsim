# Code Structure

The AWEsim code provides the necessary scripts to fly prescribed maneuvers and pumping-cycle simulations in a CFD environment, including aeroelastic coupling. The code also relies on external software such as CoCoNuT, mshGen, and AWEbox. It is recommended to install AWEsim in a folder such as `📁 Software` together with these external tools. This is taken into account by `📄 setup_awesim.sh`.

The AWEsim code is structured as follows:

```text
📁 AWEsim/
├── 📁 aircraft/
│   └── 📁 megawes/
│       └── 📄 megawes.json
│   └── 📁 aircraft_X
├── 📁 cases/
│   └── 📁 case_megawes_maneuvres/
│   └── 📁 case_megawes_pumping_cycle_10mps
│       └── 📁 PRE
│           └── 📁 CFD
│               └── 📁 meshing
│                   └── 📁 components
│                   └── 📁 aircraft
│               └── 📁 setup
│           └── 📁 CSM
│           └── 📁 DYN
│               └── 📄 path_generation.py
│       └── 📁 SIM0
│           └── 📁 CFD
│           └── 📁 CSM
│           └── 📁 DYN
│               └── 📄 path_tracking.py
│           └── 📄 parameters.json
│           └── 📄 run_simulation.py
│       └── 📁 SIM_test1
│       └── 📁 POST
│   └── 📁 case_X
├── 📁 functions/
│   └── 📁 aerodynamics/
│   └── 📁 kinematics/
│   └── 📁 postprocessing/
│   └── 📄 functions.py
├── 📁 helpers/
├── 📁 documentation/
├── 📄 README.md
├── 📄 requirements.txt
├── 📄 setup_awesim.sh
└── 📄 .gitignore
```

The AWEsim code consists of five main folders. `📁 aircraft` contains the relevant high-level information on the aircraft under study. All cases should use this information to avoid inconsistent data across different cases. `📁 cases` contains the example cases and a structure that can be used to set up new cases. `📁 functions` contains the core AWEsim functionalities and is called throughout the setup, execution, and postprocessing of cases. `📁 helpers` contains additional scripts that can be useful but are not strictly required for the workflow. Finally, the documentation is gathered in `📁 documentation` in the form of Markdown files and forms the basis of this manual.

To set up and simulate a `📁 case`, preprocessing, simulation, and postprocessing steps are required. The necessary files are gathered in `📁 PRE`, `📁 SIM0`, and `📁 POST`, respectively. `📁 SIM0` contains all files required to launch a simulation. It is recommended to copy this folder to `📁 SIM_testX` (using a useful test description name) before launch, because the folders are modified during the simulation.

A `📁 SIM` folder should contain the necessary aerodynamic case and data files in `📁 CFD`, the files of the structural model in `📁 CSM`, and the dynamics and control-related files in `📁 DYN`. The coupled simulation parameters are configured in `📄 parameters.json`, and the simulation is launched by running `📄 run_simulation.py`. This reflects the same case structure as CoCoNuT.