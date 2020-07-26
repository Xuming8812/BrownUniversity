# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 21:36:46 2019

@author: xumin
"""
import numpy as np
import matplotlib.pyplot as plt
import math
    
def drawCircle():
    x = np.linspace(-50, 50,1000)
    y = np.sin(x)-x/10
    y1 = 2000*y/((x-8.4232)*(x+7.0681)*(x-2.8523))
    
    #plt.axis('equal')
    #get axes of the plot
    ax = plt.gca()
    
    plt.xlim((-50, 50))
    plt.ylim((-2.5, 2.5))
    #set the top and right boundary to none
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    #set the xaxis as the bottom boundary
    ax.xaxis.set_ticks_position('bottom')
    # set the yaxis as the left boundary
    ax.yaxis.set_ticks_position('left')
    # set the (0,0) as the position of left and bottom position
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    #draw plot
    plt.plot(x,y)
    plt.plot(x,y1)
    
def getX(x):
    a = np.sin(x)-x/10.
    b = np.cos(x)-0.1
    return x-a/b

def func(x):
    return np.sin(x)-x/10
