#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 11:35:25 2026

@author: niels
"""

import numpy as np
import math as m
import csv
import os

#%% Transformation matrices
def Rx(theta):
    return np.array([[ 1, 0           , 0           ],
                      [ 0, m.cos(theta),-m.sin(theta)],
                      [ 0, m.sin(theta), m.cos(theta)]])

def Ry(theta):
    return np.array([[ m.cos(theta), 0, m.sin(theta)],
                      [ 0           , 1, 0           ],
                      [-m.sin(theta), 0, m.cos(theta)]])

def Rz(theta):
    return np.array([[ m.cos(theta), -m.sin(theta), 0 ],
                      [ m.sin(theta), m.cos(theta) , 0 ],
                      [ 0           , 0            , 1 ]])

#%% Awebox read function
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

#%% Get awebox flight data
def get_awebox_data():
    path = os.getcwd()
    fname = path + "/outputs_megawes_trajectory_cfd_results.csv"
    if not os.path.exists(fname):
        print("ERROR: File is missing. Exit.")
        #exit()
    else:
        data = csv2dict(fname)
        
    #position
    x= np.array(data['x_q10_0'])
    y= np.array(data['x_q10_1'])
    z= np.array(data['x_q10_2'])
    
    #velocity
    vx= data['x_dq10_0']
    vy= data['x_dq10_1']
    vz= data['x_dq10_2']
    
    #angular velocity
    om_x = data['x_omega10_0']
    om_y = data['x_omega10_1']
    om_z = data['x_omega10_2']
    
    # attitude
    phi = data['x_r10_0']
    theta = data['x_r10_1']
    psi = data['x_r10_2']
    
    #aero
    alpha = np.array(data['outputs_aerodynamics_alpha1_0'])
    beta = np.array(data['outputs_aerodynamics_beta1_0'])
    
    return x,y,z,vx,vy,vz,om_x,om_y,om_z,phi,theta,psi,alpha,beta