[![AWEsim banner](https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/cover_github.png)](https://github.com/pyfsi/AWEsim)

# The AWEsim Installation Manual

AWEsim is a geometry-resolved aero-servo-elastic simulation framework developed for airborne wind energy (AWE) systems. The aero-servo-elastic coupling algorithms and infrastructure are written in Python and build on top of [CoCoNuT](https://github.com/pyfsi/coconut), a coupling code for numerical tools for efficient partitioned multi-physics simulations, with a focus on fluid-structure interaction (FSI).

The [AWEsim branch on CoCoNuT](https://github.com/pyfsi/coconut/tree/AWEsim) adds the following functionalities:
- Rigid-body motion in the [ANSYS Fluent](https://ansys.synopsys.com/products/fluids/ansys-fluent) solver wrapper
- Control surface deflections of aircraft
- Coupling to AWE system dynamics and control toolbox [AWEbox]()

This github repository provides all the necessary scripts to setup and postprocess AWEsim simulations, including some examples. The simulations can be used in the design phase where the geometry of the aircraft is known, to assess detailed unsteady aero-servo-elastic phenomena.

The framework is currently applied to ground-gen airborne wind energy systems, but can be extented to any aircraft-like systems exhibiting dynamic motion, flexible structure, and that use multiple moving control surfaces.

## Installation

Choose or create a directory (e.g. `Software`) to install AWEsim, move to this directory and clone the Github repository with SSH:

```bash
git clone git@github.com:pyfsi/AWEsim.git
```
Make sure your public key is added to you github account. 

The AWEsim project is set up by running `setup_awesim.sh`:

```bash
cd AWEsim
chmod +x setup_awesim.sh
./setup_awesim.sh
```
This script takes care off:

- Installing CoCoNuT (branch AWEsim)
- Installing AWEbox (TODO) --> from files on cluster; later from GitHub (first test compatibility)
- Installing mshGen (TODO)
- Installing python requirements.txt (TODO)
- Configuring .bashrc
- Download example (CFD) files from UGent FM cluster 

## Quick test

Test the installation by running the examples, the results are desribed in the user manual.

## Documentation

- Theory: PhD book
- Practical: The AWEsim User Manual (link).

## References

- PhD book
- Aero-servo paper


