# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 14:11:51 2019

@author: xumin
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

'''
* @name: get_NoisyF_Sigma
* @description: return a function based the input sigma
* @param y: the input value, in format of [CA,T]
* @return: list, [dCA/dt,dT/dt]
'''  
def get_NoisyF_Sigma(sigma):
    a = sigma
    v = lambda x: (0.045 * x[0]**4 - x[0]**2 + 0.5 * x[0] + 0.065 * x[1]**4 - x[1]**2 + 0.5 * x[1] + 0.3 * x[0] * x[1])+np.random.normal(0,a)
    return v
'''
* @name: getDiff
* @description: return a function based the input sigma
* @param y: the input value, in format of [CA,T]
* @return: list, [dCA/dt,dT/dt]
'''  
def getDiff(x):
    diff1 = 0.18*x[0]*x[0]*x[0]-2*x[0]+0.5+0.3*x[1]
    diff2 = 0.26*x[1]*x[1]*x[1]-2*x[1]+0.5+0.3*x[0]
    return np.array([diff1,diff2])
'''
* @name: NoisyTest
* @description: get the result based on different sigmas
'''  
def NoisyTest():
    localMinima = np.array([[-3.63460063, 2.91071661],
                            [3.43582195, -3.0972582],
                            [-3.25733016, -2.64544543],
                            [2.98019805, 2.31968217]])
    count1 = []
    count2 = []
    sigma = np.linspace(0, 5, 11)
    
   
    vertices = np.array([[0.,0.],
                         [0.,1],
                         [-1,0]])
    for item in sigma:
        cur_count1 = 0
        cur_count2 = 0
        
        for i in range(1000):
            
            a = get_NoisyF_Sigma(item)
            
            res = minimize(a,[-0.3,0.3],method = 'BFGS',jac = getDiff)
                
            #res = minimize(a,[-0.3,0.3],method = 'Nelder-Mead',tol=0.00001,options={'initial_simplex':vertices})
                 
            result = res.x
            
            distance = []
            
            for j in range(4):
                temp = (result[0]-localMinima[j][0])**2+(result[1]-localMinima[j][1])**2
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
    print(count1)
    print(count2)
    
    return count1,count2

a,b = NoisyTest()
print(a)
print(b)