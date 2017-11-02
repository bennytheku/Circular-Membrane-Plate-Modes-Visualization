# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 14:54:07 2017

@author: Ku
"""

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import scipy.special as scpy
import os


#Calc normalization constant
def K_m(m, x0, x1, N):
    x = np.linspace(x0, x1, N)
    y = scpy.jn(m,x)
    K_m = 1.0/max(y)
    return K_m

#Get n-th root of the m-th order Bessel function of first kind
def alpha_mn(m,n):
    return scpy.jn_zeros(m,n)[-1]

"""
Visualization of the circular membrane according to:
A general procedure for thermomechanical calibration 
of nano/micro-mechanical resonators
p. 192-194 (pdf page)
"""

#Initialize
m = 1
n = 2
a = np.sqrt(2)
N = 100
r, phi = np.linspace(0, a, N), np.linspace(0, 2*np.pi, N)
R, Phi = np.meshgrid(r,phi)
X, Y = R*np.cos(Phi), R*np.sin(Phi)

alpha = alpha_mn(m,n)
K = K_m(m, 0, 10, 100)

z = alpha*R/a
psi = K*np.cos(m*Phi)*scpy.jv(m,z) #Equation (52)



#2D Colormap Plot Algorithm
directory = 'figure/circular_membrane_colormap'
if not os.path.exists(directory):
    os.makedirs(directory)
    
print('Plot in progess...')
plt.figure()
plt.title(r'$(m,n)=(' +str(m)+ ',' +str(n)+ ')$')
plt.xlim(-1, +1)
plt.ylim(-1, +1)
plt.pcolor(X,Y,psi, cmap=plt.cm.RdBu)
plt.colorbar()
plt.tight_layout()
plt.savefig(directory+ '/(m,n)=(' +str(m)+ ',' +str(n)+ ').png', bbox_inches='tight', dpi=1000)
print('Plot finished!')

#3D Surface Plot Algorithm
directory = 'figure/circular_membrane_3D'
if not os.path.exists(directory):
    os.makedirs(directory)

print('Plot in progess...')
fig = plt.figure()                  #Create the frame
ax = fig.gca(projection='3d')       #Set 3D
ax.set_title(r'$(m,n)=(' +str(m)+ ',' +str(n)+ ')$')
ax.set_xlim(-a, +a)
ax.set_ylim(-a, +a)
ax.set_zlim(-1.1,1.1)
plt.tight_layout()
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
surf = ax.plot_surface(X, Y, psi, cmap=cm.coolwarm,
                       linewidth=0, alpha=0.9, antialiased=False)
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.savefig(directory+ '/(m,n)=(' +str(m)+ ',' +str(n)+ ').png', bbox_inches='tight', dpi=1000)
print('Plot finished!')