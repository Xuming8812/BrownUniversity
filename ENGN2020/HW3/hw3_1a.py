# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:09:54 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

def getCoordinates(vC,B):
    return np.matmul(np.linalg.inv(B),vC)

submit(getCoordinates, 'hw3_1a')

check_score()