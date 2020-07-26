# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:16:57 2019

@author: xumin
"""

from submission.client import submit, check_score
import numpy as np

class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def get_value(self, x):
        length = len(self.coefficients)

        result = 0

        for i in range(length):
            result = result + self.coefficients[i]*x**(length-1-i)

        return result

submit(Polynomial, 'hw4_1')

check_score()