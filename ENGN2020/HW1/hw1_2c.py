# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:01:44 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

def solveX(A,b):
    return np.matmul(np.linalg.inv(A),b)

submit(solveX, 'hw1_2c')

check_score()