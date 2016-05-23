# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 10:45:16 2016

graphs of

@author: sebalander
"""

# %% IMPORTS
import numpy as np
import matplotlib.pyplot as plt


# %% PARAMETERS
c = 1  # light speed
v = 0.5 # object speed
l = 3  # object length
d = 1  # minimum distance to observer
d2 = d**2

# %% TRAJECTORIES
xA = np.arange(-10, 10, 0.01)
tReal = xA / v
xB = xA - l

tA = tReal + np.sqrt(xA**2 + d2)
tB = tReal + np.sqrt(xB**2 + d2)

# %% PLOT
plt.show()
plt.plot(tReal, xA, 'b', tReal, xB, 'r')
plt.xlabel('tiempo')
plt.ylabel('x')
plt.title('posiciones reales')
plt.savefig('posicionesreales.png')
plt.show()

plt.plot(tA, xA, 'b', tB, xB, 'r')
plt.xlabel('tiempo')
plt.ylabel('x')
plt.title('posiciones percibidas si v<c')
plt.savefig('posicionesVC.png')
plt.show()
