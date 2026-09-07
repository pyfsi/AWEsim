# Flying maneuvres

This section explains how the AWEsim code can be used to fly prescribed maneuvres, such as rolling, yawing, or pitching flight while simultaneously deflecting control surfaces or changing flight speed, angle of attack, and sideslip. All combinations are possible. These simulations can be used to test new aircraft configurations and to build surrogate or simplified models from the simulation data.

## PRE-processing

General pre-processing steps are explained in the previous section. This section assumes the virtual wind environment (CFD) and structural model (CSM) are set up. What's left is specifying the prescribed motion (DYN) of the maneuvre you want to fly.

This can be done using the script `build_maneuvre.py`, which can be copied from an example case. This script lets you define the maneuvre you want to prescribe to the VWE, the nominal condition, and the excitation around that nominal condition.

For example, a rolling maneuvre where the control surfaces are deflected sequentially:

<p style="text-align:center;">
  <img src="https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/maneuvre_rolling_CSD.svg"
       alt="Rolling maneuvre"
       width="75%" />
</p>

When flagged, the required files to run the simulation can be written to the user-defined folder; e.g. `SIM0_rolling_CSD`. These files include:

- Write `move_zone_X.dat` files in the CFD folders
- Write maneuvre descriptions `states.out` and `maneuvre.out` for post-processing.

Finally, the required background domain of the VWE can also be checked with this script.

## SIMulation

`SIM0` folders contain the necessary files to launch a simulation.

Configure the `parameters.json` file:
- Match total simulation time and timestep with the maneuvre
- Enable `rigid_body_motion`
- Define the `moving_zones`
- Define the FSI interface — see the CoCoNuT manual

Copy the `SIM0` folder to `SIM_*testdescription*` before launching. For large simulations that will generate a lot of data, it is advised to run on `/lusers/temp`.

Launch the simulation with `python run_simulation.py`. This launches the CoCoNuT branch of AWEsim.


## POST-processing

The AWEsim code provides scripts to post-process the data and visualize the results of the simulation.

`plot_maneuvre.py` can be used to plot the resulting forces and moments of the simulation:

<p style="text-align:center;">
  <img src="https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/maneuvre_rolling_CSD_forces.svg"
       alt="Rolling maneuvre"
       width="75%" />
</p>


`create_visual.py` can be used to make contour plots of the flow data and to create time animations:


<p style="text-align:center;">
  <img src="https://raw.githubusercontent.com/pyfsi/AWEsim/main/documentation/images/Pressure_rolling.gif"
       alt="Rolling maneuvre Pressure gif"
       width="60%" />
</p>


More details on post-processing functionalities are explained in the POST-processing section.

