# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:49:15 2019

@author: xumin
"""

from submission.client import submit, check_score

def isOdd(x):
    return x%2

submit(isOdd, 'hw0_1b')

check_score()