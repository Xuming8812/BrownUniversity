# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:50:35 2019

@author: xumin
"""

from submission.client import submit, check_score

def getSum(A):
    import numpy as np
    first = np.array(A[:,1])
    second = np.array(A[:,2])
    return np.sum(first)+np.sum(second)

submit(getSum, 'hw1_1a')

check_score()