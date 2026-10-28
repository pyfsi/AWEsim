"""
read_awebox_results.py
    1. Read CSV data from awebox trajectory optimization output file.
    2. Retrieve data dict and plot motion quantities and attitude.
author: Thomas Haas, UGent
last edit: 10/01/23
"""

# Imports
import os
import csv
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
#from scipy.spatial.transform import Rotation as R

# TODO
# This script also outputs the initial conditions (IC.out) (to be used later)
# Cleanup script

#%% Definitions
def csv2dict(fname):

    # read csv file
    with open(fname, 'r') as f:
        reader = csv.DictReader(f)

        # get fieldnames from DictReader object and store in list
        headers = reader.fieldnames

        # store data in columns
        columns = {}
        for row in reader:
            for fieldname in headers:
                val = row.get(fieldname).strip('[]')
                if val == '':
                    val = '0.0'
                columns.setdefault(fieldname, []).append(float(val))

    # add periodicity
    for fieldname in headers:
        columns.setdefault(fieldname, []).insert(0, columns[fieldname][-1])
    columns['time'][0] = 0.0

    return columns

def plot_trajectory(data_list,name_list,color_list):
    ax = plt.figure(1).add_subplot(projection='3d')
    ax.set_title("Trajectory")
    # n = 1.5
    # ax.set_xlim(0, 450*n)
    # ax.set_ylim(-225*n,225*n)
    # ax.set_zlim(0, 450*n)
    ax.set_xlim(0, 1000)
    ax.set_ylim(-500,500)
    ax.set_zlim(0,1000)
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.set_zlabel('z [m]')
    
    for i in np.arange(len(data_list)):
        data = data_list[i]
        color = color_list[i]
        name = name_list[i]
        
        P = data['outputs_performance_p_current_0']
        zerolist = np.zeros(len(P))
        x = np.array(data['x_q10_0'])
        y = np.array(data['x_q10_1'])
        z = np.array(data['x_q10_2'])
        
        ax.plot(x,y,z,color = color, label = name) 
        #ax.plot(x, z, color = 'grey', zdir='y', zs=500)  #projection
        #ax.plot(y, z, color = 'grey', zdir='x', zs=1000)
        #ax.plot(x[P<zerolist ],y[P<zerolist ],z[P<zerolist ],'.', color = 'red', markersize = 2) #points trajectory with - power
        ax.plot(x[0],y[0],z[0], '*', color = color) #startpoint
        ax.legend()
        print(f"Initial coordinates: x = {x[0]}, y = {y[0]}, z = {z[0]}")

def plot_motion(data_list,name_list,color_list):

    # Create figure
    fig, ax = plt.subplots(3,3)
    fig.suptitle('Motion (translational)')
    
    for i in np.arange(len(data_list)):
        data = data_list[i]
        color = color_list[i]
        name = name_list[i]
        
        Tl = np.array(data['time'])[-1]
        zmin = data['zmin']
        ylim = data['ylim']
        amax = data['amax']
    
        # Add data
        for i in range(3):
            ax[i,0].plot(data['time']/Tl, data['x_q10_' + str(i)], color = color, label = name)
            ax[i,1].plot(data['time']/Tl, data['x_dq10_' + str(i)],color = color, label = name)
            ax[i,2].plot(data['time']/Tl, data['outputs_xdot_from_var_ddq10_' + str(i)],color = color, label = name)
            ax[i,2].hlines([-amax,amax],0,1, linestyle='--', color = color)
        
        # Add bounds
        ax[2,0].hlines([zmin],0,1, linestyle='--', color = color)
        ax[1,0].hlines([-ylim,ylim],0,1, linestyle='--', color = color)
            
        # Add labels
        import string
        for i, k in zip(range(3), list(string.ascii_lowercase[-3:])):
            ax[i,0].set_ylabel(r'$'+k+'\,[\mathrm{m}]$', fontsize=12)
            ax[i,1].set_ylabel(r'$\dot{'+k+'}\,[\mathrm{m}/\mathrm{s}]$', fontsize=12)
            ax[i,2].set_ylabel(r'$\ddot{'+k+'}\,[\mathrm{m}/\mathrm{s2}]$', fontsize=12)
    
        ax[2,0].set_xlabel(r'$t/Tl\,[-]$', fontsize=12)
        ax[2,1].set_xlabel(r'$t/Tl\,[-]$', fontsize=12)
        ax[2,2].set_xlabel(r'$t/Tl\,[-]$', fontsize=12)
        ax[2,2].legend()
    

    
    return fig

