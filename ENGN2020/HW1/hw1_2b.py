# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:00:29 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

def eliminationLower(A):
    rowNum = A.shape[0]
    I = np.eye(rowNum)

    W = np.hstack([A, I])

    for i in range(1,rowNum):
        for j in range(0,i):
            num = W[i,j]/W[j,j]
            W[i,:] = W[i,:] - num * W[j, :]

    return W

submit(eliminationLower, 'hw1_2b')

check_score()