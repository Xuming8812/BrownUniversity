# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:51:32 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np


def multiplyElement(A,B,i,j):
    #get the ith row of A
    row = np.array(A[i,:])
    #get the jth column of A
    col = np.array(B[:,j])
    #multipy the row with the column
    result = np.array(row*col)
    #return the sum
    return np.sum(result);

submit(multiplyElement, 'hw1_1b')

check_score()