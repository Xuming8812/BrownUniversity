#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:29:01 2019

@author: mingxu
"""
import math
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

class Derivatives:
    '''
    * @name: __init__
    * @description: the constructor of class
    * @param n: parameter of number of elements
    * @param eta: parameter of eta
    '''  
    def __init__(self,n,eta):
        self.n = n
        self.step = 1/n
        self.eta = eta
    '''
    * @name: __call__
    * @description: the call function
    * @param y: current parameter for 'theta'
    * @param t: input value of 'tao'
    * @return: dy, the value of dydt  
    '''          
    def __call__(self, y, t):      
        dy = np.zeros((self.n))
        #the boundary condition at z=0
        dy[0] = (2*y[1]-2*y[0]-2*self.step*self.eta*y[0])/self.step/self.step
        #the governing function
        for i in range(1,self.n-1):
            dy[i] = (y[i+1]- 2*y[i]+y[i-1])/self.step/self.step
        #the boundary condition at z=n-1
        dy[self.n-1] = (2*y[self.n-2]-2*y[self.n-1])/self.step/self.step
        #return dy
        return dy
        
        

'''
* @name: solve
* @description: the function to get solve the finite element problem
* @param n: the number of finite elements in the block
* @param eta: parameter of transferring heat
'''  
def solve(n,eta):
    #define a object based on input n and eta
    dydt = Derivatives(n, eta)
    #get the initial guess of y0
    y0 = np.ones((n))
    #get t
    t = np.linspace(0,10,1000)
    #solve for y
    y = odeint(dydt, y0, t)
    #show y versus t at different positions, z = 0, z=0.5, z=1
    fig, axs = plt.subplots(3, 1)
    axs[0].plot(t,y[:,0],'r')
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('theta at z = 0')
    
    axs[1].plot(t,y[:,n//2],'g')
    axs[1].set_xlabel('time')
    axs[1].set_ylabel('theta at z = 0.5')
    
    axs[2].plot(t,y[:,n-1],'b')
    axs[2].set_xlabel('time')
    axs[2].set_ylabel('theta at z = 1')    
    
    plt.show()
        
    #return y[-1]

from matplotlib import animation

fig = plt.figure()


def animate(i): 
    x = np.empty([2,y[i].shape[0]])
    x[:,:] = y[i]
    cont = plt.contourf(x)

    return cont

anim = animation.FuncAnimation(fig, animate, frames=100)


for i in range(100,10):
    x = np.empty([2,y[i].shape[0]])
    x[:,:] = y[i]
    
    cont = plt.contourf(x)
    plt.colorbar()

    plt.draw()
     
        
        
        
        
        
    
    