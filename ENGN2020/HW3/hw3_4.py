# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:13:04 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

def gerschborinDisks(A):
    rowNum = A.shape[0]

    centers = np.zeros((rowNum,1))
    #centers = np.array([[]])
    radii = np.zeros((rowNum,1))

    eigvalues = np.zeros((rowNum,1))
    B = np.linalg.eig(A)


    for row in range(0,rowNum):
        radius = 0
        for col in range(0,rowNum):
            if row == col:
                centers[row,0] = A[row,col]
            else:
                radius = radius + A[row,col]

        radii[row,0] = radius
        eigvalues[row,0] = B[0][row]

    dict = {'centers':centers,'radii':radii,'eigvalues':eigvalues}
    return dict

submit(gerschborinDisks, 'hw3_4')

check_score()