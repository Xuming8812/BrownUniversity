# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:37:52 2019

@author: xumin
"""

#include libraries
import numpy as np
import json
import matplotlib.pyplot as plt
#read in results
results = json.load(open('results.json'))
team_names = json.load(open('teams.json'))
'''
* @name: getTopTenScores
* @description: get the top 10 results after given weeks
* @param results: results of all matches
* @param team_names: names of the college teams
* @param week: the given week
* @param index: the index of the team
* @return: info, data structure{"teamName", teamNumber,importance score}
'''
def getTopTenScores(results,team_names,week):
    #get datas for all teams after given weeks
    info = getScore(results,team_names,week)
    #sort the result by importance score
    info = np.sort(info, order='score')
    info = np.flip(info)
    #get top ten results
    result = info[0:10]
    return result
'''
* @name: getScoreByIndex
* @description: get the scores of a certain team after given weeks
* @param results: results of all matches
* @param team_names: names of the college teams
* @param week: the given week
* @param index: the index of the team
* @return: info, data structure{"teamName", teamNumber,importance score}
'''
def getScoreByIndex(results,team_names,week,index):
    #get datas for all teams after given weeks
    info = getScore(results,team_names,week)
    return info[index]
'''
* @name: displayScore
* @description: get all the scores of a certain team and display the result
* @param results: results of all matches
* @param team_names: names of the college teams
* @param index: the index of the team
* @return: array of scores of the given team
'''
def displayScore(results,team_names,index):
    #set initial values of scores and weeks
    scores = np.zeros((17,1))
    weeks = np.zeros((17,1))
    #loop each week to get importance score for the given team
    for i in range(17):
        temp= getScoreBｙＩｎｄｅｘ(results,team_names,i,index)
        weeks[i,0] = i+1
        scores[i,0] = temp['score']
    #plot the importance vesus week
    ax = plt.gca()
    plt.plot(weeks,scores)
    return scores
'''
* @name: getScore
* @description: get the scores of all teams after given weeks
* @param results: results of all matches
* @param team_names: names of the college teams
* @param week: the given week
* @return: info, data structure{"teamName", teamNumber,importance score}
'''
def getScore(results,team_names,week):
    #get all results from week 1 to given week
    weekresults = [result for result in results if result['week'] <= week]
    #get total number of teams
    teamNum = len(team_names)
    #set initial values of A and S
    A = np.zeros((teamNum,teamNum))
    S = np.ones((teamNum,teamNum))/teamNum
    #set the values of A according to match result
    #loop all matches
    for result in weekresults:
        #get home team and away team
        homeNo = result['home_team']
        awayNo = result['away_team']
        #if away wins
        if result['home_score']<result['away_score']:
        A[awayNo,homeNo] = 1
        else:
        A[homeNo,awayNo] = 1
    #make each column sum equals to 1
    for col in range(teamNum):
        temp = np.sum(A[:,col])
        if temp != 0:
            A[:,col] = A[:,col]/temp

    #set the value of m
    m = 0.15
    #get matrix M
    M = (1-m)*A + m*S
    #set the initial guess of x
    x = np.ones((teamNum,1))
    
    #power method to calculate x
    for i in range(50):
        x = np.matmul(M,x)
        #normalize x
        x = x/np.max(x)
    #declare a new data structure to save info
    dtype = [('teamName', 'S20'), ('teamNo', float), ('score', float)]
    info = np.empty(teamNum,dtype)
    #set the values of the information, including team name, team no, importance score
    for i in range(teamNum):
        info[i] = (team_names[i],i,x[i,0])
    return info