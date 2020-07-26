# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:18:20 2019

@author: xumin
"""

class RootFactor:
    def __init__(self, f, fprime, roots):
        self.f = f
        self.fprime = fprime
        self.roots = roots
        
    def get_f(self, x):
        #get the length of array nums
        rootNum = len(self.roots) 
        #get f(x)
        result = self.f(x)
        #g = f(x) multiplied by the continous product of fi, where fi = 1/(x-root[i])
        for i in range(rootNum):
            result = result*(1./(x-self.roots[i]))
        #return g    
        return result 

    def get_fprime(self, x):
        #get the length of array nums
        rootNum = len(self.roots)   
        # the continous product of fi, where fi = 1/(x-root[i]) is needed several times in the calculation, calculate it first
        # continousProduct = 1 
        for i in range(rootNum):
            continousProduct = continousProduct*(1./(x-self.roots[i])) 
        #according to the equation in Problem4(a), g` equals two parts summed together
        #the first part is f` multiplied by the continous product of fi
        part1 =self.fprime(x)*continousProduct 
        #set the initial value of part2
        part2=0 
        #part2 is the sum of fi*continous product
        for i in range(rootNum):
            part2 = part2 -continousProduct*(1.0/(x-self.roots[i]))
        #multiplied part2 by f(x)
        part2 = part2 * self.f(x)
        #g` is the sum of part1 and part2
        return part1+part2	
