import numpy as np
import matplotlib.pyplot as plt
from qp import solve_QP

def linear_kernel(xj, xk):
    """
    Kernel Function, linear kernel (ie: regular dot product)

    :param xj: an input sample (np array)
    :param xk: an input sample (np array)
    :return: float64
    """
    return np.dot(xj,xk)

def rbf_kernel(xj, xk, gamma = 0.01):
    """
    Kernel Function, radial basis function kernel or gaussian kernel

    :param xj: an input sample (np array)
    :param xk: an input sample (np array)
    :param gamma: parameter of the RBF kernel.
    :return: float64
    """
    d = np.linalg.norm(xj-xk)
    return np.exp(-gamma*d)

def polynomial_kernel(xj, xk, c = 0.5, d = 2):
    """
    Kernel Function, polynomial kernel

    :param xj: an input sample (np array)
    :param xk: an input sample (np array)
    :param c: mean of the polynomial kernel (np array)
    :param d: exponent of the polynomial (np array)
    :return: float64
    """
    return np.power(np.dot(xj,xk)+c,d)

class SVM(object):

    def __init__(self, kernel_func=linear_kernel, lambda_param=.1):
        self.kernel_func = kernel_func
        self.lambda_param = lambda_param

    def train(self, inputs, labels):
        """
        train the model with the input data (inputs and labels),
        find the coefficients and constaints for the quadratic program and
        calculate the alphas

        :param inputs: inputs of data, a numpy array
        :param labels: labels of data, a numpy array
        :return: None
        """
        self.train_inputs = inputs
        self.train_labels = labels
        self.n_examples = len(labels)

        # constructing QP variables
        G = self._get_gram_matrix()
        Q, c = self._objective_function(G)
        A, b = self._inequality_constraint(G)

        # TODO: Uncomment the next line when you have implemented _get_gram_matrix(),
        # _inequality_constraints() and _objective_function().
        result = solve_QP(Q, c, A, b)
        self.alpha = solve_QP(Q, c, A, b)[:self.train_inputs.shape[0]]


    def plot(self):
        postive = []
        negative = []
        for i in range(self.n_examples):
            if self.train_labels[i] == 1:
                postive.append(self.train_inputs[i])
            else:
                negative.append(self.train_inputs[i])
        
        postive_array = np.array(postive)
        negative_array = np.array(negative)

        x = np.linspace(-2,2,100)
        y = np.linspace(-2,2,100)
        xx,yy = np.meshgrid(x,y)
        xxx = xx.flatten()
        yyy = yy.flatten()
        coor = np.vstack([xxx,yyy]).T
        boundary = []

        for i in range(coor.shape[0]):
            sum = 0
            for j in range(self.n_examples):
                sum += self.alpha[j]*self.kernel_func(self.train_inputs[j],coor[i])
            if np.isclose(sum,0,atol=1e-1):
                boundary.append(coor[i])
        boundary_array = np.array(boundary)
        #z = np.polyfit(boundary_array[:,0], boundary_array[:,1], 10)
        #p = np.poly1d(z)
        #xp = np.linspace(-1.5,1.5)
        plt.scatter(postive_array[:,0], postive_array[:,1])
        plt.scatter(negative_array[:,0], negative_array[:,1])
        plt.scatter(boundary_array[:,0],boundary_array[:,1])
        plt.ylim(-2,2)
        plt.xlim(-2,2)
        plt.show()


    def _get_gram_matrix(self):
        """
        Generate the Gram matrix for the training data stored in self.train_inputs.

        Recall that element i, j of the matrix is K(x_i, x_j), where K is the
        kernel function.

        :return: the Gram matrix for the training data, a numpy array
        """

        G = np.zeros((self.n_examples,self.n_examples))

        for i in range(self.n_examples):
            for j in range(self.n_examples):
                G[i][j] = self.kernel_func(self.train_inputs[i], self.train_inputs[j])
        
        return G

    def _objective_function(self, G):
        """
        Generate the coefficients on the variables in the objective function for the
        SVM quadratic program.

        Recall the objective function is:
        minimize (1/2)x^T Q x + c^T x

        :param G: the Gram matrix for the training data, a numpy array
        :return: two numpy arrays, Q and c which fully specify the objective function
        """

        upper_left = np.multiply(G, 2*self.lambda_param)
        m = 2*self.n_examples    
        Q = np.zeros((m,m))

        for row in range(self.n_examples):
            for col in range(self.n_examples):
                Q[row][col] = upper_left[row][col]

        c = np.zeros((m))
        for i in range(self.n_examples,m):
            c[i] = 1.0/self.n_examples

        return Q,c

    def _inequality_constraint(self, G):
        """
        Generate the inequality constraints for the SVM quadratic program. The
        constraints will be enforced so that Ax <= b.

        :param G: the Gram matrix for the training data, a numpy array
        :return: two numpy arrays, A and b which fully specify the constraints
        """

        # TODO (hint: you can think of x as the concatenation of all the alphas and
        # all the all the xi's; think about what this implies for what A should look like.)
        m = 2*self.n_examples
        A = np.zeros((m,m))
        for i in range(0,self.n_examples):
            for j in range(0,self.n_examples):
                A[i][j] = -self.train_labels[i]*G[i][j]
        for i in range(0,self.n_examples):
            #A[i][0:self.n_examples] = np.multiply(G[i][:], -self.train_labels[i])
            A[i][i+self.n_examples] = -1
        for i in range(self.n_examples,m):
            A[i][i] = -1
                   
        b = np.zeros((m))
        for i in range(0,self.n_examples):
            b[i] = -1
        
        return A, b

    def predict(self, input):
        """
        Generate predictions given input.

        :param input: 2D Numpy array. Each row is a vector for which we output a prediction.
        :return: A 1D numpy array of predictions.
        """
        n_predictions = len(input)
        predictions = np.zeros((n_predictions))

        for i in range(n_predictions):
            sum = 0
            for j in range(self.n_examples):
                sum += self.alpha[j]*self.kernel_func(self.train_inputs[j],input[i])
            if sum>0:
                predictions[i] = 1
            else:
                predictions[i] = -1
        
        return predictions

    def accuracy(self, inputs, labels):
        """
        Calculate the accuracy of the classifer given inputs and their true labels.

        :param inputs: 2D Numpy array which we are testing calculating the accuracy of.
        :param labels: 1D Numpy array with the inputs corresponding true labels.
        :return: A float indicating the accuracy (between 0.0 and 1.0)
        """
        predictions = self.predict(inputs)
        n_examples = len(labels)
        count = 0.0
        for i in range(n_examples):
            if predictions[i] == labels[i]:
                count += 1
        return count/n_examples
