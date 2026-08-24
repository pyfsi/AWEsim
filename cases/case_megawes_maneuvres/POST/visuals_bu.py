# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 10:45:13 2023

@author: nipynaer
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
# import math as m
# import os
# import csv
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.colors import TwoSlopeNorm
# from matplotlib.collections import LineCollection
# from mpl_toolkits.mplot3d import Axes3D, art3d
# from matplotlib.colors import LinearSegmentedColormap

from functions.postprocessing.create_video import create_video

#TODO
# Add friction and delete other
# Add lift_distribution
# Voor I enkel center gebruiken? fijnere punten

# Settings
flow_property = "P"  # (P) pressure, (CP) pressurecoefficient, (F) friction, (V) velocity, (N) Nothing
view = "I2" # (I) inerial1, (I2) inertial2 (camera fixed at cg), (B) body, (A) aerodynamic
SIM = "_test_main2"

# File directions
FILE_DIR = Path(__file__).resolve().parent
CASE_DIR = FILE_DIR.parent
SIM_DIR = CASE_DIR / "SIM_test_rates2"

#%% Get CFD data
def get_cfd_data(name,timestep):
    data = np.genfromtxt(name + f"{timestep:04d}" , delimiter=',',skip_header= 1) #nodenumber,x-coordinate,y-coordinate, z-coordinate,pressure ,pressure-coefficient, velocity-magnitude, x-velocity, y-velocity, z-velocity, wall-shear, x-wall-shear, y-wall-shear, z-wall-shear
    x = data[:,1]
    y = data[:,2]
    z = data[:,3]
    pressure = data[:,4]
    cp = data[:,5]
    V = data[:,6]
    Vx= data[:,7]
    Vy = data[:,8]
    Vz = data[:,9]
    shear = data[:,10]
    shearx = data[:,11]
    sheary = data[:,12]
    shearz = data[:,13]
    return x,y,z,pressure, cp,V,Vx,Vy,Vz,shear,shearx,sheary,shearz


