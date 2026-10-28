# PRE-processing

See AWEsim workflow in slides.

## Aircraft geometry definition

## CFD

### Meshing aircraft components

### Setting up the virtual wind environment (VWE)

#### Flying maneuvres

- Build the background grid such that it encompasses the maneuvre.
- Position the aircraft facing into the wind, so that its initial DCM equals the identity matrix.
- TODO: draw axis system
- Applying some wind speed (e.g. 10 m/s) at the inlet is recommended to stabilize the CFD calculations.


## CSM

The structural model is currently limited to an FEM representation of the MegAWES aircraft in Abaqus, obtained from TU Delft (Dylan Eijkelhof). It was originally developed in NASTRAN and later converted to Abaqus.

This model has been translated so that its origin lies at the CG of the aircraft (x: back, y: right wing, z: up). The surfaces of the main wing and ailerons have been split into a suction side (SS) and a pressure side (PS) to obtain good interpolation at the FSI interface. For preparing Abaqus cases to be used with CoCoNuT, the reader is referred to the CoCoNuT documentation on [Abaqus](https://pyfsi.github.io/coconut/abaqus.html).

A clamped boundary condition is applied at the center nodes of this structural model, so rigid-body motion is not yet included in the structural model. The resulting file is called `MegAWES_CG_SSPS.inp`. It can be used as a starting point for other cases simulating the MegAWES aircraft. The `.inp` footer has been adapted from an example to work with the Abaqus CSE.

To be coupled with the VWE, which includes the rigid-body motion, the structural model must still be moved to the initial position of the pumping cycle, so that it matches the aircraft in the VWE at the initial time step. This is done manually in the Abaqus GUI by first rotating the model to the initial attitude and then translating it to the initial position. This attitude and position are case-dependent and are determined by AWEbox. The resulting file is `MegAWES_CG_SSPS_IC.inp`.


## DYN

- Flying maneuvres
- Pumping cycle simulations
