# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:53:29 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

def multiplyInOrder(A,B,C,D):
    result = np.matmul(A, B)
    result = np.matmul(result, C)
    result = np.matmul(result, D)

    return result

submit(multiplyInOrder, 'hw1_1c')

check_score()