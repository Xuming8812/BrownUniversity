# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:47:07 2019

@author: xumin
"""
from submission.client import submit, check_score

def hello(word):
    """A function that takes in a word and says hello to it."""
    phrase = 'Hello,' + word + '!'
    return phrase

submit(hello, 'hw0_1a')

check_score()
