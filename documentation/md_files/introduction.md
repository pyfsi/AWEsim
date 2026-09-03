# Introduction

Airborne wind energy (AWE) systems are prone to various unsteady effects. This means that the aerodynamic forces and moments on the aircraft change significantly over its operation.
These unsteady effects arise from the unsteady wind field, for example the change of wind with height, the unsteady movement of the aircraft, and encountering of wakes from its own or other systems. More locally, due to the circular motion, we have a distributed velocity across the wing span, we have the movement of the control surfaces to steer the aircraft and counteract the disturbances, and the deformation of the structure or aero-elastic effects.

![Unsteady](https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/unsteady.gif)

## Aero-servo-elastic coupling

To simulate and analyze this unsteady behavior, different engineering disciplines are required. These include the field of aerodynamics, structural dynamics, which concerns the behavior of the structure, and system dynamics and control, which studies the rigid-body motion and control of the system. The coupling or interaction of these disciplines is typically referred to as the aero-servo-elasticity triangle.


![Aero-servo-elastic triangle](https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/aeroservoelastic_coupling.png)

The AWEsim framework is build to capture those effects in a detailed way using high fidelity software. This means that geometry of the AWE aircraft is resolved in the aerodynamics and structual model of the simulation framework.

## Virtual Wind Environment

The focus of the simulation framework is on geometry-resolved aerodynamics and the inclusion of dynamics, this is captured using a virtual wind environent (VWE) constructed using CFD that enables the motion of lifting surfaces. The overset technique is an important method to enable the rigid-body motion and control surface deflections of the aircraft.

![VWE](https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/VWE.png)

This manual explains how the AWEsim framework can be used. For a detailed report on the methods behind it, you are refered to: Link to PhD book.