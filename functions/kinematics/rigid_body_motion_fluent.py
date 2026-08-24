import numpy as np

# TODO: 
# Clean-up 
# Aircraft control surfaces axis hardcoded; get from megawes.py

def rigid_body_motion_fluent(CFD_DIR, time_step, q, qdot, R, omega_ac_vec, delta_dot):

    # TODO: check why timestep + 1
    # TODO: discretization

    omega_ac_vec_E = np.matmul(R, omega_ac_vec)  # body to earth frame
    omega_ac = np.linalg.norm(omega_ac_vec_E)
    omega_ac_axis = omega_ac_vec_E / omega_ac

    #%% MOVE_ZONE_WING
    omega_w = omega_ac
    axis_w = omega_ac_axis
    origin_w = q
    velocity_w = qdot

    #Write data
    data = np.array([[omega_w], [axis_w[0]], [axis_w[1]], [axis_w[2]], [origin_w[0]], [origin_w[1]], [origin_w[2]], [velocity_w[0]], [velocity_w[1]],[velocity_w[2]]])
    file_name = f'{CFD_DIR}/move_zone_wing_update_timestep{time_step+1}.dat'
    np.savetxt(file_name, data, fmt='%27.17e', header='', comments='')

    def move_zone_CS(delta_dot_CS,hingepos_CS,hingeaxis_CS):
        # angular velocity
        omega_CS_vec = omega_ac_vec_E  + np.matmul(R, delta_dot_CS*hingeaxis_CS)  # transpose to earth frame first
        omega_CS = np.linalg.norm(omega_CS_vec)
        axis_CS = omega_CS_vec / omega_CS

        # translational velocity
        velocity_CS =  qdot + np.matmul(R, np.cross(hingepos_CS, delta_dot_CS*hingeaxis_CS))
        origin_CS = q  # origin: position aircraft

        return omega_CS, axis_CS, origin_CS, velocity_CS


    #MOVE_ZONE_ELEVATOR
    delta_e = delta_dot[1]
    #delta_e = 0.3
    hingeaxis_e = np.array([0, 1, 0])  # body frame
    hingepos_e = np.array([9.73, 0, -0.229])
    omega_e, axis_e, origin_e, velocity_e = move_zone_CS(delta_e, hingepos_e, hingeaxis_e)

    #Write data
    data = np.array(
        [[omega_e], [axis_e[0]], [axis_e[1]], [axis_e[2]], [origin_e[0]], [origin_e[1]], [origin_e[2]], [velocity_e[0]], [velocity_e[1]],
         [velocity_e[2]]])
    file_name = f'{CFD_DIR}/move_zone_elevator_update_timestep{time_step+1}.dat'
    np.savetxt(file_name, data, fmt='%27.17e', header='', comments='')

    # #MOVE_ZONE_RUDDER_LEFT
    delta_rl = -delta_dot[2]
    #delta_rl = 0.3
    hingeaxis_rl = np.array([0, 0, 1])  # body frame
    hingepos_rl = np.array([9.73, -3.8, 0])
    omega_rl, axis_rl, origin_rl, velocity_rl = move_zone_CS(delta_rl, hingepos_rl, hingeaxis_rl)

    #Write data
    data = np.array([[omega_rl], [axis_rl[0]], [axis_rl[1]], [axis_rl[2]], [origin_rl[0]], [origin_rl[1]], [origin_rl[2]], [velocity_rl[0]], [velocity_rl[1]], [velocity_rl[2]]])
    file_name = f'{CFD_DIR}/move_zone_rudder_left_update_timestep{time_step+1}.dat'
    np.savetxt(file_name, data, fmt='%27.17e', header='', comments='')

    #MOVE_ZONE_RUDDER_RIGHT
    delta_rr = -delta_dot[2]
    #delta_rr = 0
    hingeaxis_rr = np.array([0, 0, 1])  # body frame
    hingepos_rr = np.array([9.73, 3.8, 0])
    omega_rr, axis_rr, origin_rr, velocity_rr = move_zone_CS(delta_rr, hingepos_rr, hingeaxis_rr)

    #Write data
    data = np.array([[omega_rr], [axis_rr[0]], [axis_rr[1]], [axis_rr[2]], [origin_rr[0]], [origin_rr[1]], [origin_rr[2]], [velocity_rr[0]], [velocity_rr[1]], [velocity_rr[2]]])
    file_name = f'{CFD_DIR}/move_zone_rudder_right_update_timestep{time_step+1}.dat'
    np.savetxt(file_name, data, fmt='%27.17e', header='', comments='')

    #MOVE_ZONE_AILERON_LEFT
    delta_al = -delta_dot[0]
    #delta_al = 0
    hingeaxis_al = np.array([0.532, 7.07, 0.057]) / np.sqrt(0.532 ** 2 + 7.07 ** 2 + 0.057 ** 2)  # body frame
    hingepos_al = np.array([2.742 - 1.67, -13.17, 0.186 - 0.229])
    omega_al, axis_al, origin_al, velocity_al = move_zone_CS(delta_al, hingepos_al, hingeaxis_al)

    #write data
    data = np.array([[omega_al], [axis_al[0]], [axis_al[1]], [axis_al[2]], [origin_al[0]], [origin_al[1]], [origin_al[2]], [velocity_al[0]], [velocity_al[1]], [velocity_al[2]]])
    file_name = f'{CFD_DIR}/move_zone_aileron_left_update_timestep{time_step+1}.dat'
    np.savetxt(file_name, data, fmt='%27.17e', header='', comments='')

    #MOVE_ZONE_AILERON_RIGHT
    delta_ar = -delta_dot[0]
    #delta_ar = 0
    hingeaxis_ar = np.array([0.532, -7.07, 0.057]) / np.sqrt(0.532 ** 2 + 7.07 ** 2 + 0.057 ** 2)  # body frame
    hingepos_ar = np.array([2.742 - 1.67, 13.17, 0.186 - 0.229])
    omega_ar, axis_ar, origin_ar, velocity_ar = move_zone_CS(delta_ar, hingepos_ar, hingeaxis_ar)

    #write data
    data = np.array([[omega_ar], [axis_ar[0]], [axis_ar[1]], [axis_ar[2]], [origin_ar[0]], [origin_ar[1]], [origin_ar[2]], [velocity_ar[0]], [velocity_ar[1]],[velocity_ar[2]]])
    file_name = f'{CFD_DIR}/move_zone_aileron_right_update_timestep{time_step+1}.dat'
    np.savetxt(file_name, data, fmt='%27.17e', header='', comments='')

    return
