# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:40:59 2019

@author: xumin
"""

#include libraries
import numpy as np
import matplotlib.pyplot as plt
import math
#set initial values
beta = math.pi/6
gamma = math.pi/3
Fload = 1000
#get vector b
b = np.zeros((6,1))
b[1,0] = Fload
#initial matrix of A
A = np.zeros((6,6))
#1sr equation
A[0,0] = -np.cos(beta)
A[0,2] = np.cos(gamma)
#2nd equation
A[1,0] = -np.sin(beta)
A[1,2] = -np.sin(gamma)
#3rd equation
A[2,0] = np.cos(beta)
A[2,1] = 1
A[2,3] = 1
#4th equation
A[3,0] = np.sin(beta)
A[3,4] = 1
#5th equation
A[4,1] = -1
A[4,2] = -np.cos(gamma)
#6th equation
A[5,2] = np.sin(gamma)
A[5,5] = 1
#reverse matrix A
invA = np.linalg.inv(A)
#solve the linear system
F = np.matmul(invA,b)