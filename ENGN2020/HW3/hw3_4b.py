# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:14:48 2019

@author: xumin
"""

A = np.array([[5,2,4],
            [-2,0,2],
            [2,4,7]])

A = np.array([[5,0.01,0.01],
            [0.01,8,0.01],
            [0.01,0.01,9]])

A = np.array([[0,0.4,-0.1],
            [0.01,8,0.01],
            [0.01,0.01,9]])





def showEigen(A):

    import matplotlib.pyplot as plt
    import math

    plt.axis('equal')

    #get axes of the plot
    ax = plt.gca()
    #set the top and right boundary to none
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    #set the xaxis as the bottom boundary
    ax.xaxis.set_ticks_position('bottom')
    # set the yaxis as the left boundary
    ax.yaxis.set_ticks_position('left')
    # set the (0,0) as the position of left and bottom position
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))


    rowNum = A.shape[0]
    dict = gerschborinDisks(A)

    alpha = np.linspace(0., 2*math.pi,100)

    for i in range(0,rowNum):
        x = dict['centers'][i]+dict['radii'][i]*np.cos(alpha)
        y = dict['radii'][i]*np.sin(alpha)

        plt.plot(x,y,color = 'blue')
        plt.plot(dict['eigvalues'][i],0, 'ro')