# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 22:06:39 2019

@author: xumin
"""
import math

def getYPrime(y):
    return 0.5*math.pi*(1-y**2)**0.5

def EulerIterate(lastY,step):
    yPrime = getYPrime(lastY)
    newY = lastY+yPrime*step
    return newY

y0 = 0
x0 = 0

h = 0.1

y = [y0]
x = [x0]
yPrime=[]

for i in range(10):
    yDiff = getYPrime(y[-1])
    yPrime.append(yDiff)
    yValue = EulerIterate(y[-1],h)  
    y.append(yValue)
    x.append(x[-1]+h)
    
print(x)
print(y)
print(yPrime)



    
    