# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:07:27 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

def eigenVector(A):
    B = np.linalg.eig(A)
    A = np.array([[0, 1],
              [-1, 0]])

    C = B[1]
    result = np.matmul(C, A)
    return result

submit(eigenVector, 'hw2_5b')

check_score()