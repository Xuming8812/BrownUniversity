#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 11:55:54 2019

@author: mingxu
"""

import sampyl as smp
from sampyl import np

X = np.array([[1,0,-0.13667714],
              [1,-1,-0.13667714],
              [1,-2,-0.13667714],
              [1,0,0.176091259],
              [1,-1,0.176091259],
              [1,-2,0.176091259]])

y = np.array([[0.293936814],
              [-0.046433586	],
              [-0.370488466	],
              [0.399639115],
              [0.061490177],
              [-0.258060922]])


def logp(b, sig):
    #define the model
    model = smp.Model()

    # Predicted value
    y_hat = np.dot(X, b)

    # Log-likelihood
    model.add(smp.normal(y, mu=y_hat, sig=sig))

    # log-priors
    model.add(smp.exponential(sig),
              smp.normal(b, mu=0, sig=100))

    return model()

start = smp.find_MAP(logp, {'b': np.ones(3), 'sig': 1.})
nuts = smp.NUTS(logp, start)
chain = nuts.sample(2100, burn=100)
import matplotlib.pyplot as plt
plt.plot(chain.b)

alpha0,alpha1,alpha2 = chain.b[:,0],chain.b[:,1],chain.b[:,2]
np.histogram(alpha0)

plt.hist(alpha0, bins='auto')
plt.hist(alpha1, bins='auto')
plt.hist(alpha2, bins='auto')

alpha0.sort()
alpha1.sort()
alpha2.sort()

print(alpha0[49],alpha0[1950])
print(alpha1[49],alpha1[1950])
print(alpha2[49],alpha2[1950])

import numpy as np
import scipy.stats


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.norm.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

