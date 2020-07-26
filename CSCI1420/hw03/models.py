#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
   This file contains the Logistic Regression classifier

   Brown CS142, Spring 2020
'''
import random
import numpy as np


def softmax(x):
    '''
    Apply softmax to an array

    @params:
        x: the original array
    @return:
        an array with softmax applied elementwise.
    '''
    e = np.exp(x - np.max(x))
    return e / np.sum(e)

class LogisticRegression:
    '''
    Multinomial Logistic Regression that learns weights using 
    stochastic gradient descent.
    '''
    def __init__(self, n_features, n_classes, batch_size, conv_threshold):
        '''
        Initializes a LogisticRegression classifer.

        @attrs:
            n_features: the number of features in the classification problem
            n_classes: the number of classes in the classification problem
            weights: The weights of the Logistic Regression model
            alpha: The learning rate used in stochastic gradient descent
        '''
        self.n_classes = n_classes
        self.n_features = n_features
        self.weights = np.zeros((n_features + 1, n_classes))  # An extra row added for the bias
        self.alpha = 0.03  # tune this parameter
        self.batch_size = batch_size
        self.conv_threshold = conv_threshold

    def train(self, X, Y):
        '''
        Trains the model, using stochastic gradient descent

        @params:
            X: a 2D Numpy array where each row contains an example, padded by 1 column for the bias
            Y: a 1D Numpy array containing the corresponding labels for each example
        @return:
            num_epochs: integer representing the number of epochs taken to reach convergence
        '''

        #initialization
        previous_loss = 0
        is_converge = False
        m = X.shape[0]
        num_epochs = 0
        all_loss = np
        #stack X and Y together for shuffling
        training_data = np.column_stack((X,Y))


        #loop until converge
        while not is_converge:
            #shuffle training data every epoch            
            np.random.shuffle(training_data)
            #loop every batch
            for i in range(m//self.batch_size-1):
                #get current batch of X and Y
                current_batch_X = training_data[i*self.batch_size : (i+1)*self.batch_size,:-1]
                current_batch_Y = training_data[i*self.batch_size : (i+1)*self.batch_size,-1]
                #case y to int64 
                current_batch_Y_int = current_batch_Y.astype(int)
                #get gradient matrix of weights
                gradient_matrix = self.gradient(current_batch_X, current_batch_Y_int)
                #gradient descent
                self.weights = self.weights - self.alpha*gradient_matrix

            #calculate loss over all examples
            current_loss = self.loss(X,Y)
            #update number of total epochs
            num_epochs += 1
            #check converge
            if(np.absolute(current_loss - previous_loss)< self.conv_threshold):
                is_converge = True
            #update previous loss
            previous_loss = current_loss

        return num_epochs

    def loss(self, X, Y):
        '''
        Returns the total log loss on some dataset (X, Y), divided by the number of datapoints.
        @params:
            X: 2D Numpy array where each row contains an example, padded by 1 column for the bias
            Y: 1D Numpy array containing the corresponding labels for each example
        @return:
            A float number which is the squared error of the model on the dataset
        '''
        n_examples = X.shape[0]
        total_loss = 0

        y = np.dot(X, self.weights)
        #apply softmax
        l = np.apply_along_axis(softmax,1,y)
        #update the total loss
        for i in range(n_examples):
            total_loss = total_loss - np.log(l[i,Y[i]]+0.00001)
        
        return total_loss/n_examples

    def gradient(self, X, Y):
        n_examples = X.shape[0]
        y = np.dot(X, self.weights)
        #apply softmax
        l = np.apply_along_axis(softmax,1,y)
        
        for i in range(n_examples):
            l[i, Y[i]] -= 1

        gradient_matrix = np.dot(X.transpose(), l) 
        
        return gradient_matrix/n_examples

    def predict(self, X):
        '''
        Compute predictions based on the learned parameters and examples X

        @params:
            X: a 2D Numpy array where each row contains an example, padded by 1 column for the bias
        @return:
            A 1D Numpy array with one element for each row in X containing the predicted class.
        '''
        n_samples = X.shape[0]
        y = np.dot(X, self.weights)
        #apply softmax
        softmax_result = np.apply_along_axis(softmax,1,y)

        predictions = np.zeros((n_samples,1))
        #find the class that has max probability 
        for i in range(n_samples):
            predictions[i] = np.argmax(softmax_result[i,:])

        return predictions


    def accuracy(self, X, Y):
        '''
        Outputs the accuracy of the trained model on a given testing dataset X and labels Y.

        @params:
            X: a 2D Numpy array where each row contains an example, padded by 1 column for the bias
            Y: a 1D Numpy array containing the corresponding labels for each example
        @return:
            a float number indicating accuracy (between 0 and 1)
        '''
        #get predictions 
        predictions = self.predict(X)
        n_samples = X.shape[0]
        accurate = 0
        #compare prediction with actual label
        for i in range(n_samples):
            if predictions[i] == Y[i]:
                accurate = accurate + 1

        return accurate/n_samples
