# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 09:57:03 2024

@author: nipynaer
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

#%% Settings
timestep = 1000
timestep_awe = timestep - 1
sim = "trac"
plt.close('all')

#%% Functions
def get_cfd_data(name,timestep):
    data = np.genfromtxt(name + f"{timestep:04d}" , delimiter=',',skip_header= 1)
    x = data[:,1]
    y = data[:,2]
    z = data[:,3]
    var = data[:,4]
    return x,y,z,var

def rotate_scale_translate_point(x, y, X, Y, theta, scale, Xoffset, Yoffset): #source: ChatGPT
    # Translate point to the origin (relative to the center point)
    translated_x = x - X
    translated_y = y - Y

    # Apply the rotation matrix
    rotated_x = translated_x * np.cos(theta) - translated_y * np.sin(theta)
    rotated_y = translated_x * np.sin(theta) + translated_y * np.cos(theta)

    # Translate the point back
    final_x = scale*(rotated_x + X) + Xoffset
    final_y = scale*(rotated_y + Y) + Yoffset

    return final_x, final_y


def nearest_neighbor_interpolation(X1, Y1, Z1, P1, X2, Y2, Z2):
    # Combine X1, Y1, Z1 into a single array of points
    points1 = np.array([X1, Y1, Z1]).T
    # Combine X2, Y2, Z2 into a single array of target points
    points2 = np.array([X2, Y2, Z2]).T

    # Create a KDTree for the original grid points
    tree = cKDTree(points1)
    
    # For each point in the new grid, find the nearest point in the original grid
    dist, indices = tree.query(points2)

    # Use the indices to map pressure values from P1 to the new grid
    P2 = P1[indices]

    return P2

#%% state
#MPC data
x_u_mpc = np.genfromtxt('data/states_controls_' + sim + ".out", delimiter = ",") 
time_mpc = x_u_mpc[:,0]
q10_x_mpc = x_u_mpc[:,1]
q10_y_mpc = x_u_mpc[:,2]
q10_z_mpc = x_u_mpc[:,3]
dq10_x_mpc = x_u_mpc[:,4]
dq10_y_mpc = x_u_mpc[:,5]
dq10_z_mpc = x_u_mpc[:,6]
r10_1_mpc = x_u_mpc[:,10]
r10_2_mpc = x_u_mpc[:,11]
r10_3_mpc = x_u_mpc[:,12]
r10_4_mpc = x_u_mpc[:,13]
r10_5_mpc = x_u_mpc[:,14]
r10_6_mpc = x_u_mpc[:,15]
r10_7_mpc = x_u_mpc[:,16]
r10_8_mpc = x_u_mpc[:,17]
r10_9_mpc = x_u_mpc[:,18]

q = np.array([q10_x_mpc[timestep_awe],q10_y_mpc[timestep_awe],q10_z_mpc[timestep_awe]])  #position timestep_awe  
dq = np.array([dq10_x_mpc[timestep_awe],dq10_y_mpc[timestep_awe],dq10_z_mpc[timestep_awe]])  #position timestep_awe  
R = np.array([[r10_1_mpc[timestep_awe],r10_2_mpc[timestep_awe],r10_3_mpc[timestep_awe]],[r10_4_mpc[timestep_awe],r10_5_mpc[timestep_awe],r10_6_mpc[timestep_awe]],[r10_7_mpc[timestep_awe],r10_8_mpc[timestep_awe],r10_9_mpc[timestep_awe]]]).reshape(3,3) #Attitude timestep i

#%% Import aircraft nodes

# Fluent data
x_pres, y_pres, z_pres, pressure = get_cfd_data('data_pressure_' + sim + '/pressure_wing-', timestep)
x_pres_ailr, y_pres_ailr, z_pres_ailr, pressure_ailr = get_cfd_data('data_pressure_' + sim + '/pressure_aileron_right-', timestep)
x_pres_aill, y_pres_aill, z_pres_aill, pressure_aill = get_cfd_data('data_pressure_' + sim + '/pressure_aileron_left-', timestep)
x_pres_tipl, y_pres_tipl, z_pres_tipl, pressure_tipl = get_cfd_data('data_pressure_' + sim + '/pressure_wingtip_left-', timestep)
x_pres_tipr, y_pres_tipr, z_pres_tipr, pressure_tipr = get_cfd_data('data_pressure_' + sim + '/pressure_wingtip_right-', timestep)   