def plot_rotation(data_list,name_list,color_list):

    # Create figure
    fig, ax = plt.subplots(3,2)
    fig.suptitle('Motion (rotational)')
    
    for i in np.arange(len(data_list)):
        data = data_list[i]
        color = color_list[i]
        name = name_list[i]
        
        Tl = np.array(data['time'])[-1]
        omega_bound = data['omega_bound']
    
        # Add data
        for i in range(3):
            R_i = (180.0 / np.pi) * np.array(data['x_r10_' + str(i)])
            omega_i = (180.0 / np.pi) * np.array(data['x_omega10_' + str(i)])
            ax[i,0].plot(data['time']/Tl, R_i, color = color, label = name)
            ax[i,1].plot(data['time']/Tl, omega_i, color = color, label = name)
        
            print(f"Initial euler angles: {['Rx','Ry','Rz'][i]} = {R_i[0]}")
        
        # Add bounds
        for i in range(3):
            ax[i,1].hlines([-omega_bound,omega_bound],0,1, linestyle='--', color = color)
            
        # Add labels
        import string
        for i, k in zip(range(3), list(string.ascii_lowercase[-3:])):
            ax[i,0].set_ylabel(r'$R_{'+k+'}\,[\deg]$', fontsize=12)
            ax[i,1].set_ylabel(r'$\omega_{'+k+'}\,[\deg/\mathrm{s}]$', fontsize=12)
    
        ax[2,0].set_xlabel(r'$t/Tl\,[-]$', fontsize=12)
        ax[2,1].set_xlabel(r'$t/Tl\,[-]$', fontsize=12)
        ax[2,1].legend()
    

    return fig

def plot_control_AC(data_list,name_list,color_list):
    
    # Create figure
    fig, ax = plt.subplots(3,2)
    fig.suptitle('Control aircraft')
    
    for i in np.arange(len(data_list)):
        data = data_list[i]
        color = color_list[i]
        name = name_list[i]
        
        Tl = np.array(data['time'])[-1]
        delta_max = data['delta_max'] 
        ddelta_max = data['ddelta_max'] 
    
        # Add data
        for i in range(3):
            ax[i,0].plot(data['time']/Tl, (180.0 / np.pi) *np.array(data['x_delta10_' + str(i)]), color = color, label = name)
            ax[i,1].plot(data['time']/Tl, (180.0 / np.pi) *np.array(data['u_ddelta10_' + str(i)]), color = color, label = name)
            print(f"Initial control deflections [rad]: {['ail','ele','rud'][i]} = {np.array(data['x_delta10_' + str(i)])[0]}")
        
        # Add bounds
        for i in range(3):
            ax[i,0].hlines([-delta_max,delta_max],0,1, linestyle='--', color = color)
            ax[i,1].hlines([-ddelta_max,ddelta_max],0,1, linestyle='--', color = color)
            
        # Add labels
        import string
        for i, k in zip(range(3), list(string.ascii_lowercase[-3:])):
            ax[i,0].set_ylabel(r'$\delta_{'+k+'}\,[\deg]$', fontsize=12)
            ax[i,1].set_ylabel(r'$\dot{\delta}_{'+k+'}\,[\deg/\mathrm{s}]$', fontsize=12)
    
        ax[2,0].set_xlabel(r'$t/Tl\,[-]$', fontsize=12)
        ax[2,1].set_xlabel(r'$t/Tl\,[-]$', fontsize=12)
        ax[2,1].legend()
    

    return fig

