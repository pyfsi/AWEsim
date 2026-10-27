# POST-processing

# Quatitative plots

`plot_results_maneuvre.py` Plotting resulting aerodynamic forces and moments from the maneuvre.

- load_simulation_data()
- compute_cfd_coefficients()
- compute_sd_coefficients()
- plot_aerodynamic_coefficients()

`plot_results_pumping.py` Plotting resulting aerodynamic forces and moments from the pumping cycles and other properties. 

- settings
  - case direction
- load_simulation_data()
  - reference traject
  - states/controls MPC
  - forces_MPC
  - forces_CFD
- postprocessing
  - calculate_tether_tension()
  - calculate_power()
  - calculate_aerodynamic_properties()
  - calculate_aerodynamic_coefficients()
  - reconstruct_aerodynamic_coefficients()
- plotting
  - plot_trajectory()
  - plot_motion()
  - plot_power()
  - plot_tether()
  - plot_control_surfaces()
  - plot_angular_rates()
  - plot_aerodynamic_properties()
  - plot_body_coefficients()
  - plot_lift_drag_coefficients()
  - plot_coefficient_contributions()


# Qualitative visuals

`create_visual.py`

Contour plots of the aerodynamic pressure (P), pressure coefficient (CP), velocity (V), and frition (F) on the aircraft.  

Use (N) to visualize just the aircraft.

The view of the plot can be set in the fixed earth frame (I), moving earth frame (I2), body frame (B), and aerodynamic frame (A).

Animations are saved in the `Animations` folder.

- create_single_visual()
- create_animation_frames()
- create_video()

## Pumping cycle visuals

`create_visuals_pumping_views.py`, in the `POST` folder of a pumping cycle case (e.g. `case_megawes_1loop_12mps`), makes 3D visuals of the aircraft flying along the pumping cycle trajectory. The plotting functions are in `functions/postprocessing/visuals_pumping.py`.

**Usage**

1. Set `SIM_DIR` to the simulation folder, e.g. `SIM_Restart2400`.
2. Choose the settings (see below).
3. Uncomment the function you need under `# Main` and run the script from the `POST` folder:

```
python create_visuals_pumping.py
```

The script reads the following simulation output:

- `CFD/Results/data_<component>-XXXX`: Fluent surface data, one file per component in `COMPONENTS`
- `CFD/Results/wake_back-XXXX`: wake points, only needed with `SHOW_WAKE = True`
- `AWEbox/states_controls.out`, `AWEbox/forces_MPC.out`, `AWEbox/forces_CFD.out`
- `AWEbox/Flight_path/megawes_optimised_path_cfd.csv`: reference trajectory

**Settings**

| Setting | Options |
|---|---|
| `FLOW_PROPERTY` | `P` pressure, `CP` pressure coefficient, `V` velocity, `F` wall shear (body x-direction), `CS` control surfaces coloured per component, `N` aircraft only |
| `VIEW` | `I` fixed earth frame, `I2` earth frame centred at the aircraft, `B` body frame, `A` aerodynamic frame (only the centre section, within 4.7 m of the symmetry plane) |
| `TRAJECTORY` | `"loop"` coloured per loop, `"power"` coloured by power (green: produced, red: consumed), `None` hidden |
| `TRAJECTORY_START` | First timestep of the plotted trajectory |
| `TIME_OFFSET` | Time [s] subtracted from the displayed time |
| `SHOW_WAKE` | Plot the wake |
| `COLORBAR` | Add a colour bar of the flow property |
| `CAMERA` | Override the default camera of the view, e.g. `{"limit": 12, "elevation": 20, "azimuth": 45}` |
| `SAVE` | Save the figure as PNG in `ANIMATION_DIR` |

**Single frame, animation and video**

- `create_single_visual(timestep=...)` plots one timestep and shows it.
- `create_animation_frames(START, STOP, STEP, ...)` saves one PNG per timestep in `ANIMATION_DIR`, named `FRAME_PREFIX` + timestep.
- `create_video(...)` combines these frames into the video `VIDEO_NAME` at `FPS` frames per second.

Only timesteps with Fluent output can be plotted (every 10th timestep in `case_megawes_1loop_12mps`).

**Examples**

| Visual | Settings |
|---|---|
| Pressure in the body frame | `VIEW = "B"`, `FLOW_PROPERTY = "P"` |
| Control surfaces | `VIEW = "B"`, `FLOW_PROPERTY = "CS"`, `CAMERA = {"limit": 12, "elevation": 20, "azimuth": 45}` |
| Pressure on the wing section | `VIEW = "A"`, `FLOW_PROPERTY = "P"`, `COLORBAR = True` |
| Wake along the trajectory | `VIEW = "I"`, `FLOW_PROPERTY = "V"`, `TRAJECTORY = None`, `SHOW_WAKE = True` |
| Power along the trajectory | `VIEW = "I"`, `FLOW_PROPERTY = "N"`, `TRAJECTORY = "power"`, `TRAJECTORY_START = 0` |

Default plot settings (colour limits, point sizes, loop colours and the camera of each view) are set at the top of `visuals_pumping.py`.