"""
    This is a file you will have to fill in.
    It contains helper functions required by K-means method via iterative improvement
"""
import numpy as np
from random import sample

def init_centroids(k, inputs):
    """
    Selects k random rows from inputs and returns them as the chosen centroids
    Hint: use random.sample (it is already imported for you!)
    :param k: number of cluster centroids
    :param inputs: a 2D Numpy array, each row of which is one input
    :return: a Numpy array of k cluster centroids, one per row
    """
    n_examples = len(inputs)
    indices = [i for i in range(n_examples)]
    centroids_indices = sample(indices,k)


    return np.array(inputs[centroids_indices])


def assign_step(inputs, centroids):
    """
    Determines a centroid index for every row of the inputs using Euclidean Distance
    :param inputs: inputs of data, a 2D Numpy array
    :param centroids: a Numpy array of k current centroids
    :return: a Numpy array of centroid indices, one for each row of the inputs
    """
    n_examples = len(inputs)
    n_centroids = len(centroids)
    centroid_indices = np.zeros((n_examples,))

    for i in range(n_examples):
        distance = np.zeros((n_centroids,))
        for j in range(n_centroids):
            distance[j] = np.linalg.norm(inputs[i]-centroids[j])
        centroid_indices[i] = np.argmin(distance)

    return centroid_indices

                


def update_step(inputs, indices, k):
    """
    Computes the centroid for each cluster
    :param inputs: inputs of data, a 2D Numpy array
    :param indices: a Numpy array of centroid indices, one for each row of the inputs
    :param k: number of cluster centroids, an int
    :return: a Numpy array of k cluster centroids, one per row
    """
    n_examples, n_features = inputs.shape
    centroids = np.zeros((k,n_features))

    for i in range(k):
        elements = []

        for j in range(n_examples):
            if indices[j] == i:
                elements.append(inputs[j])

        elements_array = np.array(elements)
        centroids[i] = np.mean(elements_array, axis=0)
    
    return centroids

        




def kmeans(inputs, k, max_iter, tol):
    """
    Runs the K-means algorithm on n rows of inputs using k clusters via iterative improvement
    :param inputs: inputs of data, a 2D Numpy array
    :param k: number of cluster centroids, an int
    :param max_iter: the maximum number of times the algorithm can iterate trying to optimize the centroid values, an int
    :param tol: relative tolerance with regards to inertia to declare convergence, a float number
    :return: a Numpy array of k cluster centroids, one per row
    """
    centroids = init_centroids(k,inputs)

    iter = 0
    converged = False
    while iter<max_iter and not converged:
        previous_centroids = centroids
        indices = assign_step(inputs, previous_centroids)
        centroids = update_step(inputs,indices,k)
        iter += 1
        flag = True

        for j in range(k):
            distance = np.linalg.norm(previous_centroids[j]-centroids[j])
            norm = np.linalg.norm(previous_centroids[j])
            if distance/norm > tol:
                flag = False 
        converged = flag

    return centroids