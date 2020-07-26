# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:19:06 2019

@author: xumin
"""

from scipy.optimize import fsolve
from submission.client import submit
import math

class RootFactor:
    def __init__(self, f, fprime, roots):
        self.f = f
        self.fprime = fprime
        self.roots = roots
        
    def get_f(self, x):
        rootNum = len(self.roots)        
        result = self.f(x)
        
        for i in range(rootNum):
            result = result*(1./(x-self.roots[i]))
            
        return result
        
    def get_fprime(self, x):
        
        rootNum = len(self.roots)   
        
        continousProduct = 1
        
        for i in range(rootNum):
            continousProduct = continousProduct*(1./(x-self.roots[i]))
            
        part1 =self.fprime(x)*continousProduct
        
        part2=0
        
        for i in range(rootNum):
            part2 = part2 -continousProduct*(1.0/(x-self.roots[i]))
        
        part2 = part2 * self.f(x)
        
        return part1+part2
        
def get_f(x):
    return 0.2*x**2 -20.*math.sin(x)+30*math.cos(0.3*x+1.)
    
def get_fprime(x):    
    return 0.4*x-20.*math.cos(x)-9.*math.sin(0.3*x+1.)
    
def use_my_code(roots, x0):
    newfunction = RootFactor(f=get_f, fprime=get_fprime, roots=roots)
    root = fsolve(func=newfunction.get_f, fprime=newfunction.get_fprime,x0=x0)
    return root

submit(use_my_code, assignment='hw4_2c')