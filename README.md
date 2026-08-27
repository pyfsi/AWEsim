[![AWEsim banner](https://raw.githubusercontent.com/pyfsi/AWEsim/main/docs/images/cover_github.png)](https://github.com/pyfsi/AWEsim)

# AWEsim

AWEsim is a geometry-resolved aero-servo-elastic simulation framework for airborne wind energy (AWE) systems. 

The coupling algorithms and infrastructure are written in python using a partitioned approach using folowing software dependence: CoCoNuT (Coupling code), Ansys Fluent (CFD), Abaqus (CSM), AWEbox (AWE dynamics and control).

AWEsim is Build on top of CoCoNuT (Focus on FSI), adding following functionalities:
- Rigid-body motion
- Control surface deflections of aircraft
- Coupling to dynamics and control (AWEbox)

The framework is currently applied to ground-gen airborne wind energy systems, but can be extented to any aircraft-like systems exhibiting dynamic motion use multiple moving control surfaces.

Focus now on AWE aircraft simulation, but can be extended to anything that moves ( awesim) and deforms (FSI, coconut), where a high-fidelity prediction of the flow around an object and its corresponding forces/moments and dynamic behavior are of interest to study.

The tool can be used in a more detailed design phase where the geometry of the aircraft is known, to assess detailed unsteady phenomena.

What is is not? AWEsim is not a meshing tool (link to mshGen), it requires existing grids of the aircraft components and lifting surfaces as input. It is not a design tool, it requires an existing geometry as input.

This manual introduces the practical implementation and use of AWEsim. For a detailed report on the methods behind it, you are refered to: Link to PhD book

## 1. Introduction

(Explain what the project is about and what problem it solves.)

Airborne wind energy systems are prone to various unsteady effects (Check slides AWEC 2026)

Aero-servo-elastic triangle

The AWEsim framework is build to capture those effects in a detailed way using high fidelity software.

This means that geometry of the AWE aircraft is resolved in the aerodynamics and structual model of the simulation framework.

The focus on the simulation is on geometry-resolved aerodynamics and the inclusion of dynamics, this is captured using a virtual wind environent (VWE) constructed using CFD that enables the motion of lifting surfaces.

Focus on high-fidelity simulations using CFD, the virtual wind environment (VWE) is the core of AWEsim.



## 2. Installation

Describe how to install or set up the project.

```bash
git clone https://github.com/username/project.git
cd project
pip install -r requirements.txt
```

- run install_awesim.sh 
- git clone coconut branch AWEsim
- git clone AWEsim
- add software folder to bashrc
- Get fluent files; from where? Zenodo?
- add github conncetion using public key
- VSCode: set python executable

## 3. Project structure

## 4. User Guide

### Flying Maneuvres

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

