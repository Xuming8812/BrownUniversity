# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 20:57:34 2019

@author: xumin
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

x = np.arange(-6,6,0.1)


def f1(x):
    return x**2 + 3*x + 5
def f2(x):
    return -1 * x**2 + 5 * x - 7
def f3(x):
    return 2 * x**2 - 4 * x + 7
def loss(xs):
    x1 = xs[0]
    y1 = xs[1]
    x2 = xs[2]
    y2 = xs[3]
    x3 = xs[4]
    y3 = xs[5]
    y1_ = f1(x1)
    y2_ = f2(x2)
    y3_ = f3(x3)

    dist = np.sqrt((x2-x1)**2+(y2-y1)**2) + np.sqrt((x3-x2)**2+(y3-y2)**2) + 5 * (y1-y1_)**2 + 5 * (y2-y2_)**2 + 5 *  (y3-y3_)**2
    return dist

res = minimize(loss,np.array([1,1.5,2,2.5,5,5.5]))

y1 = f1(x)
y2 = f2(x)
y3 = f3(x)

#plt.axis('equal')

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

plt.plot(x,y1)
plt.plot(x,y2)
plt.plot(x,y3)

X = [0,0,0]
Y = [0,0,0]
for i in range(3):
    X[i] = res.x[2*i]
    Y[i] = res.x[2*i+1]

plt.plot(X,Y)
plt.axis([-5, 6, -5, 10])
plt.legend(loc='upper right')
plt.show()