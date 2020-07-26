import numpy as np
import random


def l2_loss(predictions,Y):
    '''
        Computes L2 loss (sum squared loss) between true values, Y, and predictions.

        :param Y: A 1D Numpy array with real values (float64)
        :param predictions: A 1D Numpy array of the same size of Y
        :return: L2 loss using predictions for Y.
    '''
    n_predictions = len(predictions)
    loss = 0.0
    for i in range(n_predictions):
        loss += (predictions[i]-Y[i])*(predictions[i]-Y[i])
    return loss

def sigmoid(x):
    '''
        Sigmoid function f(x) =  1/(1 + exp(-x))
        :param x: A scalar or Numpy array
        :return: Sigmoid function evaluated at x (applied element-wise if it is an array)
    '''
    return np.where(x > 0, 1 / (1 + np.exp(-x)), np.exp(x) / (np.exp(x) + np.exp(0)))

def sigmoid_derivative(x):
    '''
        First derivative of the sigmoid function with respect to x.
        :param x: A scalar or Numpy array
        :return: Derivative of sigmoid evaluated at x (applied element-wise if it is an array)
    '''
    return sigmoid(x)*(1-sigmoid(x))

def relu(x):
    return np.where(x>0,x,0)
def relu_derivative(x):
    return np.where(x>0,1,0)

class OneLayerNN:
    '''
        One layer neural network trained with Stocastic Gradient Descent (SGD)
    '''
    def __init__(self):
        '''
        @attrs:
            weights The weights of the neural network model.
        '''
        self.weights = None
        pass

    def train(self, X, Y, learning_rate=0.001, epochs=250, print_loss=True):
        '''
        Trains the OneLayerNN model using SGD.

        :param X: 2D Numpy array where each row contains an example
        :param Y: 1D Numpy array containing the corresponding values for each example
        :param learning_rate: The learning rate to use for SGD
        :param epochs: The number of times to pass through the dataset
        :param print_loss: If True, print the loss after each epoch.
        :return: None
        '''
        n_examples, n_features = X.shape
        w = np.random.normal(size = n_features)

        for epoch in range(epochs):
            indices = [i for i in range(n_examples)]
            random.shuffle(indices)
            for i in indices:
                dev = np.zeros((n_features))
                for j in range(n_features):
                    dev[j] = 2*(Y[i]-np.dot(w,X[i]))*(-X[i][j])
                w -= learning_rate*dev

        self.weights = w

    def predict(self, X):
        '''
        Returns predictions of the model on a set of examples X.

        :param X: 2D Numpy array where each row contains an example.
        :return: A 1D Numpy array containing the corresponding predicted values for each example
        '''
        n_examples = len(X)
        predictions = np.zeros((n_examples))

        for i in range(n_examples):
            predictions[i] = np.dot(self.weights, X[i])

        return predictions

    def loss(self, X, Y):
        '''
        Returns the total squared error on some dataset (X, Y).

        :param X: 2D Numpy array where each row contains an example
        :param Y: 1D Numpy array containing the corresponding values for each example
        :return: A float which is the squared error of the model on the dataset
        '''
        predictions = self.predict(X)
        return l2_loss(predictions, Y)

    def average_loss(self, X, Y):
        '''
        Returns the mean squared error on some dataset (X, Y).

        MSE = Total squared error/# of examples

        :param X: 2D Numpy array where each row contains an example
        :param Y: 1D Numpy array containing the corresponding values for each example
        :return: A float which is the mean squared error of the model on the dataset
        '''
        return self.loss(X, Y)/X.shape[0]

