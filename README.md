[![AWEsim banner](https://raw.githubusercontent.com/pyfsi/AWEsim/main/docs/images/cover_github.png)](https://github.com/pyfsi/AWEsim)

# The AWEsim Manual

AWEsim is a geometry-resolved aero-servo-elastic simulation framework developed for airborne wind energy (AWE) systems. The aero-servo-elastic coupling algorithms and infrastructure are written in Python and build on top of [CoCoNuT](https://github.com/pyfsi/coconut), a coupling code for numerical tools for efficient partitioned multi-physics simulations, with a focus on fluid-structure interaction (FSI).

The [AWEsim branch on CoCoNuT](https://github.com/pyfsi/coconut/tree/AWEsim) adds the following functionalities:
- Rigid-body motion in the [ANSYS Fluent](https://ansys.synopsys.com/products/fluids/ansys-fluent) solver wrapper
- Control surface deflections of aircraft
- Coupling to AWE system dynamics and control toolbox [AWEbox]()

This github repository provides all the necessary scripts to setup and postprocess AWEsim simulations, including some examples. The simulations can be used in the design phase where the geometry of the aircraft is known, to assess detailed unsteady aero-servo-elastic phenomena.

The framework is currently applied to ground-gen airborne wind energy systems, but can be extented to any aircraft-like systems exhibiting dynamic motion, flexible structure, and that use multiple moving control surfaces.



## 1. Introduction

(Explain what the project is about and what problem it solves.)

Airborne wind energy systems are prone to various unsteady effects (Check slides AWEC 2026)

Aero-servo-elastic triangle

The AWEsim framework is build to capture those effects in a detailed way using high fidelity software.

This means that geometry of the AWE aircraft is resolved in the aerodynamics and structual model of the simulation framework.

The focus on the simulation is on geometry-resolved aerodynamics and the inclusion of dynamics, this is captured using a virtual wind environent (VWE) constructed using CFD that enables the motion of lifting surfaces.

Focus on high-fidelity simulations using CFD, the virtual wind environment (VWE) is the core of AWEsim.

This manual introduces the practical implementation and use of AWEsim. For a detailed report on the methods behind it, you are refered to: Link to PhD book

## 2. Installation

Choose or create a directory (e.g. `Software`) to install AWEsim, move to this directory and clone the Github repository with SSH:

```bash
git clone git@github.com:pyfsi/AWEsim.git
cd AWEsim
chmod +x setup_awesim.sh
./setup_awesim.sh
```
Make sure your public key is added to you github account. The AWEsim project is set up by running `setup_awesim.sh`, which takes care off:

- Installing CoCoNuT (branch AWEsim)
- Installing AWEbox (TODO)
- Installing mshGen (TODO)
- Installing python requirements.txt (TODO)
- Configuring .bashrc
- Download example (CFD) files from UGent FM cluster

### Quick test

### Getting started

## 3. Project structure

## 4. User Guide

### Flying Maneuvres

![Rolling maneuvre](https://raw.githubusercontent.com/pyfsi/AWEsim/main/docs/images/Pressure_rolling.mp4)

### Prescribed pumping cycle simulations
To be published.

### Controlled pumping cycle simulations
To be published.

### Fully coupled aero-servo-elastic simulations
To be developed.

## 5. Develope Guide

Refer of the outlook of my book. 

### Useful Markdown syntax

| What you want | Markdown |
|---|---|
| **Title** | `# Title` |
| **Subtitle** | `## Subtitle` |
| **Sub-subtitle** | `### Section` |
| **Bold** | `**text**` |
| *Italic* | `*text*` |
| Link | `[text](https://example.com)` |
| Image | `![description](path/to/image.png)` |
| Bullet list | `- Item` |
| Numbered list | `1. Item` |
| Code | `` `code` `` |
| Code block | ` ```python ... ``` ` |
| Quote | `> Quote` |
| Horizontal line | `---` |
| Table | `\| Column \| Column \|` |

