# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:06:46 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

def solveEquation(a,b,c):
    A = np.array([[0, 1, 0],
                  [2, -2, -1],
                  [0,0,2]])
    B = np.array([[a,-c,b]]).T
    return np.linalg.solve(A,B)

submit(solveEquation, 'hw2_2')

check_score()