# Transform from global to local wind frame coordinates
q_pres = np.array([x_pres-q[0],y_pres-q[1],z_pres-q[2]]) 
q_pres_ailr = np.array([x_pres_ailr-q[0],y_pres_ailr-q[1],z_pres_ailr-q[2]])
q_pres_aill = np.array([x_pres_aill-q[0],y_pres_aill-q[1],z_pres_aill-q[2]])
q_pres_tipr = np.array([x_pres_tipr-q[0],y_pres_tipr-q[1],z_pres_tipr-q[2]])
q_pres_tipl = np.array([x_pres_tipl-q[0],y_pres_tipl-q[1],z_pres_tipl-q[2]])

# Merge Tips (w/o aileron)
# q_pres = np.concatenate((q_pres,  q_pres_tipl ,  q_pres_tipr), axis=1)    
# pressure = np.concatenate((pressure, pressure_tipl , pressure_tipr ), axis=0)
#with aileron
q_pres = np.concatenate((q_pres, q_pres_aill, q_pres_ailr,   q_pres_tipl ,  q_pres_tipr), axis=1)    
pressure = np.concatenate((pressure, pressure_aill , pressure_ailr, pressure_tipl , pressure_tipr ), axis=0)        

# Step1 : Body frame
q_pres = np.matmul(R,q_pres)


#%% Step2: Recreate the wing: 
ny = 100 #number of spanwise divisions

#aircraft properties
yt = 21.235 #halfspan
yr = 4.65 #span to constant cors
cr = 4.4640 #root chord
ct = 2.11 #tip chord
cref = 150.45/42.47
tr = 5 #twist root
tt = 0 #wist tip
xLEr = 0 #leading edge offset root
xLEt = -0.56 #leading edge offset tip
    
y_list = np.linspace(-yt,yt,ny)

#chord distribution
def c_y(y):
    y = abs(y)
    if y <= yr:
        return cr
    else:
        return cr + (ct - cr) / (yt - yr) * (y - yr)
c_list = [c_y(y) for y in y_list]   

#twist distribution
def t_y(y):
    y = abs(y)
    if y <= yr:
        return tr
    else:
        return tr + (tt - tr) / (yt - yr) * (y - yr)
t_list = [t_y(y) for y in y_list] 

#leading edge offset distribution
def xLE_y(y):
    y = abs(y)
    if y <= yr:
        return xLEr
    else:
        return xLEr + (1/4) * (ct - cr) / (yt - yr) * (y - yr)
xLE_list = [xLE_y(y) for y in y_list]  

#airfoil 
airfoil = np.genfromtxt('Mrev-v2.txt')
nd = 31
x_ss_base = airfoil[:nd,0][::-1]
z_ss_base = airfoil[:nd,1][::-1]
x_ps_base = airfoil[nd-1:,0]
z_ps_base = airfoil[nd-1:,1]

# scale, rotate, translate: which order?

x_ss_list = np.array([])
y_ss_list = np.array([])
z_ss_list = np.array([])
x_ps_list = np.array([])
y_ps_list = np.array([])
z_ps_list = np.array([])


for yi in y_list:
    ci = c_y(yi)
    ti = t_y(yi)
    xLEi = xLE_y(yi)
    
    Xoffset = -xLEi - 1.6729
    Yoffset = -0.2294
    
    x_ss, z_ss = rotate_scale_translate_point(x_ss_base, z_ss_base, 0, 0, -np.deg2rad(ti), ci, Xoffset, Yoffset) #Counterclockwise positive, this order in meshing tool, but rotation around LE
    x_ps, z_ps = rotate_scale_translate_point(x_ps_base, z_ps_base, 0, 0, -np.deg2rad(ti), ci, Xoffset, Yoffset) #Counterclockwise positive
    
    x_ss_list = np.append(x_ss_list, x_ss)
    y_ss_list = np.append(y_ss_list, yi*np.ones(len(x_ss)))
    z_ss_list = np.append(z_ss_list, z_ss)
    x_ps_list = np.append(x_ps_list, x_ps)
    y_ps_list = np.append(y_ps_list, yi*np.ones(len(x_ps)))
    z_ps_list = np.append(z_ps_list, z_ps)