#%% Main function
def plot_timestep(timestep):
    
    #%% Collect data
    ## Retrieve CFD data of the different aircraft components
    x_wing,y_wing,z_wing,pressure_wing,cp_wing,V_wing,Vx_wing,Vy_wing,Vz_wing,shear_wing,shearx_wing,sheary_wing,shearz_wing = get_cfd_data(str(SIM_DIR) + "/CFD/Results/data_wing-", timestep)
    x_ht,y_ht,z_ht,pressure_ht,cp_ht,V_ht,Vx_ht,Vy_ht,Vz_ht,shear_ht,shearx_ht,sheary_ht,shearz_ht = get_cfd_data(str(SIM_DIR) + "/CFD/Results/data_tail-", timestep)
    x_vtl,y_vtl,z_vtl,pressure_vtl,cp_vtl,V_vtl,Vx_vtl,Vy_vtl,Vz_vtl,shear_vtl,shearx_vtl,sheary_vtl,shearz_vtl = get_cfd_data(str(SIM_DIR) + "/CFD/Results/data_vtail_left-", timestep)
    x_vtr ,y_vtr ,z_vtr ,pressure_vtr ,cp_vtr ,V_vtr ,Vx_vtr ,Vy_vtr ,Vz_vtr ,shear_vtr ,shearx_vtr ,sheary_vtr ,shearz_vtr = get_cfd_data(str(SIM_DIR) + "/CFD/Results/data_vtail_right-", timestep)
    x_ailr ,y_ailr ,z_ailr ,pressure_ailr ,cp_ailr ,V_ailr ,Vx_ailr ,Vy_ailr ,Vz_ailr ,shear_ailr ,shearx_ailr ,sheary_ailr ,shearz_ailr = get_cfd_data(str(SIM_DIR) + "/CFD/Results/data_aileron_right-", timestep)
    x_aill,y_aill,z_aill,pressure_aill,cp_aill,V_aill,Vx_aill,Vy_aill,Vz_aill,shear_aill,shearx_aill,sheary_aill,shearz_aill  = get_cfd_data(str(SIM_DIR) + "/CFD/Results/data_aileron_left-", timestep)
    x_tipl,y_tipl,z_tipl,pressure_tipl,cp_tipl,V_tipl,Vx_tipl,Vy_tipl,Vz_tipl,shear_tipl,shearx_tipl,sheary_tipl,shearz_tipl = get_cfd_data(str(SIM_DIR) + "/CFD/Results/data_wingtip_left-", timestep)
    x_tipr,y_tipr,z_tipr,pressure_tipr,cp_tipr,V_tipr,Vx_tipr,Vy_tipr,Vz_tipr,shear_tipr,shearx_tipr,sheary_tipr,shearz_tipr = get_cfd_data(str(SIM_DIR) + "/CFD/Results/data_wingtip_right-", timestep)
    x_aic,y_aic,z_aic,pressure_aic,cp_aic,V_aic,Vx_aic,Vy_aic,Vz_aic,shear_aic,shearx_aic,sheary_aic,shearz_aic = get_cfd_data(str(SIM_DIR) + "/CFD/Results/data_aircraft_c-", timestep)
   
    ## Merge data
    x = np.concatenate((x_wing, x_ht, x_vtl, x_vtr, x_ailr, x_aill, x_tipl, x_tipr, x_aic), axis = 0)
    y = np.concatenate((y_wing, y_ht, y_vtl, y_vtr, y_ailr, y_aill, y_tipl, y_tipr, y_aic), axis = 0)
    z = np.concatenate((z_wing, z_ht, z_vtl, z_vtr, z_ailr, z_aill, z_tipl, z_tipr, z_aic), axis = 0)
    pressure = np.concatenate((pressure_wing, pressure_ht, pressure_vtl, pressure_vtr, pressure_ailr, pressure_aill, pressure_tipl, pressure_tipr, pressure_aic), axis = 0)
    cp = np.concatenate((cp_wing, cp_ht, cp_vtl, cp_vtr, cp_ailr, cp_aill, cp_tipl, cp_tipr, cp_aic), axis = 0)
    V = np.concatenate((V_wing, V_ht, V_vtl, V_vtr, V_ailr, V_aill, V_tipl, V_tipr, V_aic), axis = 0)
    Vx = np.concatenate((Vx_wing, Vx_ht, Vx_vtl, Vx_vtr, Vx_ailr, Vx_aill, Vx_tipl, Vx_tipr, Vx_aic), axis = 0)
    Vy = np.concatenate((Vy_wing, Vy_ht, Vy_vtl, Vy_vtr, Vy_ailr, Vy_aill, Vy_tipl, Vy_tipr, Vy_aic), axis = 0)
    Vz = np.concatenate((Vz_wing, Vz_ht, Vz_vtl, Vz_vtr, Vz_ailr, Vz_aill, Vz_tipl, Vz_tipr, Vz_aic), axis = 0)
    shear = np.concatenate((shear_wing, shear_ht, shear_vtl, shear_vtr, shear_ailr, shear_aill, shear_tipl, shear_tipr, shear_aic), axis = 0)
    shearx = np.concatenate((shearx_wing, shearx_ht, shearx_vtl, shearx_vtr, shearx_ailr, shearx_aill, shearx_tipl, shearx_tipr, shearx_aic), axis = 0)
    sheary = np.concatenate((sheary_wing, sheary_ht, sheary_vtl, sheary_vtr, sheary_ailr, sheary_aill, sheary_tipl, sheary_tipr, sheary_aic), axis = 0)
    shearz = np.concatenate((shearz_wing, shearz_ht, shearz_vtl, shearz_vtr, shearz_ailr, shearz_aill, shearz_tipl, shearz_tipr, shearz_aic), axis = 0)
        
    ## DYN data: states
    x_u = np.genfromtxt(SIM_DIR / "states.out", delimiter = ",")
    time = x_u[:,0]
    q10_x = x_u[:,1]
    q10_y = x_u[:,2]
    q10_z = x_u[:,3]
    dq10_vx = x_u[:,4]
    dq10_vy = x_u[:,5]
    dq10_vz = x_u[:,6]
    r10_1 = x_u[:,10]
    r10_2 = x_u[:,11]
    r10_3 = x_u[:,12]
    r10_4 = x_u[:,13]
    r10_5 = x_u[:,14]
    r10_6 = x_u[:,15]
    r10_7 = x_u[:,16]
    r10_8 = x_u[:,17]
    r10_9 = x_u[:,18]
    
    i = timestep - 1 #WHY -1 ??
    qi = np.array([[q10_x[i]],[q10_y[i]],[q10_z[i]]])  #position timestep i
    r10i = np.array([[r10_1[i],r10_2[i],r10_3[i]],[r10_4[i],r10_5[i],r10_6[i]],[r10_7[i],r10_8[i],r10_9[i]]]).reshape(3,3) #attitude timestep i
    
    ## DYN data: aerodynamics
    # Vwi = np.array([(1.212260663819277/0.4187)*np.log((q10_z[i]+0.1)/0.1), 0, 0])  #HARDCODED WIND
    # Vi = np.array([dq10_vx[i],dq10_vy[i],dq10_vz[i]])
    # Vai = Vi - Vwi
    # Vai_b = np.matmul(r10i,Vai) #earth to body
    # alphai =  (Vai_b[2] / Vai_b[0])
    # betai =  (Vai_b[1] / Vai_b[0])
    # #betai = 0 #ONLY SEE EFFECT ALPHA
    # RAi = np.matmul(Rz(-betai),Ry(alphai))   #transformation body to aerodynamic TODO:CHECK
    
    #%% Post-process and plot
    plt.close('all')
    
    #TODO maak dit een eenvoudige functie om meerdere keren te gebruiken
    #%% View == "I2" and flow_property == "P"
    if view == "I2" and flow_property == "P":
          
        # Transform from global to local wind frame coordinates
        q_nodes = np.array([[x-qi[0]],[y-qi[1]],[z-qi[2]]])

        # Configure plot
        ax = plt.figure(figsize=(10,6)).add_subplot(projection='3d' )
        #ax.set_title("Local " + axis + " frame")
        lim = 15
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(-lim, lim)
        ax.set_xlabel('x [m]')
        ax.set_ylabel('y [m]')
        ax.set_zlabel('z [m]')
        ax.elev = 30
        ax.azim =  0 #-180 - 30
        ax.grid(False)
        ax.set_axis_off()
        
        # Plot
        pressure_scatter = ax.scatter(q_nodes[0], q_nodes[1], q_nodes[2],  c = pressure/1000 ,s = 5, cmap='coolwarm', vmin = -20, vmax = 9) #pressure #s = 10e-1 %Previous bounds; [-9,5]
        ax.plot(q10_x - qi[0], q10_y - qi[1], q10_z - qi[2] , linestyle = 'dotted', color = 'grey') #reference trajectory
        ax.plot(q10_x[:timestep] - qi[0], q10_y[:timestep] - qi[1], q10_z[:timestep] - qi[2] , color = 'purple') #trajectory
        #ax.plot([0,-float(qi[0])],[0,-float(qi[1])],[0,-float(qi[2])], linewidth=1, color="black") #tether
        
        #colorbar_pressure = plt.figure(1).colorbar(pressure_scatter, location = 'bottom')
        #colorbar_pressure.set_label('Static pressure [kPa]')
        time = timestep*0.01
        ax.text2D(0.05, 0.95, "Time = " + f"{time:0.2f}" + "s", fontsize=12, ha='center',transform=ax.transAxes)
    
        # Save
        plt.tight_layout()
        plt.show()
        
    


## Single timestep
Save = True
timestep = int(350) 
plot_timestep(timestep)
if Save:
    plt.tight_layout()
    plt.savefig('Animations/Animation_main/Pressure_' + f"{timestep:04d}" + '.png',dpi = 600)
    print('Saved Figure' + f"{timestep:04d}" + '.png' )
    plt.show()

#
# Animation
#

# Loop timesteps and create figures/frames
# timesteps = np.arange(5,405,5)
# for timestep in timesteps:  
#     plot_timestep(int(timestep))
#     plt.tight_layout()
#     plt.savefig('Animations/Animation_main/Pressure_' + f"{timestep:04d}" + '.png',dpi = 600)
#     print('Saved Figure' + f"{timestep:04d}" + '.png' )
#     plt.show()

# Create video from frames
# create_video(
#     input_folder="Animations/Animation_main",
#     output_file="Animations/Animation_main/Pressure.mp4",
#     prefix="Pressure_",
#     start=5,
#     stop=405,
#     step=5,
#     fps=20,
# )