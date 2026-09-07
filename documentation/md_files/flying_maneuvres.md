# Flying maneuvres

This section explains how the AWEsim code can be used to fly prescribed maneuvres, such as a rolling, yawing, pitching flight while simulatenously deflecting control surfaces or changing flight speed, angle-of-attack and sideslip; all combinations are possible. This can be used to test new aircraft configurations, and build surrogate or simplified models from the data of these simulations.

## PRE-processing

General pre-processing steps are explained in previous section. This sections assumes the virtual wind environment (CFD) and structural model (CSM) is setup. What's left is specifing the prescribed motion (DYN) of the maneuvre you want to fly.

This can be done using the script `build_maneuvre.py` ; which can be copied from an example case. This script allows you define the maneuvre you want to prescibe to the VWE; define the nominal condition and the excitation around that nominal condition.

For example a rolling maneuvre where the control surfaces are deflected once after eachother:

<p style="text-align:center;">
  <img src="https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/maneuvre_rolling_CSD.svg"
       alt="Rolling maneuvre"
       width="75%" />
</p>

When flagged, the required filed to run the simulation can be written to the user-defined folder; e.g. `SIM0_rolling_CSD`. Also the required background domain of the VWE can be checked with this script.


## POST-processing


<p style="text-align:center;">
  <img src="https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/Pressure_rolling.gif"
       alt="Rolling maneuvre Pressure gif"
       width="75%" />
</p>
![Rolling maneuvre](https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/Pressure_rolling.gif)


More details on post-processing functionalities are explained in the next section.

