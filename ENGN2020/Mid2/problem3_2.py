# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:25:31 2019

@author: xumin
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def get_f(x1, x2, sigma):
    return (0.045 * x1**4 - x1**2 + 0.5 * x1 + 0.065 * x2**4 - x2**2 + 0.5 * x2 + 0.3 * x1 * x2)+np.random.normal(0,sigma)

def step_neldner(f,vertices,sigma):
    #define type {type, x, y, z}
    dtype = [('index', int), ('x1', float), ('x2', float),('z',float)]
    #use an array to store input vertices
    results = np.empty(3,dtype)
    #set the element in the results
    for i in range(3):
        results[i] = (i,vertices[i,0],vertices[i,1],get_f(vertices[i,0],vertices[i,1],sigma))
        
    #sort by z value, which will be in accent order
    results = np.sort(results, order='z')
    
    #get x0 by using best two points
    x0 = (results[0]['x1']+results[1]['x1'])/2.0
    y0 = (results[0]['x2']+results[1]['x2'])/2.0
    z0 = get_f(x0,y0,sigma)

    #use x0 and worst point x2 to get xr, x0 = x0 + alpha*(x0-x2), where alpha = 1
    xr = 2*x0-results[2]['x1']
    yr = 2*y0-results[2]['x2']
    zr = get_f(xr,yr,sigma)
    
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
        ze = get_f(xe,ye,sigma)
        
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
        zc = get_f(xc,yc,sigma)
        
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
       results[1]['z'] = get_f(x1,y1,sigma)
       results[2]['x1'] = x2
       results[2]['x2'] = y2       
       results[2]['z'] = get_f(x2,y2,sigma)
       
     #sort the result in z`s order          
    results = np.sort(results, order='z')
    
    #take out the x and y coordinate
    ans = np.zeros((3,2))

    for i in range(3):
        ans[i,0] = results[i]['x1']
        ans[i,1] = results[i]['x2']

    
    return ans

def nelderMead(sigma):
    delta = 0.025
    
    x = y = np.arange(-6.0, 6.0, delta)
    
    X, Y = np.meshgrid(x, y)
    
    Z = 0.045*X**4-X**2+0.5*X+0.065*Y**4-Y**2+0.5*Y+0.3*X*Y
    
    Z = np.ma.array(Z)
    
#    origin = 'lower'
#    
#    fig1, ax2 = plt.subplots(constrained_layout=True)
#    
#    CS = ax2.contourf(X, Y, Z, 15, cmap=plt.cm.bone, origin= origin)
#    cbar = fig1.colorbar(CS) 
        
    vertices = np.array([[0.,0.],
                         [0.,1],
                         [-1,0]])
    
    minValue = -10000
    finalX = 0
    finalY = 0

    for i in range(50):
        #plot vertices
        x1, y1 = [vertices[0,0], vertices[1,0]], [vertices[0,1], vertices[1,1]]
        x2, y2 = [vertices[1,0], vertices[2,0]], [vertices[1,1], vertices[2,1]]
        x3, y3 = [vertices[2,0], vertices[0,0]], [vertices[2,1], vertices[0,1]]
        #plt.plot(x1, y1, x2, y2, x3, y3, marker = 'o')
        #plt.show()
        #check whether to stop
        z = np.zeros((3,1))
        for j in range(3):
            z[j,0] = get_f(vertices[j,0],vertices[j,1],sigma)
            
        std = np.std(z)
        
        if std<0.1:
            minValue= np.mean(z)
            finalX = (vertices[0,0]+vertices[1,0]+vertices[2,0])/3
            finalY = (vertices[0,1]+vertices[1,1]+vertices[2,1])/3
            break

        #call function to calculate new vertices
        vertices = step_neldner(f=get_f, vertices=vertices,sigma=sigma)

#    plt.show()
    
    return {'min':minValue,'x':finalX,'y':finalY}


def NoisyTest():
    localMinima = np.array([[-3.63460063, 2.91071661],
                            [-3.25733016, -2.64544543],
                            [3.43582195, -3.0972582],
                            [2.98019805, 2.31968217]])
    count1 = []
    count2 = []
    sigma = np.linspace(0, 5, 11)
    for item in sigma:
        cur_count1 = 0
        cur_count2 = 0
        
        for i in range(1000):
            result = nelderMead(item)
            
            distance = []
            
            for j in range(4):
                temp = (result['x']-localMinima[j][0])**2+(result['y']-localMinima[j][1])**2
                distance.append(temp)
            
            if distance[0] < 1:
                cur_count1 = cur_count1+1
                cur_count2 = cur_count2+1
            elif distance[1]<1 or distance[2]<1 or distance[3]<1:
                cur_count2 = cur_count2+1
        
        count1.append(cur_count1)
        count2.append(cur_count2)
                
            
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(sigma,count1)
    axs[0].set_xlabel('sigma')
    axs[0].set_ylabel('same local minima')
    
    axs[1].plot(sigma,count2)
    axs[1].set_xlabel('sigma')
    axs[1].set_ylabel('any local minima')
    
    fig.tight_layout()
    plt.show()
    #print(count1)
    #print(count2)
    
    return count1,count2


a,b=NoisyTest()