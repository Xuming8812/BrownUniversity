# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:36:58 2019

@author: xumin
"""

#the matrix of A
A = np.array([[0.,1.,0.,0.,0.],
[1.,0.,0.,0.,0.],
[0.,0.,0.,1.,0.5],
[0.,0.,0.,0.,0.5],
[0.,0.,0.,0.,0.]])
#get size of matrix A
n = A.shape[0]
#build matrix S
S = np.ones((n,n))/n
#set value of m
m = 0.15
#build matrix S
M = (1-m)*A + m*S
#solve for eigenvalues and eigen vectors
C = np.linalg.eig(M)
#get the result
V = C[1][:,0]
#normalize by norm 1
V = V/np.max(V)

