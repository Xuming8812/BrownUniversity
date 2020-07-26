# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:43:03 2019

@author: xumin
"""

#include libraries
import math
from scipy import optimize
'''
* @name: getV3
* @description: the function to calculate V3 based on given gamma
* @param gamma: input gamma
* @return: value of V3max – V3
'''
def getV3(gamma):
#get cot of gamma
    cot = 1/np.tan(gamma)
    k = 1+cot/(4/math.sqrt(3)-cot)
    return 800-1000/k

root = optimize.newton(getV3, 1)