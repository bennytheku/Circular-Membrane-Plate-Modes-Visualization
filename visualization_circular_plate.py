# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 09:56:30 2017

@author: Ku
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import scipy.special as scpy
import pandas as pd
import os
import time

start_time = time.time()

"""
Visualization of the circular plate according to:
06_PlateTheory_08_Vibrations.pdf

See root_finder.py for the roots of Equation 6.8.20
Get ka values from the excel sheet ka.xlsx
"""

#INITIALIZATION
n = 0   #n-th order of Bessel Function
i = 1   #i-th root of Eq. 6.8.20
ka = pd.read_excel('ka.xlsx', header=None).values[n][i]
a = np.sqrt(2)
k = ka/a
N = 100     #Array size
r, phi = np.linspace(0, a, N), np.linspace(0, 2*np.pi, N)
R, Phi = np.meshgrid(r,phi)
X, Y = R*np.cos(Phi), R*np.sin(Phi)


#jv: Bessel Function of first kind
#iv: Modified Bessel Fuction of first kind
#Equation 6.8.21
w = (scpy.jv(n,k*r) - (scpy.jv(n,ka)/scpy.iv(n,ka)) * scpy.iv(n,k*r))
A_bar = 1.0/max(w)  #Normalization
W = A_bar*(scpy.jv(n,k*R) - (scpy.jv(n,ka)/scpy.iv(n,ka)) * scpy.iv(n,k*R))

#2D Colormap Plot Algorithm
directory = 'figure/circular_plate_colormap'
if not os.path.exists(directory):
    os.makedirs(directory)
    
print('Plot in progess...')
plt.figure()
plt.title(r'$(n,i)=(' +str(n)+ ',' +str(i)+ ')$')
plt.xlim(-1, +1)
plt.ylim(-1, +1)
plt.pcolor(X,Y,W, cmap=plt.cm.RdBu)
plt.colorbar()
plt.tight_layout()
plt.savefig(directory+ '/(n,i)=(' +str(n)+ ',' +str(i)+ ').png', bbox_inches='tight', dpi=1000)
print('Plot finished!')
print('Time: ' +str(np.round(time.time()-start_time))+ ' sec')

#3D Surface Plot Algorithm
directory = 'figure/circular_plate_3D'
if not os.path.exists(directory):
    os.makedirs(directory)

print('Plot in progess...')
fig = plt.figure()                  #Create the frame
ax = fig.gca(projection='3d')       #Set 3D
ax.set_title(r'$(n,i)=(' +str(n)+ ',' +str(i)+ ')$')
ax.set_xlim(-a, +a)
ax.set_ylim(-a, +a)
ax.set_zlim(-1.1,1.1)
plt.tight_layout()
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
surf = ax.plot_surface(X, Y, W, cmap=cm.coolwarm,
                       linewidth=0, alpha=0.9, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.savefig(directory+ '/(n,i)=(' +str(n)+ ',' +str(i)+ ').png', bbox_inches='tight', dpi=1000)
print('Plot finished!')
print('Time: ' +str(np.round(time.time()-start_time))+ ' sec')