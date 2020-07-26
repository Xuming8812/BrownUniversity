#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:29:01 2019

@author: mingxu
"""
import math
from scipy.integrate import odeint
'''
* @name: f_fit
* @description: the function to be fitted by the experimental points
* @param t: time, in form of array
* @param cp: heat capacity
* @param h: surface heat-transfer coefficient
* @return: the corresponding temperature of given t
'''  
def f_fit(t,cp,h):
    #copy the input parameter of cp and h
    alpha = cp
    beta = h
    #the pre-defined parameter
    m = 1
    a = 200
    b = 0.1
    A = 0.02
    T_inf = 25
 
    #define the function to be solved by numberial method in lamda format
    f = lambda y,t: -beta*A*(y-T_inf)/m/alpha + a * (1+ math.sin(b*t))/m/alpha

    #set the initial guess by T0
    y0 = 25
    
    #solve for temperature of given time
    results = odeint(f, y0, t)

    #resize the temperature as 1*141
    results.resize((141))
    return results

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#load the experimental data
data = np.load('thermal-block.npz')
#get time
t = data['times']
#get temperature
realTemperature = data['temperatures']
#resize the temperature as the same size with time
realTemperature.resize((141))
#curve fit to calculate cp and h
popt, pcov = curve_fit(f_fit, t, realTemperature)
#print result
print(popt)
#calculate the temperature based on fitting result
fitTemperature = f_fit(t,popt[0],  popt[1])

fig, axs = plt.subplots(1, 1)
axs.plot(t,fitTemperature,'r')
axs.plot(t,realTemperature,'bx')
axs.set_xlabel('time')
axs.set_ylabel('CA')

plt.show()