def plot_control_tether(data_list,name_list,color_list):
    # Create figure
    fig, ax = plt.subplots(3,1)
    fig.suptitle('Control tether')
    
    for i in np.arange(len(data_list)):
        data = data_list[i]
        color = color_list[i]
        name = name_list[i]
    
        Tl = np.array(data['time'])[-1]
        l_t_min = data['l_t_min']
        l_t_max = data['l_t_max'] 
        dl_t_min = data['dl_t_min'] 
        dl_t_max = data['dl_t_max']
        ddl_t_max= data['ddl_t_max'] 
        
        #Add data
        ax[0].plot(data['time']/Tl, data['x_l_t_0'], color = color, label = name)
        ax[1].plot(data['time']/Tl, data['x_dl_t_0'], color = color, label = name)
        ax[2].plot(data['time']/Tl, data['u_ddl_t_0'], color = color, label = name)
        
        #Add bounds
        ax[0].hlines([l_t_min,l_t_max],0,1, linestyle='--', color = color)
        ax[0].set_ylim([0,1000])
        ax[1].hlines([dl_t_min,dl_t_max],0,1, linestyle='--', color = color)
        ax[1].hlines([0],0,1, linestyle='--', color = 'black')
        ax[2].hlines([-ddl_t_max,ddl_t_max],0,1, linestyle='--', color = color)
        
        #Add labels
        ax[0].set_ylabel(r'l_t_0 [m]', fontsize=12)
        ax[1].set_ylabel(r'dl_t_0 [m/s]', fontsize=12)
        ax[2].set_ylabel(r'ddl_t_0 [m/s2]', fontsize=12)
        ax[2].set_xlabel(r't/Tl [-]', fontsize=12)
        ax[2].legend()
    
    return fig

def plot_aero(data_list,name_list,color_list):
    
    # Create figure
    fig, ax = plt.subplots(3,2)
    fig.suptitle('Aerodynamics')
    
    for i in np.arange(len(data_list)):
        data = data_list[i]
        color = color_list[i]
        name = name_list[i]
        
        Tl = np.array(data['time'])[-1]
        airspeed_min = data['airspeed_min'] 
        airspeed_max = data['airspeed_max']
        alpha_min = data['alpha_min'] 
        alpha_max = data['alpha_max']
        beta_min = data['beta_min'] 
        beta_max = data['beta_max']
        
        #Add data
        ax[0,0].plot(data['time']/Tl, data['outputs_aerodynamics_airspeed1_0'], '* ', color = color, label = name)
        ax[1,0].plot(data['time']/Tl, data['outputs_aerodynamics_alpha_deg1_0'], color = color, label = name)
        ax[2,0].plot(data['time']/Tl, data['outputs_aerodynamics_beta_deg1_0'], color = color, label = name)
        ax[0,1].plot(data['time']/Tl, data['outputs_aerodynamics_CL1_0'], color = color, label = name)
        ax[1,1].plot(data['time']/Tl, data['outputs_aerodynamics_CD1_0'], color = color, label = name)
        ax[2,1].plot(data['time']/Tl, data['outputs_aerodynamics_CY1_0'], color = color, label = name)
        
        #Add bounds
        #ax[0,0].hlines([airspeed_min,airspeed_max],0,1, linestyle='--', color = color)
        #ax[1,0].hlines([alpha_min,alpha_max],0,1, linestyle='--', color = color)
        #ax[2,0].hlines([beta_min,beta_max],0,1, linestyle='--', color = color)
        
        #Add labels
        ax[0,0].set_ylabel(r'airspeed [m/s]', fontsize=12)
        ax[1,0].set_ylabel(r'alpha [deg]', fontsize=12)
        ax[2,0].set_ylabel(r'beta [deg]', fontsize=12)
        ax[0,1].set_ylabel(r'CL []', fontsize=12)
        ax[1,1].set_ylabel(r'CD []', fontsize=12)
        ax[2,1].set_ylabel(r'CY []', fontsize=12)
        ax[2,0].set_xlabel(r't/Tl [-]', fontsize=12)
        ax[2,1].set_xlabel(r't/Tl [-]', fontsize=12)
        ax[2,1].legend()
    
    return fig

