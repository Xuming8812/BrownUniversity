# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:28:16 2019

@author: xumin
"""

from submission.client import submit, check_score
import requests
from lxml import html

class Vertex:
    def __init__(self, name):
        self.name = name

    def get_children(self):
        #load the page
        page = requests.get(self.name)
        #get the tree structure of the urls
        tree = html.fromstring(page.content)
        #get all links
        links = tree.xpath('//a/@href')

        result = []
        #save all links related to engineering school
        for i in links:
            if i.startswith('http://www.brown.edu/academics/engineering/') \
                or i.startswith('https://www.brown.edu/academics/engineering/') \
                or i.startswith('/academics/engineering'):
                    result.append(i)

        return result

submit(Vertex, 'hw5_3d')

check_score()