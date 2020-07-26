# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:16:02 2019

@author: xumin
"""
import numpy as np
from scipy.integrate import odeint

import matplotlib.pyplot as plt

from scipy.optimize import fsolve
import math

Cinlet = 2   
Tinlet = 300
Hrxn = -83700
Rhocp = 4184
tao = 60
A = 4.3e18
EA = 125500   
R = 8.314


#part a
'''
* @name: f1
* @description: get the result of the system 
* @param y: the input value, in format of [CA,T]
* @return: list, [dCA/dt,dT/dt]
'''  
def f1(y):
        
    k = getK(y[1])
    #dCA/dt
    dy0 = ((Cinlet-y[0])/tao-k*y[0])
    #dT/dt
    dy1 = ((Tinlet-y[1])/tao-Hrxn*k*y[0]/Rhocp)
    
    return [dy0,dy1]

'''
* @name: getK
* @description: get k based on input temperature T
* @param T: the input temperture
* @return: k, the cofficient
'''    
def getK(T):
    return A*math.exp(-EA/(R*T))    


x, y =  fsolve(f1, [2.0, 500])
x, y =  fsolve(f1, [200, 3000])
x, y =  fsolve(f1, [10, 300])

#part b
'''
* @name: getDev
* @description: get the value of dev(Jacobian matrix) and f1 based on input value
* @param p: the input value, in format of [CA,T]
* @return: list, [dev(J),f1]
'''  
def getDev(p):
    
    Y,T = p
    
    k = getK(T)
        
    a = -1/tao - k
    b = -k*Y*EA/R/T/T
    c = -Hrxn/Rhocp*k
    d = -1/tao - Hrxn/Rhocp*k*Y*EA/R/T/T
    
    return [a*d-b*c,(Cinlet-Y)/tao-k*Y]

x, y =  fsolve(getDev, (2, 500))
x, y =  fsolve(getDev, (10, 300))
'''
* @name: getTinlet
* @description: get Tinlet based on CA and T
* @param Y: the input value of CA
* @param T: the input value of T
* @return: float, the value of Tinlet
'''  
def getTinlet(Y,T): 

    k = getK(T)  
    
    Tinlet = Hrxn*k*Y/Rhocp*tao+T
    
    return Tinlet

getTinlet(0.46977726099921147,329.45193859762)
getTinlet(1.5958612315442713,312.0553014597565)

    
#part c
'''
* @name: getDevMatrix
* @description: get Jacobian Matrix based on CA and T
* @param Y: the input value of CA
* @param T: the input value of T
* @return: float, the value of Tinlet
'''  
def getDevMatrix(Y,T):   
    k = getK(T)
     
    a = -1/tao - k
    b = -k*Y*EA/R/T/T
    c = -Hrxn/Rhocp*k
    d = -1/tao - Hrxn/Rhocp*k*Y*EA/R/T/T

    devMatrix = np.array([[a,b],[c,d]])
    
    return devMatrix

a = getDevMatrix(1.90527612180833,301.894930354838)
B = np.linalg.eig(a)
print(B[0])

a = getDevMatrix(0.252719607191793,334.9539600568946)
B = np.linalg.eig(a)
print(B[0])

a = getDevMatrix(0.80662556095798,323.873193247566)
B = np.linalg.eig(a)
print(B[0])


#part e
def f(y,t):
      
    k = getK(y[1])
    
    dy0 = ((Cinlet-y[0])/tao-k*y[0])
    dy1 = ((Tinlet-y[1])/tao-Hrxn*k*y[0]/Rhocp)
    
    return [dy0,dy1]

def solve(y0):
    t = np.linspace(0,6000,10000)
    #y0 = [0.8, 200.0]
    y = odeint(f, y0, t)
    
    print(y[-1])
    
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t,y[:,0],label='CA')
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('CA')
        
    axs[1].plot(t,y[:,1],label='T')
    axs[1].set_xlabel('time')    
    axs[1].set_ylabel('Temperature')
    
    fig.tight_layout()
    plt.show()
    
    return y[-1]
    
solve(y0 = [0,0])
solve(y0 = [0,500])
solve(y0 = [10,500])
solve(y0 = [2,2500])
solve(y0 = [200,0])

#part f
def mapInitialValues():
    Y = np.arange(0, 20, 0.1) 
    lenY = Y.shape[0]
    T = np.arange(0, 500, 5) 
    lenT = T.shape[0]
    Y_mesh, T_mesh = np.meshgrid(Y, T)
    
    result = np.zeros((Y_mesh.shape))
    
    case1 = [1.90527612180833,301.894930354838]
    case2 = [0.252719607191793,334.9539600568946]
    case3 = [0.80662556095798,323.873193247566]
    for i in range(lenY*lenT):
        row = i//lenY
        col = i%lenY
        
        temp = solve([Y_mesh[row][col],T_mesh[row][col]])
        
        distance1 = (case1[0]-temp[0])**2+(case1[1]-temp[1])**2
        distance2 = (case2[0]-temp[0])**2+(case2[1]-temp[1])**2
        distance3 = (case3[0]-temp[0])**2+(case3[1]-temp[1])**2
        
        if distance1<1:
            result[row][col] = 0.
        elif distance2<1:
            result[row][col] = 1.
        elif distance3<1:
            result[row][col] = -1.
            
    #plt.scatter(T, Y, s=result)
    #plt.show()
    
    return result
    
result = mapInitialValues()

fig, axs = plt.subplots(1, 1)
axs.matshow(result)
axs.set_xlabel('CA')
axs.set_ylabel('Temperature')

Y = np.arange(0, 20, 0.1)    
T = np.arange(0, 500, 5) 

plt.xscale('linear',0.2)
plt.yscale('linear',5)

plt.show()
    
    


        




 
 