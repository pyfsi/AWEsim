# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 13:35:05 2022

@author: nipynaer
"""

import numpy as np
import matplotlib.pyplot as plt


y = np.linspace(0.5,800,1000)

#paper 1
# y0 = 0.5 #0.1
# vw_ref = 10 #5
# yref= 403 #10

#paper 2
# y0 = 0.0002 #0.1
# vw_ref = 12 #5
# yref= 100 #10

#AWEV 2026
y0 = 0.1 #0.1
vw_ref = 20 #5
yref= 100 #10


Vw_awebox = vw_ref*np.log(y/y0)/np.log(yref/y0)

#fluent
#y0 = 0.5
#u_star =  0.62554
KAPPA = 0.4187
C1 = -0.04
C2 = 0.53
Cmu = 0.09

u_star = KAPPA*vw_ref/np.log(yref/y0)

Vw = u_star/KAPPA*np.log((y+y0)/y0)

# k = u_star**2/np.sqrt(Cmu)*np.sqrt(C1*np.log((y+y0)/y0)+C2)
# om = u_star/(KAPPA*np.sqrt(Cmu))*1/(y+y0)

plt.close('all')
plt.figure(1)
plt.plot(Vw,y, label = "fluent")
plt.plot(Vw_awebox,y , label = "awebox")

plt.legend()

