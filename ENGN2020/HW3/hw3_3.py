# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:11:42 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

def powerMethod(A,x0,n):
    x = x0
    for i in range(0,n):
        x = np.matmul(A, x)
        a = np.max(x)
        x = x/a
    return x

submit(powerMethod, 'hw3_3')

check_score()