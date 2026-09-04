# Introduction

Airborne wind energy (AWE) systems are prone to various unsteady effects. This means that the aerodynamic forces and moments on the aircraft change significantly during operation.
These unsteady effects arise from the unsteady wind field, for example changes in wind speed with height, the unsteady motion of the aircraft, and encounters with wakes from its own system or other systems. More locally, due to the circular motion, there is a distributed velocity across the wing span, movement of the control surfaces to steer the aircraft and counteract disturbances, and deformation of the structure, which gives rise to aeroelastic effects.

![Unsteady](https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/Unsteady.gif)

## Aero-servo-elastic coupling

To simulate and analyze this unsteady behavior, different engineering disciplines are required. These include aerodynamics, structural dynamics, which concerns the behavior of the structure, and system dynamics and control, which studies the rigid-body motion and control of the system. The coupling or interaction of these disciplines is typically referred to as the aero-servo-elasticity triangle.

<p style="text-align:center;">
  <img src="https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/aeroservoelastic_coupling.png"
       alt="Aero‑servo‑elastic triangle"
       width="50%" />
</p>

The AWEsim framework is built to capture these effects in detail using high-fidelity software. This means that the geometry of the AWE aircraft is resolved in the aerodynamic and structural models of the simulation framework.

## Virtual Wind Environment

The focus of the simulation framework is on geometry-resolved aerodynamics and the inclusion of dynamics. This is captured using a virtual wind environment (VWE) constructed with CFD, which enables the motion of lifting surfaces. The overset technique is an important method for enabling rigid-body motion and control-surface deflections of the aircraft.

![VWE](https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/VWE.png)

This manual explains how the AWEsim framework can be used. For a detailed report on the methods behind it, please refer to: Link to PhD book.