def plot_forces(data_list,name_list,color_list):
    # Create figure
    fig, ax = plt.subplots(4)
    fig.suptitle('Forces')
    
    for i in np.arange(len(data_list)):
        data = data_list[i]
        color = color_list[i]
        name = name_list[i]
        
        Tl = np.array(data['time'])[-1]
        Ftether_max = data['Ftether_max'] 
        Ftether_min = data['Ftether_min']
    
        # Add data
        for i in range(3):
            ax[i].plot(data['time']/Tl,np.array(data['outputs_aerodynamics_f_aero_earth1_' + str(i)])/1e3, color = color, label = name)
        ax[3].plot(data['time']/Tl, np.array(data['outputs_local_performance_tether_force10_0'])/1e3, color = color, label = name)
        
        # Add bounds
        ax[3].hlines([Ftether_min/1e3,Ftether_max/1e3],0,1, linestyle='--', color = color)
    
        # Add labels
        import string
        for i, k in zip(range(3), list(string.ascii_lowercase[-3:])):
            ax[i].set_ylabel(r'$F_{'+k+'}\,[kN]$', fontsize=12)
        ax[3].set_ylabel(r'$F_{tether}\,[kN]$', fontsize=12)
        ax[3].set_xlabel(r'$t/Tl\, [-]$', fontsize=12)
        ax[3].legend()

    return fig

def plot_performance(data_list,name_list,color_list):
    # Create figure
    fig, ax = plt.subplots(2)
    fig.suptitle('Performance')
    
    for i in np.arange(len(data_list)):
        data = data_list[i]
        color = color_list[i]
        name = name_list[i]
        
        Tl = np.array(data['time'])[-1]
        P_avg = np.average(np.array(data['outputs_performance_p_current_0']))
        
        #Add data
        #ax[0].plot(data['time']/Tl, np.array(data['outputs_performance_p_current_0'])/(1000*P_avg), color = color, label = name)
        ax[0].plot(data['time']/Tl, np.array(data['outputs_performance_p_current_0'])/1e6, color = color, label = name)
        
        #Add bounds
        #ax[0].hlines([P_avg/P_avg],0,1, linestyle='--', color = color)
        #ax[0].hlines([0],0,1, linestyle='-', color = color)
        ax[0].hlines([P_avg/1e6],0,1, linestyle='--', color = color)
        #ax[0].hlines([0],0,1, linestyle='-', color = color)
        
        #Add labels
        # ax[0].set_ylabel(r'Pnorm [-]', fontsize=12)
        # ax[0].set_xlabel(r't/Tl [-]', fontsize=12)
        ax[0].set_ylabel(r'P [MW]', fontsize=12)
        ax[0].set_xlabel(r't/Tl [-]', fontsize=12)
        ax[0].grid(True)
        ax[0].legend()

    return fig


#%% Input
path = os.getcwd()
fname = path + "/outputs_megawes_trajectory_cfd_results.csv"
if not os.path.exists(fname):
    print("File is missing. Exit.")
    # exit()
else:
    data = csv2dict(fname)
    
#add bounds to data
data['zmin'] = 40
data['omega_bound'] = 10 #p
data['delta_max'] = 10 #elevator rudder
data['ddelta_max'] = 50
data['l_t_min'] = 10
data['l_t_max'] = 10000 
data['dl_t_min'] = -15
data['dl_t_max'] = 15
data['ddl_t_max'] = 2.5
data['airspeed_min'] = 10
data['airspeed_max'] = 120
data['alpha_min'] = -14.5
data['alpha_max'] = 4.2
data['beta_min'] = -10
data['beta_max'] =  10
data['Ftether_max'] =  1700000
data['Ftether_min'] =  50
data['P_avg'] = 1
data['ylim'] = 1
data['amax'] = 3*9.81

outputs_megawes_trajectory_cfd_results= data

#%% collect trajectories
data_list = [ outputs_megawes_trajectory_cfd_results]
name_list = [  'outputs_megawes_trajectory_cfd_results']
color_list = [ 'blue']

plt.close('all')

fig0 = plot_trajectory(data_list,name_list,color_list)
fig1 = plot_motion(data_list,name_list,color_list)
fig2 = plot_rotation(data_list,name_list,color_list)
fig3 = plot_control_AC(data_list,name_list,color_list)
#fig4 = plot_control_tether(data_list,name_list,color_list)
fig5 = plot_aero(data_list,name_list,color_list)
fig6 = plot_forces(data_list,name_list,color_list)
fig7 = plot_performance(data_list,name_list,color_list)

plt.show()

