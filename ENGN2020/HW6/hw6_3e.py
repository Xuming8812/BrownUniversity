#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 12:26:02 2019

@author: mingxu
"""

import requests
from lxml import html


class Vertex:
    def __init__(self, name):
        self.name = name

    def get_neighbors(self):
        #load the page
        page = requests.get(self.name)
        #get the tree structure of the urls
        tree = html.fromstring(page.content)
        #get all links
        links = tree.xpath('//a/@href')

        result = []
        #save all links related to engineering school
        for i in links:
            if i.startswith('https://www.brown.edu/academics/engineering/'):
                    result.append(str(i))
            if i.startswith('/academics/engineering'):
                result.append('https://www.brown.edu'+i)

        return result
    
    
class Queue:
    def __init__(self):
        self.queue = []
        
    def next(self):
        if(len(self.queue)!=0):
            result =  self.queue[0]
            self.queue.remove(result);
            return result;
        
    def append(self,vertex,distance):        
        result = {"distance":distance,"vertex":vertex}
        self.queue.append(result)


class StepTable:
    """Container to remember the steps taken by Moore's algorithm.
    "data" is a list of steps, where each step contains the vertex
    object, the distance from the origin, and the new neighbors
    encountered of that vertex. E.g.,
    
    data = [ (<vertex object>, 0, ['B', 'D']),
            (<vertex object>, 1, ['C']),
            (<vertex object>, 1, ['F']),
            ...]
    """
    
    def __init__(self, data=None):
        if data is None:
            self.data = []
        else:
            self.data = data
            
    def append(self, vertex, distance):
        """Adds the given vertex object to the step table.
        Distance is the distance from the origin."""
        neighbors = list(set(vertex.get_neighbors()))
        new_neighbors = self.get_new_neighbors(neighbors)
        self.data.append((vertex, distance, new_neighbors))
       
    def get_new_neighbors(self, neighbors):
        """Compares the vertex names in the list "neighbors"
        to the neighbors already contained in steptable.
        Returns a (shorter) list of names of neighbors that have
        not yet been discovered.
        """
        #loop all items in the neighbors
        for i in neighbors:
            #loop all vertices that in the step table
            for item in self.data:
                #if already exits in the step talbe, remove it
                visited = False
                if item[0].name == i:
                    neighbors.remove(i)
                    visited = True
                    break
                for neighbor in item[2]:
                    if(i == neighbor):
                        neighbors.remove(i)
                        visited = True
                        break  
                if(visited):
                    break;
                          
        return neighbors
                
    def get_reverse_path(self, vertex_name):
        """Starting at the vertex named "vertex_name", traces
        backwards through the step table to find the shortest
        distance to the origin. Note that this should only be
        called*after*vertex_name has been discovered.
        """       
        #initial list with given vertex name
        result = [vertex_name]
        
        #get length of the recorded data
        length = len(self.data)
        
        #set the current vertex name
        current = vertex_name
        
        start = self.data[0][0].name
        
        #loop from step table reversely
        for i in range(length):           
            for vertex in self.data:
                #find the current vertex in table
                if start == current:
                    return result
            
                if current in vertex[2]:
                    result.insert(0,vertex[0].name)
                    current = vertex[0].name
        
        return result
        
    def print(self):
        """Attempts to pretty print the contents of the
        step table."""
        for row in self.data:
            print('{:10s} {:3d} {:s}'.format(row[0].name, row[1], str(row[2])))



'''
* @name: findPath
* @description: use Moore`s algorithm to find the shortest path from start to end vertices
* @param start: the name of the start vertex
* @param end: the name of the end vertex
* @return: list, the shortest path from start to end vertices
'''
def findPath(start,end):
    #declare the queue
    bfs = Queue();
    #declare the step table
    record = StepTable();
    #create the start vertex
    start = Vertex(start);
    #append this start point into queue
    bfs.append(start,0)
    #save the this start point into step table
    record.append(start,0);
    
    #use Moore`s algorithm or so called bfs
    while(bfs.queue!=[]):
        #get the front the queue 
        nextNode = bfs.next()
        
        currentName = nextNode["vertex"].name
        #if find the target then break the while loop
        if currentName==end:
            break
        #get the distance of this point
        currentDistance = nextNode["distance"]
        #get the neighbors of this point
        neighbors = list(set(nextNode["vertex"].get_neighbors()));
        
        #loop all neighbors
        for item in neighbors:
            #use a bool value to see if the vertex has been visited
            visited = False
            
            #loop all records in the step table to see if visited
            for step in record.data:
                if step[0].name == item:
                    visited = True
                    break
            #if not visited
            if(not visited):
                #create the vertex 
                temp = Vertex(item);
                #push it into queue
                bfs.append(temp,currentDistance+1);
                #record this step in step table
                record.append(temp,currentDistance+1);
            
    #record.print()
    #get the path from start to end
    path = record.get_reverse_path(end);
    #print path
    print(path)
    
    return path
        

findPath('https://www.brown.edu/academics/engineering/',\
         'https://www.brown.edu/academics/engineering/graduate-study/masters-and-phd-programs')
#findPath('B','J')