# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 12:17:51 2017

@author: Ku
"""

from __future__ import unicode_literals, print_function, division
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
from mpl_toolkits.mplot3d.axes3d import Axes3D
import pandas as pd
import scipy.special as scpy
import os
import time
from moviepy.editor import *

start_time = time.time()

"""
Animation of the circular plate according to:
06_PlateTheory_08_Vibrations.pdf

See root_finder.py for the roots of Equation 6.8.20
Get ka values from the excel sheet ka.xlsx
"""

directory = 'animation/circular_plate'
if not os.path.exists(directory):
    os.makedirs(directory)

#INITIALIZATION
n = 2   #n-th order of Bessel Function
i = 4   #i-th root of Bessel Function 
ka = pd.read_excel('ka.xlsx', header=None).values[n][i]
a = np.sqrt(2)
k = ka/a
N = 50     #Array size
r, phi = np.linspace(0, a, N), np.linspace(0, 2*np.pi, N)
R, Phi = np.meshgrid(r,phi)
X, Y = R*np.cos(Phi), R*np.sin(Phi)

#jv: Bessel Function of first kind
#iv: Modified Bessel Fuction of first kind
#Equation 6.8.21
#Normalization
w = (scpy.jv(n,k*r) - (scpy.jv(n,ka)/scpy.iv(n,ka)) * scpy.iv(n,k*r))
A_bar = 1.0/max(w)


fig = plt.figure()
ax = fig.add_subplot(1,1,1, projection='3d')
plt.tight_layout()

    
def animation(t):
    W = A_bar*(scpy.jv(n,k*R) - (scpy.jv(n,ka)/scpy.iv(n,ka)) * scpy.iv(n,k*R))*np.sin(t)
    
    ax.cla()
    ax.set_zlim(-1.1,1.1)
    ax.set_title(r'Circular Plate: $(n,i)=(' +str(n)+ ',' +str(i)+ ')$')
    ax.plot_surface(X, Y, W, rstride=1, cstride=1, cmap="jet",
                           vmin=-1, vmax=1, label="test", linewidth=0)
    print('Progress: ' +str(np.round(100*t/(2*np.pi),2))+ '%')
    print('Time: ' +str(np.round(time.time()-start_time))+ ' sec')

anim = ani.FuncAnimation(fig, animation, np.linspace(0, 2*np.pi, 80))
plt.rcParams['animation.ffmpeg_path'] = 'C:/FFMPEG/bin/ffmpeg.exe'
anim.save('animation/circular_plate/(n,i)=(' +str(n)+ ',' +str(i)+ ').mp4', dpi=100, fps=20)

directory = 'animation/circular_plate'
clip = (VideoFileClip(directory+ '/(n,i)=(' +str(n)+ ',' +str(i)+ ').mp4'))
clip.write_gif(directory+ '/(n,i)=(' +str(n)+ ',' +str(i)+ ').gif')