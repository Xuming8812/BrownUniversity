# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 20:19:45 2019

@author: xumin
"""
import numpy as np
import matplotlib.pyplot as plt
import math


x = np.linspace(-1.,5.,100)
y1= np.sin(3*x)
y2 = x**2-3*x+1.2436
y3 = x**2-3*x+2.2337
plt.ylim((-1.5, 1.5))
plt.plot(x,y1)
plt.plot(x,y2,linestyle = '--')
plt.plot(x,y3,linestyle = '--')