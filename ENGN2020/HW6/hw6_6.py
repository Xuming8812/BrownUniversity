# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 23:05:25 2019

@author: xumin
"""
import numpy as np
'''
* @name: Prim
* @description: the class to implement Prim`s algorithm for shortest spanning tree
* @param adjMatrix: the given graph stored in adjacency matrix
'''
class Prim: 
    '''
    * @name: __init__
    * @description: constructor of the class
    * @param adjMatrix: the given graph stored in adjacency matrix
    '''
    def __init__(self,adjMatrix):
        #the input value is a adjacency matrix
        self.graph = adjMatrix
    
    '''
    * @name: nextVertex
    * @description: decide which is the next vertex to add to the tree
    * @param U: the vertices that already in the spanning tree
    * @param visited: list that save whether the vertex is used
    * @return: list, the new vertex added to the tree and the parent vertex of the new vertex
    '''
    def nextVertex(self,U,visited):
        #get the number of vertices
        vertexNum = self.graph.shape[0]
        
        #initial the values
        minValue = 10000 
        minIndex = 0
        parent = 0
        
        #loop all unvisited vertices
        for i in range(vertexNum):
            if not visited[i]:
                #loop all nodes that already in the tree
                for j in U:
                    #find the nearest distance to the vertices in the tree
                    if self.graph[i][j]< minValue and self.graph[i][j]!=0:
                        minValue = self.graph[i][j]
                        minIndex = i
                        parent = j
        #return the list of the new vertex added to the tree and the parent vertex of the new vertex
        return [minIndex,parent]
    
    '''
    * @name: prim
    * @description: use Prim`s algorithm to create the shortest spanning tree
    * @param U: the vertices that already in the spanning tree
    * @param visited: list that save whether the vertex is used
    '''            
    def prim(self):
        #get the number of the vertices in the graph
        vertexNum = self.graph.shape[0]
        
        #set the all vertices by unvisited
        visited = [False]*vertexNum
        #start with vertex 0
        visited[0] = True
        U =[0]
        #loop all vertices
        for i in range(vertexNum):
            #call the member function to find next vertex
            nextStep = self.nextVertex(U,visited)
            #add it in U
            U.append(nextStep[0]);
            #set it as visited
            visited[nextStep[0]] = True;
            #print it
            if nextStep[0]!=nextStep[1]:
                print("Parent: "+str(nextStep[1]+1)+"    next: "+str(nextStep[0]+1))  
            

            
A = np.array([[0, 2, 0, 6, 0],
              [2, 0, 3, 8, 5],
              [0, 3, 0, 0, 7],
              [6, 8, 0, 0, 9],
              [0, 5, 7, 9, 0]])

a = Prim(A);
a.prim();            

A = np.array([[0, 6, 1, 0, 15],
              [6, 0, 3, 14, 9],
              [1, 3, 0, 10, 0],
              [0, 14, 0, 0, 2],
              [15, 9, 0, 9, 0]])
    

A = np.array([[0, 6, 4, 2, 0, 0],
              [6, 0, 14, 0, 0, 8],
              [4, 14, 0, 6, 12,12],
              [2, 0, 6, 0, 20, 0],
              [0, 0, 12, 20, 0, 0],
              [0, 8, 12, 0, 0, 0]])
    
A = np.array([[0, 3, 0, 0, 0, 0, 0, 8],
              [3, 0, 4, 0, 0, 10, 7, 7],
              [0, 4, 0, 3, 5, 2, 6, 0],
              [0, 0, 3, 0, 0, 1, 0, 0],
              [0, 0, 5, 0, 0, 6, 0, 0],
              [0, 10, 2, 1, 6, 0, 8, 0],
              [0, 7, 6, 0, 0, 8, 0, 20],
              [8, 7, 0, 0, 0, 0, 20, 0]])
    
A = np.array([[0, 16, 8, 4, 0],
              [16, 0, 6, 4, 0],
              [8, 6, 0, 2, 10],
              [4, 4, 2, 0, 14],
              [0, 0, 10, 14, 0]])
