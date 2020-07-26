#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 19:06:01 2019

@author: mingxu
"""

import numpy as np
from scipy.interpolate import interp1d
#from matplotlib import pyplot
import math
import scipy.stats

# The below creates an interpolation function, get_energy(r).
data = np.load(r'/Users/mingxu/Desktop/2020/ENGN2020/HW9/h2-data.npz')
get_energy = interp1d(data['bondlengths'], data['energies'],
fill_value=(np.inf, 0.), bounds_error=False)
#fig, ax = pyplot.subplots()
#ax.plot(data['bondlengths'], data['energies'], 'o')
#ls = np.linspace(0., data['bondlengths'][-1] * 1.1, num=1000)
#es = [get_energy(_) for _ in ls]
#ax.plot(ls, es, 'r-')
#ax.set_xlabel('bond length, $\AA$')
#ax.set_ylabel('energy, eV')
#fig.savefig('interp.pdf')

def metropolis(initial_guess = 0.5,T = 1500, steps = 500,maxStep = 0.1):
    accept = 0
        
    kb = 1.38064852e-23
    
    evToJ = 1.60218e-19
    
    l_old = initial_guess
    
    result = np.zeros((steps))
    
    means = np.zeros((steps))
    
    stds = np.zeros((steps))
    
    acceptNums = np.zeros((steps))
    
    for i in range(steps):
        #get energy of old l
        El_old = get_energy(l_old)
        #random jump to a new l
        l_new = l_old+np.random.uniform(-1,1)*maxStep
        #get the energy of new l
        El_new = get_energy(l_new)

        #calculate r by two energy, note that r is for logP
        r = -(El_new-El_old)*evToJ/kb/T
            
        #if P(new)>P(old)
        if r>0:
            #save new l
            accept = accept + 1
            l_old = l_new
            result[i] = l_new
        else:
            #generate a new random value from [0,1]
            prob = np.random.uniform(0,1)
            #see if the we accept the new step
            if math.exp(r) > prob:
                accept = accept + 1
                l_old = l_new
                result[i] = l_new
            else:
                result[i] = l_old
                
        #get min
        current = result[:i+1]
        
        current_mean = np.mean(current)
        means[i] = current_mean
        #get std
        
        current_std = np.std(current)
        stds[i] = current_std
        
        #get accept ratio
        acceptNums[i] = accept/(i+1)
                
    return result,means,stds,acceptNums
            
    
result,means,stds,acceptNums = metropolis(initial_guess = 0.5)

steps = np.linspace(0,499,500)   

import matplotlib.pyplot as plt

#plt.hist(a, bins='auto')     

#plt.plot(steps,means)

result,means,stds,acceptNums = metropolis(initial_guess = 0.5,maxStep = 1)
fig, ax = plt.subplots()
ax.plot(steps,means)
ax.set_xlabel('Step number')
ax.set_ylabel('Average of l')
        
    
    
    