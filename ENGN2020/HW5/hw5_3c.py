# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:29:37 2019

@author: xumin
"""

from submission.client import submit, check_score

def findEngineeringLinks(website):


    import requests
    from lxml import html

    page = requests.get(website)
    tree = html.fromstring(page.content)
    links = tree.xpath('//a/@href')

    length = len(links)

    result=[]

    for i in range(length):
        if(links[i].find('/academics/engineering/')!=-1):
            result.append(links[i])

    return result

submit(findEngineeringLinks,'hw5_3c')

check_score()