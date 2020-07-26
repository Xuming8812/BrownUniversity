# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 10:40:31 2019

@author: xumin
"""

from submission.client import submit, check_score

def filter(links):
    length = len(links)

    result=[]

    #loop all links to see if it contains the "/academics/engineering/" key word
    for i in range(length):
        if(links[i].find('/academics/engineering/')!=-1):
            #save to result list
            result.append(links[i])

    return result

submit(filter, 'hw5_3b')

check_score()