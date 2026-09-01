# Introduction

(Explain what the project is about and what problem it solves.)

Airborne wind energy systems are prone to various unsteady effects (Check slides AWEC 2026)

Aero-servo-elastic triangle

The AWEsim framework is build to capture those effects in a detailed way using high fidelity software.

This means that geometry of the AWE aircraft is resolved in the aerodynamics and structual model of the simulation framework.

The focus on the simulation is on geometry-resolved aerodynamics and the inclusion of dynamics, this is captured using a virtual wind environent (VWE) constructed using CFD that enables the motion of lifting surfaces.

Focus on high-fidelity simulations using CFD, the virtual wind environment (VWE) is the core of AWEsim.

This manual introduces the practical implementation and use of AWEsim. For a detailed report on the methods behind it, you are refered to: Link to PhD book