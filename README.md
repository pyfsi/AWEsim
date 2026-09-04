[![AWEsim banner](https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/cover_github.png)](https://github.com/pyfsi/AWEsim)

# The AWEsim Installation Manual

AWEsim is a geometry-resolved aero-servo-elastic simulation framework developed for airborne wind energy (AWE) systems. The aero-servo-elastic coupling algorithms and infrastructure are written in Python and built on top of [CoCoNuT](https://github.com/pyfsi/coconut), a coupling code for numerical tools for efficient partitioned multiphysics simulations, with a focus on fluid-structure interaction (FSI).

The [AWEsim branch on CoCoNuT](https://github.com/pyfsi/coconut/tree/AWEsim) adds the following functionalities:
- Rigid-body motion in the [ANSYS Fluent](https://ansys.synopsys.com/products/fluids/ansys-fluent) solver wrapper
- Control-surface deflections of aircraft
- Coupling to the AWE system dynamics and control toolbox [AWEbox]()

This GitHub repository provides all the necessary scripts to set up and postprocess AWEsim simulations, including some examples. The simulations can be used in the design phase, when the geometry of the aircraft is known, to assess detailed unsteady aero-servo-elastic phenomena.

The framework is currently applied to ground-generation airborne wind energy systems, but can be extended to any aircraft-like systems exhibiting dynamic motion, flexible structures, and multiple moving control surfaces.

## Installation

Choose or create a directory (e.g., `Software`) to install AWEsim, move to this directory, and clone the GitHub repository with SSH:

```bash
git clone git@github.com:pyfsi/AWEsim.git
```
Make sure your public key has been added to your GitHub account.

The AWEsim project is set up by running `setup_awesim.sh`:

```bash
cd AWEsim
chmod +x setup_awesim.sh
./setup_awesim.sh
```
This script takes care of:

- Installing CoCoNuT (branch AWEsim)
- Installing AWEbox (TODO) --> from files on the cluster; later from GitHub (first test compatibility)
- Installing mshGen (TODO)
- Installing Python requirements.txt (TODO)
- Configuring `.bashrc`
- Downloading example (CFD) files from the UGent FM cluster

## Quick test

Test the installation by running the examples; the results are described in the user manual.

## Documentation

- Theory: PhD book
- Practical: The AWEsim User Manual (link).

## References

- PhD book
- Aero-servo paper