#%%Step 3: Map pressure onto new grid: find nearest neighbour
pressure_mapped_ss = nearest_neighbor_interpolation(q_pres[0], q_pres[1], q_pres[2],  pressure,  x_ss_list, y_ss_list, z_ss_list)
pressure_mapped_ps = nearest_neighbor_interpolation(q_pres[0], q_pres[1], q_pres[2],  pressure,  x_ps_list, y_ps_list, z_ps_list)

#%%Step 4: Calculate cl distribution along span

Vw = np.array([(0.3828883453000257/0.4187)*np.log((q[2]+0.0002)/0.0002), 0, 0])
Vk = np.array([dq[0],dq[1],dq[2]])
Va = np.linalg.norm(Vk - Vw)
p_dyn = 0.5*1.225*Va**2

cx_distribution = []
cz_distribution = []
cx_ss_distribution = []
cz_ss_distribution = []
cx_ps_distribution = []
cz_ps_distribution = []

for i in np.arange(int(len(y_list))):
    y_section = y_list[i]
    
    #ss LE --> TE
    x_ss_section = x_ss_list[i*nd : (i+1)*nd]
    z_ss_section = z_ss_list[i*nd : (i+1)*nd]
    P_ss_section = pressure_mapped_ss[i*nd: (i+1)*nd]
    
    c = np.sqrt((x_ss_section[-1] - x_ss_section[0])**2 + (z_ss_section[-1] - z_ss_section[0])**2)
    dx = x_ss_section[1:] - x_ss_section[:-1] 
    dz = z_ss_section[1:] - z_ss_section[:-1] 
    ds = np.sqrt(dx**2 + dz**2)
    theta =  np.arctan2(dz,dx) #np.arctan(dz/dx) #np.arctan(dx/dz)
    P = (P_ss_section[1:] + P_ss_section[:-1])/2
    fx_ss = np.sum(P*np.sin(theta)*ds)
    fz_ss = -np.sum(P*np.cos(theta)*ds)
    cx_ss = fx_ss/(p_dyn*c)
    cz_ss = fz_ss/(p_dyn*c)
    
    #ps: LE --> TE
    x_ps_section = x_ps_list[i*nd : (i+1)*nd]
    z_ps_section = z_ps_list[i*nd : (i+1)*nd]
    P_ps_section = pressure_mapped_ps[i*nd: (i+1)*nd]
    
    c = np.sqrt((x_ps_section[-1] - x_ps_section[0])**2 + (z_ps_section[-1] - z_ps_section[0])**2)
    dx = x_ps_section[1:] - x_ps_section[:-1] 
    dz = z_ps_section[1:] - z_ps_section[:-1] 
    ds = np.sqrt(dx**2 + dz**2)
    theta =  np.arctan(dz/dx) #np.arctan(dx/dz)
    P = (P_ps_section[1:] + P_ps_section[:-1])/2
    fx_ps = -np.sum(P*np.sin(theta)*ds)
    fz_ps = np.sum(P*np.cos(theta)*ds)
    cx_ps = fx_ps/(p_dyn*c)
    cz_ps = fz_ps/(p_dyn*c)    

    
    cx_ps_distribution.append(cx_ps)
    cz_ps_distribution.append(cz_ps)
    cx_ss_distribution.append(cx_ss)
    cz_ss_distribution.append(cz_ss)
    cx_distribution.append(cx_ps + cx_ss)
    cz_distribution.append(cz_ps + cz_ss)


