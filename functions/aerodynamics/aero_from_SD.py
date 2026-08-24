# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 16:10:15 2024

@author: nipynaer

INPUT: Va, alpha, beta, p, q, r, delta_a, delta_e, delta_r

OUTPUT: 

"""

#%% Imports
import numpy as np
from matplotlib import pyplot as plt
import math as m
from scipy import interpolate
from pathlib import Path

HERE = Path(__file__).resolve().parent

#%% functions
def C(C_a,alpha):
    return np.matmul(C_a,np.array([alpha**2,alpha,1],dtype=object).T)

#%% SD CFD
b = 42.47
c = 150.45/42.47

#Stability Derivatives #TODO put in aircraft data
SD = np.genfromtxt(HERE / "stabilityDerivatives_CFD_mix_woi_V80_NP.txt", skip_header = 4, delimiter = ",")

C0 =  SD[:,1]
C1 = SD[:,2]
C2 =  SD[:,3]

#main alpha contribution
CX0 = np.array([C2[0],C1[0],C0[0]])
CY0 = np.array([0,0,0])#np.array([C2[8],C1[8],C0[8]])
CZ0  = np.array([C2[16],C1[16],C0[16]])
#beta contribution
CXb   = np.array([0,0,0])#np.array([C2[1],C1[1],C0[1]])
CYb  = np.array([C2[9],C1[9],C0[9]])
CZb  = np.array([0,0,0])#np.array([C2[17],C1[17],C0[17]])
#roll contribution
CXp = np.array([0,0,0])#np.array([C2[2],C1[2],C0[2]])
CYp = np.array([C2[10],C1[10],C0[10]])
CZp  = np.array([0,0,0])#np.array([C2[18],C1[18],C0[18]])
#pitch contribution
CXq   = np.array([C2[3],C1[3],C0[3]])
CYq = np.array([0,0,0])#np.array([C2[11],C1[11],C0[11]])
CZq  = np.array([C2[19],C1[19],C0[19]])
#yaw contribution
CXr   =np.array([0,0,0]) #np.array([C2[4],C1[4],C0[4]])
CYr  = np.array([C2[12],C1[12],C0[12]])
CZr   = np.array([0,0,0])#np.array([C2[20],C1[20],C0[20]])
#aileron deflection
CXda  = np.array([0,0,0])#np.array([C2[5],C1[5],C0[5]])
CYda   = np.array([C2[13],C1[13],C0[13]])
CZda  = np.array([0,0,0])#np.array([C2[21],C1[21],C0[21]])
#elevator deflection
CXde  = np.array([C2[6],C1[6],C0[6]])
CYde = np.array([0,0,0])#np.array([C2[14],C1[14],C0[14]])
CZde = np.array([C2[22],C1[22],C0[22]])
#rudder deflection
CXdr  = np.array([0,0,0])#np.array([C2[7],C1[7],C0[7]])
CYdr = np.array([C2[15],C1[15],C0[15]])
CZdr  = np.array([0,0,0])#np.array([C2[23],C1[23],C0[23]])

#main alpha contribution
Cl0 = np.array([0,0,0])#np.array([C2[24],C1[24],C0[24]])
Cm0 = np.array([C2[32],C1[32],C0[32]])
Cn0 = np.array([0,0,0])#np.array([C2[40],C1[40],C0[40]])
#beta contribution
Clb = np.array([C2[25],C1[25],C0[25]])
Cmb = np.array([0,0,0])#np.array([C2[33],C1[33],C0[33]])
Cnb = np.array([C2[41],C1[41],C0[41]])
#roll contribution
Clp = np.array([C2[26],C1[26],C0[26]])
Cmp  = np.array([0,0,0])#np.array([C2[34],C1[34],C0[34]])
Cnp  = np.array([C2[42],C1[42],C0[42]])
#pitch contribution
Clq  =np.array([0,0,0]) #np.array([C2[27],C1[27],C0[27]])
Cmq = np.array([C2[35],C1[35],C0[35]])
Cnq = np.array([0,0,0])#np.array([C2[43],C1[43],C0[43]])
#yaw contribution
Clr  = np.array([C2[28],C1[28],C0[28]])
Cmr = np.array([0,0,0])#np.array([C2[36],C1[36],C0[36]])
Cnr = np.array([C2[44],C1[44],C0[44]])
#aileron deflection
Clda  = np.array([C2[29],C1[29],C0[29]])
Cmda = np.array([0,0,0])#np.array([C2[37],C1[37],C0[37]])
Cnda = np.array([C2[45],C1[45],C0[45]])
#elevator deflection
Clde  = np.array([0,0,0])#np.array([C2[30],C1[30],C0[30]])
Cmde = np.array([C2[38],C1[38],C0[38]])
Cnde = np.array([0,0,0])#np.array([C2[46],C1[46],C0[46]])
#rudder deflection
Cldr = np.array([C2[31],C1[31],C0[31]])
Cmdr = np.array([0,0,0])#np.array([C2[39],C1[39],C0[39]])
Cndr = np.array([C2[47],C1[47],C0[47]])



def force_coefficients_from_states(Va, alpha,beta,p, q, r, da, de, dr):
    
    #Conversion from awebox to Malz frame
    alphai = alpha
    betai = beta  #This needs to be corrected everywhere!!
    pi = -p
    qi = q
    ri = -r
    Vai = Va
    dai = da
    dei = de
    dri = dr

    Cf_0 = np.array([[C(CX0,alphai),C(CY0,alphai),C(CZ0,alphai)]]).T
    Cf_B = np.array([[C(CXb,alphai),C(CYb,alphai),C(CZb,alphai)]]).T
    Cf_pqr = np.matrix([[C(CXp,alphai),C(CXq,alphai),C(CXr,alphai)],
                     [C(CYp,alphai),C(CYq,alphai),C(CYr,alphai)],
                     [C(CZp,alphai),C(CZq,alphai),C(CZr,alphai)]])
    Cf_da = np.array([[C(CXda,alphai),C(CYda,alphai),C(CZda,alphai)]]).T
    Cf_de = np.array([[C(CXde,alphai),C(CYde,alphai),C(CZde,alphai)]]).T
    Cf_dr = np.array([[C(CXdr,alphai),C(CYdr,alphai),C(CZdr,alphai)]]).T

    pqr_norm = np.array([[b*pi/(2*Vai) ,c*qi/(2*Vai), b*ri/(2*Vai) ]]).T
        
    Cf_tot = Cf_0  + Cf_B*betai  + Cf_pqr*pqr_norm + Cf_da*dai + Cf_de*dei + Cf_dr*dri
    
    #individual contributions
    Cf_angles = Cf_0  + Cf_B*betai 
    Cf_rot = Cf_pqr*pqr_norm
    Cf_CS = Cf_da*dai + Cf_de*dei + Cf_dr*dri
    
    Cf_alpha = Cf_0 
    Cf_beta = Cf_B*betai 
    Cf_p = np.array([[C(CXp,alphai),C(CYp,alphai),C(CZp,alphai)]]).T*b*pi/(2*Vai)
    Cf_q = np.array([[C(CXq,alphai),C(CYq,alphai),C(CZq,alphai)]]).T*c*qi/(2*Vai)
    Cf_r = np.array([[C(CXr,alphai),C(CYr,alphai),C(CZr,alphai)]]).T*b*ri/(2*Vai)
    Cf_CSda = Cf_da*dai
    Cf_CSde = Cf_de*dei
    Cf_CSdr = Cf_dr*dri
    
    #Conversion from Malz to awebox frame
    Cf_tot = np.array([-Cf_tot[0,0],Cf_tot[1,0],-Cf_tot[2,0]]) 
    Cf_angles = np.array([-Cf_angles[0,0],Cf_angles[1,0],-Cf_angles[2,0]]) 
    Cf_rot  = np.array([-Cf_rot[0,0],Cf_rot [1,0],-Cf_rot [2,0]]) 
    Cf_CS  = np.array([-Cf_CS[0,0],Cf_CS[1,0],-Cf_CS[2,0]])
    
    Cf_alpha  = np.array([-Cf_alpha[0,0],Cf_alpha[1,0],-Cf_alpha[2,0]])
    Cf_beta  = np.array([-Cf_beta[0,0],Cf_beta[1,0],-Cf_beta[2,0]])
    Cf_p  = np.array([-Cf_p[0,0],Cf_p[1,0],-Cf_p[2,0]])
    Cf_q  = np.array([-Cf_q[0,0],Cf_q[1,0],-Cf_q[2,0]])
    Cf_r  = np.array([-Cf_r[0,0],Cf_r[1,0],-Cf_r[2,0]])
    Cf_CSda  = np.array([-Cf_CSda[0,0],Cf_CSda[1,0],-Cf_CSda[2,0]])
    Cf_CSde  = np.array([-Cf_CSde[0,0],Cf_CSde[1,0],-Cf_CSde[2,0]])
    Cf_CSdr  = np.array([-Cf_CSdr[0,0],Cf_CSdr[1,0],-Cf_CSdr[2,0]])
    
    
    
    return Cf_tot, Cf_angles, Cf_rot, Cf_CS, Cf_alpha, Cf_beta, Cf_p, Cf_q, Cf_r,Cf_CSda ,Cf_CSde, Cf_CSdr

def moment_coefficients_from_states(Va, alpha,beta,p, q, r, da, de, dr):

    #Conversion from awebox to Malz frame
    alphai = alpha
    betai = beta
    pi = -p
    qi = q
    ri = -r
    Vai = Va
    dai = da
    dei = de
    dri = dr
    
    Cm_0 = np.array([[C(Cl0,alphai),C(Cm0,alphai),C(Cn0,alphai)]]).T
    Cm_B = np.array([[C(Clb,alphai),C(Cmb,alphai),C(Cnb,alphai)]]).T
    Cm_pqr = np.matrix([[C(Clp,alphai),C(Clq,alphai),C(Clr,alphai)],
                     [C(Cmp,alphai),C(Cmq,alphai),C(Cmr,alphai)],
                     [C(Cnp,alphai),C(Cnq,alphai),C(Cnr,alphai)]])
    Cm_da = np.array([[C(Clda,alphai),C(Cmda,alphai),C(Cnda,alphai)]]).T
    Cm_de = np.array([[C(Clde,alphai),C(Cmde,alphai),C(Cnde,alphai)]]).T
    Cm_dr = np.array([[C(Cldr,alphai),C(Cmdr,alphai),C(Cndr,alphai)]]).T
    
    pqr_norm = np.array([[b*pi/(2*Vai) ,c*qi/(2*Vai), b*ri/(2*Vai) ]]).T
    
    #Individual contributions    
    Cm_tot = Cm_0 + Cm_B*betai  + Cm_pqr*pqr_norm + Cm_da*dai + Cm_de*dei + Cm_dr*dri
    Cm_angles = Cm_0  + Cm_B*betai 
    Cm_rot = Cm_pqr*pqr_norm
    Cm_CS = Cm_da*dai + Cm_de*dei + Cm_dr*dri
    
    Cm_alpha = Cm_0 
    Cm_beta = Cm_B*betai 
    Cm_p = np.array([[C(Clp,alphai),C(Cmp,alphai),C(Cnp,alphai)]]).T*b*pi/(2*Vai)
    Cm_q = np.array([[C(Clq,alphai),C(Cmq,alphai),C(Cnq,alphai)]]).T*c*qi/(2*Vai)
    Cm_r = np.array([[C(Clr,alphai),C(Cmr,alphai),C(Cnr,alphai)]]).T*b*ri/(2*Vai)
    Cm_CSda = Cm_da*dai
    Cm_CSde = Cm_de*dei
    Cm_CSdr = Cm_dr*dri
    
    #Conversion from Malz to awebox frame
    Cm_tot = np.array([-Cm_tot[0,0],Cm_tot[1,0],-Cm_tot[2,0]]) 
    Cm_angles = np.array([-Cm_angles[0,0],Cm_angles[1,0],-Cm_angles[2,0]]) 
    Cm_rot  = np.array([-Cm_rot[0,0],Cm_rot [1,0],-Cm_rot [2,0]]) 
    Cm_CS  = np.array([-Cm_CS[0,0],Cm_CS[1,0],-Cm_CS[2,0]]) 
    
    Cm_alpha  = np.array([-Cm_alpha[0,0],Cm_alpha[1,0],-Cm_alpha[2,0]])
    Cm_beta  = np.array([-Cm_beta[0,0],Cm_beta[1,0],-Cm_beta[2,0]])
    Cm_p  = np.array([-Cm_p[0,0],Cm_p[1,0],-Cm_p[2,0]])
    Cm_q  = np.array([-Cm_q[0,0],Cm_q[1,0],-Cm_q[2,0]])
    Cm_r  = np.array([-Cm_r[0,0],Cm_r[1,0],-Cm_r[2,0]])
    Cm_CSda  = np.array([-Cm_CSda[0,0],Cm_CSda[1,0],-Cm_CSda[2,0]])
    Cm_CSde  = np.array([-Cm_CSde[0,0],Cm_CSde[1,0],-Cm_CSde[2,0]])
    Cm_CSdr  = np.array([-Cm_CSdr[0,0],Cm_CSdr[1,0],-Cm_CSdr[2,0]])
    
    return Cm_tot, Cm_angles, Cm_rot, Cm_CS, Cm_alpha, Cm_beta, Cm_p, Cm_q, Cm_r,Cm_CSda ,Cm_CSde, Cm_CSdr



