# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:10:28 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

def transformCoordinates(vB,B,Bprime):
    temp = np.matmul(B,vB)
    return np.matmul(np.linalg.inv(Bprime),temp)

submit(transformCoordinates, 'hw3_1b')

check_score()