plt.figure(6)
plt.plot(y_list,cz_distribution, label = 'total')
plt.plot(y_list,cz_ss_distribution, label = 'ss')
plt.plot(y_list,cz_ps_distribution, label = 'ps')
plt.legend()

plt.figure(7)
plt.plot(y_list,cx_distribution, label = 'total')
plt.plot(y_list,cx_ss_distribution, label = 'ss')
plt.plot(y_list,cx_ps_distribution, label = 'ps')
plt.legend()

Cx = np.average(cx_distribution)
Cz = np.average(cz_distribution)

print('Cx: ')
print(Cx)
print('Cz: ')
print(Cz)

#%% plots


lim = 15

# Compare grids
# Configure plot
ax = plt.figure(1,figsize=(5,3)).add_subplot(projection='3d' )
ax.set_title("Compare grids")

ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(-lim, lim)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_zlabel('z [m]')
ax.elev = 90
ax.azim =  0 #-180 - 30
#ax.grid(False)
#ax.set_axis_off()
ax.w_xaxis.set_pane_color(color = 'white')
ax.w_yaxis.set_pane_color(color = 'white')
ax.w_zaxis.set_pane_color(color = 'white')

ax.scatter(x_ss_list, y_ss_list , z_ss_list,  c = 'red', s = 3) 
ax.scatter(x_ps_list, y_ps_list , z_ps_list,  c = 'red', s = 3)

ax.scatter(q_pres[0], q_pres[1], q_pres[2],  c = 'black', s = 3) 

#Pressure distribution Fluent
ax = plt.figure(2,figsize=(5,3)).add_subplot(projection='3d' )
ax.set_title("Pressure distribution Fluent")
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(-lim, lim)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_zlabel('z [m]')
ax.elev = 90
ax.azim =  0 #-180 - 30
#ax.grid(False)
#ax.set_axis_off()
ax.w_xaxis.set_pane_color(color = 'white')
ax.w_yaxis.set_pane_color(color = 'white')
ax.w_zaxis.set_pane_color(color = 'white')

pressure_scatter = ax.scatter(q_pres[0], q_pres[1], q_pres[2],  c = pressure/1000 ,s = 10e-1, cmap='coolwarm', vmin = -9, vmax = 5 ) #pressure #s = 10e-1
colorbar_pressure = plt.figure(1).colorbar(pressure_scatter, location = 'right')
colorbar_pressure.set_label('Static pressure [kPa]')
time = timestep*0.005
ax.text2D(0.05, 0.95, "Time = " + f"{time:0.2f}" + "s", fontsize=12, ha='center',transform=ax.transAxes)

#Pressure distribution Mapped
ax = plt.figure(3,figsize=(5,3)).add_subplot(projection='3d' )
ax.set_title("Pressure distribution Mapped")
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(-lim, lim)
ax.set_xlabel('x [m]')
ax.set_ylabel('y [m]')
ax.set_zlabel('z [m]')
ax.elev = 90
ax.azim =  0 #-180 - 30
#ax.grid(False)
#ax.set_axis_off()
ax.w_xaxis.set_pane_color(color = 'white')
ax.w_yaxis.set_pane_color(color = 'white')
ax.w_zaxis.set_pane_color(color = 'white')

pressure_scatter = ax.scatter(x_ss_list, y_ss_list , z_ss_list,  c = pressure_mapped_ss/1000 ,s = 10e-1, cmap='coolwarm', vmin = -9, vmax = 5 ) #pressure #s = 10e-1
colorbar_pressure = plt.figure(1).colorbar(pressure_scatter, location = 'right')
pressure_scatter = ax.scatter(x_ps_list, y_ps_list , z_ps_list,  c = pressure_mapped_ps/1000 ,s = 10e-1, cmap='coolwarm', vmin = -9, vmax = 5 ) #pressure #s = 10e-1

colorbar_pressure.set_label('Static pressure [kPa]')
time = timestep*0.005
ax.text2D(0.05, 0.95, "Time = " + f"{time:0.2f}" + "s", fontsize=12, ha='center',transform=ax.transAxes)

#Plot lift distribution

plt.show()
