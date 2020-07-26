# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:32:23 2019

@author: xumin
"""

from matplotlib import rc
rc("font", family="serif", size=12)
rc("text", usetex=False)

#import daft library
import daft

class Vertex:
    #return the edges based on input vertex name
    def get_children(self,name):
        self.name = name
        return Vertex.links[self.name];
    #draw the graph
    def draw(self):
        #initialize the graph
        pgm = daft.PGM([6, 6], origin=[0, 1])

        #give the location of all vertices
        pgm.add_node(daft.Node("A", r"A", 1, 5))
        pgm.add_node(daft.Node("B", r"B", 5, 5))
        pgm.add_node(daft.Node("D", r"D", .5, 3))
        pgm.add_node(daft.Node("G", r"G", 1.5, 3))
        pgm.add_node(daft.Node("E", r"E", 5.5, 4))
        pgm.add_node(daft.Node("H", r"H", 5.5, 2))
        pgm.add_node(daft.Node("C", r"C", 3, 3))
        pgm.add_node(daft.Node("F", r"F", 1, 1.5))
        pgm.add_node(daft.Node("I", r"I", 3, 1.5))
        pgm.add_node(daft.Node("J", r"J", 5, 1.5))

        #loop all edges to add to daft
        for start, edges in Vertex.links.items():
            for item in edges:
                pgm.add_edge(start,item)
        #draw the graph
        pgm.render()
        pgm.figure.savefig("vertex.png",dpi=150)

    #the graph
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

#define a Vertex object
a = Vertex()
#draw the graph
a.draw()