class TwoLayerNN:

    def __init__(self, hidden_size, activation=sigmoid, activation_derivative=sigmoid_derivative):
        '''
        @attrs:
            activation: the activation function applied after the first layer
            activation_derivative: the derivative of the activation function. Used for training.
            hidden_size: The hidden size of the network (an integer)
            output_neurons: The number of outputs of the network
        '''
        self.activation = activation
        self.activation_derivative = activation_derivative
        self.hidden_size = hidden_size

        # In this assignment, we will only use output_neurons = 1.
        self.output_neurons = 1

    def _get_layer2_bias_gradient(self, x, y, layer1_weights, layer1_bias,
        layer2_weights, layer2_bias):
        '''
        Computes the gradient of the loss with respect to the output bias, b2.

        :param x: Numpy array for a single training example with dimension: input_size by 1
        :param y: Label for the training example
        :param layer1_weights: Numpy array of dimension: hidden_size by input_size
        :param layer1_bias: Numpy array of dimension: hidden_size by 1
        :param layer2_weights: Numpy array of dimension: output_neurons by hidden_size
        :param layer2_bias: Numpy array of dimension: output_neurons by 1
        :return: the partial derivates dL/db2, a numpy array of dimension: output_neurons by 1
        '''
        n_features = len(x)
        n_hidden = len(layer1_bias)
        a = np.matmul(layer1_weights,x).reshape((n_hidden,1))+layer1_bias
        v = self.activation(a)
        h = np.matmul(layer2_weights, v) + layer2_bias

        return 2*(h-y)

    def _get_layer2_weights_gradient(self, x, y, layer1_weights, layer1_bias,
        layer2_weights, layer2_bias):
        '''
        Computes the gradient of the loss with respect to the output weights, v.

        :param x: Numpy array for a single training example with dimension: input_size by 1
        :param y: Label for the training example
        :param layer1_weights: Numpy array of dimension: hidden_size by input_size
        :param layer1_bias: Numpy array of dimension: hidden_size by 1
        :param layer2_weights: Numpy array of dimension: output_neurons by hidden_size
        :param layer2_bias: Numpy array of dimension: output_neurons by 1
        :return: the partial derivates dL/dv, a numpy array of dimension: output_neurons by hidden_size
        '''
        n_features = len(x)
        n_hidden = len(layer1_bias)
        a = np.matmul(layer1_weights,x).reshape((n_hidden,1))+layer1_bias
        v = self.activation(a)
        h = np.matmul(layer2_weights, v) + layer2_bias
        return 2*(h-y)*v.T

    def _get_layer1_bias_gradient(self, x, y, layer1_weights, layer1_bias,
        layer2_weights, layer2_bias):
        '''
        Computes the gradient of the loss with respect to the hidden bias, b1.

        :param x: Numpy array for a single training example with dimension: input_size by 1
        :param y: Label for the training example
        :param layer1_weights: Numpy array of dimension: hidden_size by input_size
        :param layer1_bias: Numpy array of dimension: hidden_size by 1
        :param layer2_weights: Numpy array of dimension: output_neurons by hidden_size
        :param layer2_bias: Numpy array of dimension: output_neurons by 1
        :return: the partial derivates dL/db1, a numpy array of dimension: hidden_size by 1
        '''
        n_features = len(x)
        n_hidden = len(layer1_bias)
        a = np.matmul(layer1_weights,x).reshape((n_hidden,1))+layer1_bias
        v = self.activation(a)
        h = np.matmul(layer2_weights, v) + layer2_bias
        dev = self.activation_derivative(a)
        gradients = np.zeros((n_hidden,1))
        for i in range(n_hidden):
            gradients[i] = 2*(h-y)*dev[i]*layer2_weights[0][i]
        return gradients

    def _get_layer1_weights_gradient(self, x, y, layer1_weights, layer1_bias,
        layer2_weights, layer2_bias):
        '''
        Computes the gradient of the loss with respect to the hidden weights, W.

        :param x: Numpy array for a single training example with dimension: input_size by 1
        :param y: Label for the training example
        :param layer1_weights: Numpy array of dimension: hidden_size by input_size
        :param layer1_bias: Numpy array of dimension: hidden_size by 1
        :param layer2_weights: Numpy array of dimension: output_neurons by hidden_size
        :param layer2_bias: Numpy array of dimension: output_neurons by 1
        :return: the partial derivates dL/dW, a numpy array of dimension: hidden_size by input_size
        '''
        n_features = len(x)
        n_hidden = len(layer1_bias)
        a = np.matmul(layer1_weights,x).reshape((n_hidden,1))+layer1_bias
        v = self.activation(a)
        h = np.matmul(layer2_weights, v) + layer2_bias
        dev = self.activation_derivative(a)
        gradients = np.zeros((n_hidden,n_features))

        for i in range(n_hidden):
            C = 2*(h-y)*layer2_weights[0][i]*self.activation_derivative(np.matmul(layer1_weights[i][:],x)+layer1_bias[i])
            for j in range(n_features):
                gradients[i][j] = C*x[j]

        return gradients



    def train(self, X, Y, learning_rate=0.01, epochs=1000, print_loss=True):
        '''
        Trains the TwoLayerNN with SGD using Backpropagation.

        :param X: 2D Numpy array where each row contains an example
        :param Y: 1D Numpy array containing the corresponding values for each example
        :param learning_rate: The learning rate to use for SGD
        :param epochs: The number of times to pass through the dataset
        :param print_loss: If True, print the loss after each epoch.
        :return: None
        '''
        # NOTE:
        # Use numpy arrays of the following dimensions for your model's parameters.
        # layer 1 weights: hidden_size x input_size
        # layer 1 bias: hidden_size x 1
        # layer 2 weights: output_neurons x hidden_size
        # layer 2 bias: output_neurons x 1
        # HINT: for best performance initialize weights with np.random.normal or np.random.uniform
        n_examples, n_features = X.shape
        #initialization by normal distribution
        layer1_weights = np.random.normal(size=(self.hidden_size, n_features))
        layer1_bias = np.random.normal(size=(self.hidden_size,1))
        layer2_weights = np.random.normal(size = (self.output_neurons, self.hidden_size))
        layer2_bias = np.random.normal(size = (self.output_neurons,1))

        for epoch in range(epochs):
            indices = [i for i in range(n_examples)]
            random.shuffle(indices)     
            for i in indices:
                layer1_weights_gradients = self._get_layer1_weights_gradient(X[i],Y[i],layer1_weights,layer1_bias,layer2_weights,layer2_bias)
                layer2_weights_gradients = self._get_layer2_weights_gradient(X[i],Y[i],layer1_weights,layer1_bias,layer2_weights,layer2_bias)
                layer1_bias_gradients = self._get_layer1_bias_gradient(X[i],Y[i],layer1_weights,layer1_bias,layer2_weights,layer2_bias)
                layer2_bias_gradients = self._get_layer2_bias_gradient(X[i],Y[i],layer1_weights,layer1_bias,layer2_weights,layer2_bias)

                layer1_weights -= learning_rate * layer1_weights_gradients              
                layer2_weights -= learning_rate * layer2_weights_gradients
                layer1_bias -= learning_rate * layer1_bias_gradients
                layer2_bias -= learning_rate * layer2_bias_gradients
        
        self.layer1_weights = layer1_weights
        self.layer1_bias = layer1_bias
        self.layer2_weights = layer2_weights
        self.layer2_bias = layer2_bias



    def predict(self, X):
        '''
        Returns predictions of the model on a set of examples X.

        :param X: 2D Numpy array where each row contains an example.
        :return: A 1D Numpy array containing the corresponding predicted values for each example
        '''
        n_examples = len(X)
        n_hidden = self.hidden_size
        predictions = np.zeros((n_examples))

        for i in range(n_examples):
            a = np.matmul(self.layer1_weights,X[i]).reshape((n_hidden,1))+self.layer1_bias
            v = self.activation(a)
            predictions[i] = np.matmul(self.layer2_weights, v) + self.layer2_bias

        return predictions

    def loss(self, X, Y):
        '''
        Returns the total squared error on some dataset (X, Y).

        :param X: 2D Numpy array where each row contains an example
        :param Y: 1D Numpy array containing the corresponding values for each example
        :return: A float which is the squared error of the model on the dataset
        '''
        predictions = self.predict(X)
        return l2_loss(predictions, Y)

    def average_loss(self, X, Y):
        '''
        Returns the mean squared error on some dataset (X, Y).

        MSE = Total squared error/# of examples

        :param X: 2D Numpy array where each row contains an example
        :param Y: 1D Numpy array containing the corresponding values for each example
        :return: A float which is the mean squared error of the model on the dataset
        '''
        return self.loss(X, Y)/X.shape[0]
