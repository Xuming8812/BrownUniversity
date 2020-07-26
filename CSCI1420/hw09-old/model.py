import numpy as np
from qp import solve_QP

def linear_kernel(xj, xk):
    """
    Kernel Function, linear kernel (ie: regular dot product)

    :param xj: an input sample (np array)
    :param xk: an input sample (np array)
    :return: float64
    """
    return np.dot(xj,xk)

def rbf_kernel(xj, xk, gamma = 0.1):
    """
    Kernel Function, radial basis function kernel or gaussian kernel

    :param xj: an input sample (np array)
    :param xk: an input sample (np array)
    :param gamma: parameter of the RBF kernel.
    :return: float64
    """
    d = np.linalg.norm(xj-xk)
    return np.exp(-gamma*d)

def polynomial_kernel(xj, xk, c = 0, d = 1):
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
        Q, c = self._objective_function()
        A, b = self._inequality_constraints()
        E, d = self._equality_constraints()
        # TODO: Uncomment the next line when you have implemented _objective_function(),
        # _inequality_constraints() and _equality_constraints().
        self.alphas = solve_QP(Q, c, A, b, E, d)

        index = 0
        #find the alpha that between 0 and 1/2*n*lambda
        for i in range(self.n_examples):
            if not np.isclose(self.alphas[i], 0, atol=1e-3) and not np.isclose(self.alphas[i], 1/(2*self.n_examples*self.lambda_param), atol=1e-3):
                index = i
                break
        
        sum = 0
        for i in range(self.n_examples):
            sum += self.alphas[i]*(2*labels[i]-1)*self.kernel_func(inputs[index], inputs[i])
        self.bias = sum - (2*labels[index]-1)

    def _objective_function(self):
        """
        Generate the coefficients on the variables in the objective function for the
        SVM quadratic program.

        Recall the objective function is:
        minimize (1/2)x^T Q x + c^T x

        For specifics on the values for Q and c, see the objective function in the handout.

        :return: two numpy arrays, Q and c which fully specify the objective function.
        """
        x = self.train_inputs
        y = self.train_labels
        Q = np.zeros((self.n_examples,self.n_examples))
        for i in range(self.n_examples):
            for j in range(self.n_examples):
                Q[i][j] = (2*y[i]-1)*(2*y[j]-1)*self.kernel_func(x[j],x[i])
        c = np.ones((self.n_examples))
        c = np.multiply(c, -1)
        return Q, c

    def _equality_constraints(self):
        """
        Generate the equality constraints for the SVM quadratic program. The
        constraints will be enforced so that Ex = d.

        For specifics on the values for E and d, see the constraints in the handout

        :return: two numpy arrays, E, the coefficients, and d, the values
        """
        E = np.zeros((1,self.n_examples))
        for i in range(self.n_examples):
            E[0][i] = 2*self.train_labels[i]-1

        d = np.array([0.0])     
        return E, d


    def _inequality_constraints(self):
        """
        Generate the inequality constraints for the SVM quadratic program. The
        constraints will be enforced so that Ax <= b.

        For specifics on the values of A and b, see the constraints in the handout

        :return: two numpy arrays, A, the coefficients, and b, the values
        """
        m = 2*self.n_examples
        A = np.zeros((m,self.n_examples))
        for i in range(self.n_examples):
            A[i][i] = 1
            A[i+self.n_examples][i] = -1
        r = 1/(2*self.n_examples*self.lambda_param)
        b = np.zeros((m))
        for i in range(self.n_examples):
            b[i] = r  
        return A, b

    def predict(self, input):
        """
        Generate predictions given input.

        :param input: 2D Numpy array. Each row is a vector for which we output a prediction.
        :return: A 1D numpy array of predictions.
        """
        n_predictions = len(input)
        predictions = np.zeros((n_predictions))
        x = self.train_inputs
        y = self.train_labels

        for i in range(n_predictions):
            sum = 0
            for j in range(self.n_examples):
                sum += self.alphas[j]*(2*y[j]-1)*self.kernel_func(x[j],input[i])
            c = sum - self.bias
            if c>0:
                predictions[i] = 1
        
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

