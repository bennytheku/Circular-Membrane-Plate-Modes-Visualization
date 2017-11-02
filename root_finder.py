# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 17:35:56 2017

@author: Ku
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
import scipy.special as scpy
import pandas as pd

"""
Find the roots of the Equation 6.8.20.
Plot the function and find the approximated position of the root of interest x0.
Get the exact value by opt.newton(y,x0).
"""

def y(x):
    n = 2
    return scpy.jv(n,x)*scpy.iv(n+1,x) + scpy.iv(n,x)*scpy.jv(n+1,x)

x = np.linspace(0.0, 100.0, 1000)
plt.plot(x,y(x)) 
plt.ylim(-100,100)
plt.axhline(y=0)

test = pd.read_excel('ka.xlsx', header=None).values[0][1]
