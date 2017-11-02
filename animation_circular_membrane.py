# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
from mpl_toolkits.mplot3d.axes3d import Axes3D
import scipy.special as scpy
from moviepy.editor import *
import os
import time

"""
Animation of the circular membrane according to:
A general procedure for thermomechanical calibration 
of nano/micro-mechanical resonators
p. 192-194 (pdf page)
"""


start_time = time.time()

#Calc normalization constant
def K_m(m, x0, x1, N):
    x = np.linspace(x0, x1, N)
    y = scpy.jn(m,x)
    K_m = 1.0/max(y)
    return K_m

#Get n-th root of the m-th order Bessel function of first kind
def alpha_mn(m,n):
    return scpy.jn_zeros(m,n)[-1]

directory = 'animation/circular_membrane'
if not os.path.exists(directory):
    os.makedirs(directory)

#INITIALIZATION
m = 0
n = 2
N = 50
a = np.sqrt(2)
r, phi = np.linspace(0, a, N), np.linspace(0, 2*np.pi, N)
R, Phi = np.meshgrid(r,phi)
X, Y = R*np.cos(Phi), R*np.sin(Phi)
alpha = alpha_mn(m,n)
K = K_m(m, 0, 10, 100)

#PLOT SETUP
fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection='3d')
plt.tight_layout()
    
def animation(t):
    z = alpha*R/a
    Psi = K*np.cos(m*Phi)*scpy.jv(m,z)*np.sin(t) #Equation (52)
    
    ax.cla()
    ax.set_zlim(-1.1,1.1)
    ax.set_title(r'Circular Membrane: $(m,n)=(' +str(m)+ ',' +str(n)+ ')$')
    ax.plot_surface(X, Y, Psi, rstride=1, cstride=1, cmap="jet",
                           vmin=-1, vmax=1, label="test", linewidth=0)
    print('Progress: ' +str(np.round(100*t/(2*np.pi),2))+ '%')
    print('Time: ' +str(np.round(time.time()-start_time))+ ' sec')

#ANIMATION AS MP4
anim = ani.FuncAnimation(fig, animation, np.linspace(0, 2*np.pi, 80))
plt.rcParams['animation.ffmpeg_path'] = 'C:/FFMPEG/bin/ffmpeg.exe'
anim.save('animation/circular_membrane/(m,n)=(' +str(m)+ ',' +str(n)+ ').mp4', dpi=100, fps=20)

#CONVERT ANIMATION TO GIF
directory = 'animation/circular_membrane'
clip = (VideoFileClip(directory+ '/(m,n)=(' +str(m)+ ',' +str(n)+ ').mp4'))
clip.write_gif(directory+ '/(m,n)=(' +str(m)+ ',' +str(n)+ ').gif')