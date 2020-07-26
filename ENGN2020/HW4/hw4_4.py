# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 21:55:04 2019

@author: xumin
"""

import numpy as np
import matplotlib.pyplot as plt

def nelderMead():
    delta = 0.025
    
    x = y = np.arange(-6.0, 6.0, delta)
    
    X, Y = np.meshgrid(x, y)
    
    Z = 0.045*X**4-X**2+0.5*X+0.065*Y**4-Y**2+0.5*Y+0.3*X*Y
    
    Z = np.ma.array(Z)
    
    origin = 'lower'
    
    fig1, ax2 = plt.subplots(constrained_layout=True)
    
    CS = ax2.contourf(X, Y, Z, 15, cmap=plt.cm.bone, origin= origin)
    cbar = fig1.colorbar(CS) 
        
    vertices = np.array([[0.,0.],
                         [0.,1.02],
                         [-1.04,0]])

    for i in range(20):
        #plot vertices
        x1, y1 = [vertices[0,0], vertices[1,0]], [vertices[0,1], vertices[1,1]]
        x2, y2 = [vertices[1,0], vertices[2,0]], [vertices[1,1], vertices[2,1]]
        x3, y3 = [vertices[2,0], vertices[0,0]], [vertices[2,1], vertices[0,1]]
        plt.plot(x1, y1, x2, y2, x3, y3, marker = 'o')
        #plt.show()
        #check whether to stop
        z = np.zeros((3,1))
        for j in range(3):
            z[j,0] = get_f(vertices[j,0],vertices[j,1])
            
        std = np.std(z)
        
        if std<0.1:
            break
        #call function to calculate new vertices
        vertices = step_neldner(f=get_f, vertices=vertices)

    plt.show()
    
    
def get_f(x1, x2):
    return (0.045 * x1**4 - x1**2 + 0.5 * x1 + 0.065 * x2**4 - x2**2 + 0.5 * x2 + 0.3 * x1 * x2)

def wrapper(vertices):
    return step_neldner(f=get_f, vertices=vertices)

def step_neldner(f,vertices):
    #define type {type, x, y, z}
    dtype = [('index', int), ('x1', float), ('x2', float),('z',float)]
    #use an array to store input vertices
    results = np.empty(3,dtype)
    #set the element in the results
    for i in range(3):
        results[i] = (i,vertices[i,0],vertices[i,1],get_f(vertices[i,0],vertices[i,1]))
        
    #sort by z value, which will be in accent order
    results = np.sort(results, order='z')
    
    #get x0 by using best two points
    x0 = (results[0]['x1']+results[1]['x1'])/2.0
    y0 = (results[0]['x2']+results[1]['x2'])/2.0
    z0 = get_f(x0,y0)

    #use x0 and worst point x2 to get xr, x0 = x0 + alpha*(x0-x2), where alpha = 1
    xr = 2*x0-results[2]['x1']
    yr = 2*y0-results[2]['x2']
    zr = get_f(xr,yr)
    
    #if point r is better than second best, but worse than the best, just replace x2 and return the new vertices
    if zr>=results[0]['z'] and zr<results[1]['z']:
        results[2]['x1'] = xr
        results[2]['x2'] = yr
        results[2]['z'] = zr
    #if point r is better than best, need expansion
    elif zr<results[0]['z']:
        #expand the vertices by calculate point e, where xe = x0 + gamma*(xr-x0), where gamma = 2
        xe = 2*xr-x0
        ye = 2*yr-y0
        ze = get_f(xe,ye)
        
        #if ze<zr, use point e to replace x2
        if ze<zr:
            results[2]['x1'] = xe
            results[2]['x2'] = ye
            results[2]['z'] = ze
        else:
            #use xr to replace x2
            results[2]['x1'] = xr
            results[2]['x2'] = yr
            results[2]['z'] = zr
    #if zr is worse than the second worst,need contraction
    elif zr>=results[1]['z']:
        #xc = x0 + row*(x2-x0),where row = 0.5
        xc = (x0+results[2]['x1'])/2
        yc = (y0+results[2]['x2'])/2
        zc = get_f(xc,yc)
        
        if zc<results[2]['z']:
            results[2]['x1'] = xc
            results[2]['x2'] = yc
            results[2]['z'] = zc
    #shrink
    else:
        #xi = x0+sigma(xi-x0),where sigma = 0.5
       x1 =  (results[0]['x1']+results[1]['x1'])/2.0
       y1 =  (results[0]['x2']+results[1]['x2'])/2.0
       x2 =  (results[0]['x1']+results[2]['x1'])/2.0
       y2 =  (results[0]['x2']+results[2]['x2'])/2.0   
       results[1]['x1'] = x1
       results[1]['x2'] = y1
       results[1]['z'] = get_f(x1,y1)
       results[2]['x1'] = x2
       results[2]['x2'] = y2       
       results[2]['z'] = get_f(x2,y2)
       
     #sort the result in z`s order          
    results = np.sort(results, order='z')
    
    #take out the x and y coordinate
    ans = np.zeros((3,2))

    for i in range(3):
        ans[i,0] = results[i]['x1']
        ans[i,1] = results[i]['x2']

    
    return ans

nelderMead()