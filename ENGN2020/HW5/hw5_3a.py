# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 10:39:48 2019

@author: xumin
"""

from submission.client import submit, check_score

class Vertex:
    def __init__(self, name):
        self.name = name
    def get_children(self):
        return Vertex.links[self.name];
    #save the link in the vertex class
    links = {
    'A': ['B', 'D', 'G'],
    'B': ['E', 'G', 'H'],
    'C': ['A', 'H', 'I'],
    'D': ['F'],
    'E': ['H', 'A', 'C'],
    'F': ['G', 'I'],
    'G': ['C'],
    'H': ['A', 'E'],
    'I': ['C', 'J']
    }

submit(Vertex, 'hw5_3a')

check_score()