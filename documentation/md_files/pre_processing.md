# PRE-processing workflow

See AWEsim workflow in slides.

## 1. Aircraft geometry definition

## 2. Aircraft mesh generation

### Meshing aircraft components

### Configuring aircraft components

## 3. Aircraft identification

### Flying maneuvres

- Build the background grid such that it encompasses the maneuvre.
- Position the aircraft facing into the wind, so that its initial DCM equals the identity matrix.
- TODO: draw axis system
- Applying some wind speed (e.g. 10 m/s) at the inlet is recommended to stabilize the CFD calculations.

### Calculating aerodynamic derivatives

## 4. Fligth path, dynamics and control generation

AWEsim currently uses awebox [link] to optimize a flight trajectory and to define a controller (MPC), to track that trajectory.

### a. Settings

Configure the settings of the AWE system in the `AWE_system_settings.py` (e.g. megawes_settings.py)
Important to consider both path generation and path tracking constraints.

TODO: provide full list of settings; physical settings, some imporant numerical settings

### b. Path and controller generation

Run `path_control_generation.py` to generate the trajectory and controller.

1.	Put `control_flag` and `compile_flag` to False to first generate a feasible trajectory.

2.	Visualize outputs “outputs_megawes_trajectory_cfd_results” with script `plot_awebox_results.py`.

3.	Put `control_flag` to true to check controller

4.	Put `compile_flag` to true to make compiled trajectory

Some tips:
- constrain the cycle period to an ‘easy’ number for later processing; e.g., 20s.

### c. Controller and tracking testing and implementation

1.	Test compiled trajectory with `path_tracking.py` 
2.	Copy trajectory (`Flight_path` folder) to SIM0
3.	Change Initial conditions `f_aero_CFDFW.py`: Last value in .csv file
4.	Check MPC settings awesim_path_tracking.py
5.	Check namingoutput folder under #load trial results 


## 5. Setting up the virtual wind environment (VWE)


## 2./5. Structural modelling (CSM)

The structural model is currently limited to an FEM representation of the MegAWES aircraft in Abaqus, obtained from TU Delft (Dylan Eijkelhof). It was originally developed in NASTRAN and later converted to Abaqus.

This model has been translated so that its origin lies at the CG of the aircraft (x: back, y: right wing, z: up). The surfaces of the main wing and ailerons have been split into a suction side (SS) and a pressure side (PS) to obtain good interpolation at the FSI interface. For preparing Abaqus cases to be used with CoCoNuT, the reader is referred to the CoCoNuT documentation on [Abaqus](https://pyfsi.github.io/coconut/abaqus.html).

A clamped boundary condition is applied at the center nodes of this structural model, so rigid-body motion is not yet included in the structural model. The resulting file is called `MegAWES_CG_SSPS.inp`. It can be used as a starting point for other cases simulating the MegAWES aircraft. The `.inp` footer has been adapted from an example to work with the Abaqus CSE.

To be coupled with the VWE, which includes the rigid-body motion, the structural model must still be moved to the initial position of the pumping cycle, so that it matches the aircraft in the VWE at the initial time step. This is done manually in the Abaqus GUI by first rotating the model to the initial attitude and then translating it to the initial position. This attitude and position are case-dependent and are determined by AWEbox. The resulting file is `MegAWES_CG_SSPS_IC.inp`.