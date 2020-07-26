# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:03:46 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

def solvecircuit(R1,R2,R3,deltaV1,deltaV2):
    A = np.array([[1, -1, -1],
                  [R1, 0, R3],
                  [0,R2,-R3]])
    B = np.array([[0,deltaV1,deltaV2]]).T
    return np.linalg.solve(A,B)

submit(solvecircuit, 'hw2_1')

check_score()