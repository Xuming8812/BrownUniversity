# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 22:06:39 2019

@author: xumin
"""
import math

def getYPrime(y):
    return 2*(1+y**2)

def getYPrime2(x,y):
    return x*y*y

def getY(x):
    return math.tan(2*x)

def getY2(x):
    return -1/(0.5*x*x-1)

def ImprovedEulerMethod(x0,y0,h,steps):
    yn = [y0]
    xn = [x0]
    
    yExact = [y0]
  
    for i in range(steps):
       
        #get xn
        x = xn[-1]+h
              
        #get predictor
        #k1 = h*getYPrime(yn[-1])
        
        k1 = h*getYPrime2(xn[-1],yn[-1])
        #get corrector
        #k2 = h*getYPrime(yn[-1]+k1)
        xn.append(x)
        k2 = h*getYPrime2(xn[-1],yn[-1]+k1)
        #get new yn
        yValue = yn[-1] + (k1+k2)/2
        yn.append(yValue)
        
        #get exact y
        y = getY2(x)
        yExact.append(y)
       
    return {"xn":xn,"yn":yn,"y":yExact}
        


y0 = 1
x0 = 0
h = 0.1
steps =10

result = ImprovedEulerMethod(x0,y0,h,steps)

    
    