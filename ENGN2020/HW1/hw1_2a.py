# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:54:20 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

def elimination(A):
    #get the row number of matrix A
    rowNum = A.shape[0]
    #create I
    I = np.eye(rowNum)
    #combine A and I
    W = np.hstack([A, I])
    #divide eliminate for each row
    for i in range(1,rowNum):
        num = W[i,0]/W[0,0]
        W[i,:] = W[i,:] - num * W[0, :]

    return W

submit(elimination, 'hw1_2a')

check_score()