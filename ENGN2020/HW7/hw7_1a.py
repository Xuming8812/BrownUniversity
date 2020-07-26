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

def getY(x):
    return math.sin(x*math.pi*0.5)

def EulerMethod(x0,y0,h,steps):
    yn = [y0]
    xn = [x0]
    
    yExact = [y0]
    
    yPrime=[]
    
    for i in range(steps):
        #get ydiff by last yn
        yDiff = getYPrime(yn[-1])
        yPrime.append(yDiff)
        #get new yn by last yn and step
        yValue = EulerIterate(yn[-1],h)
        
        yn.append(yValue)
        #get xn
        x = xn[-1]+h
        xn.append(x)
        
        #get exact y
        y = getY(x)
        yExact.append(y)
       
    return {"xn":xn,"yn":yn,"y":yExact,"yPrime":yPrime}
        


y0 = 0
x0 = 0
h = 0.1
steps =10

result = EulerMethod(x0,y0,h,steps)

    
    