# Python 3.7
import numpy as np  # Used to perform efficient (and convenient) array and matrix operations.
from sklearn import datasets  # Used to load standard datasets.
from matplotlib import pyplot as plt  # Used to create plots.
import math  # Used for trigonometric functions, log, pow, etc.


def graph_iris_data():
	''' 
	function for graphing iris data. Fill this out to get a scatter plot of iris datapoints!
	'''

	iris = datasets.load_iris()
	data = iris.data
	xs = data[:, 0]
	ys = data[:, 1]  # Technically, we didn't need to make new_data before slicing these columns,

	# [TODO] plot iris data here

	plt.scatter(xs,ys,iris.target)

	plt.suptitle('Made by: B01532164')
	plt.xlabel('petal length')
	plt.ylabel('petal width')
	plt.show()


def graph_series_data():
	'''
	function for graphing series data
	'''

	xs = np.arange(100) * .5 - 10  # Creates a list of 100 values in intervals of .5, starting at -10.
	# Numpy makes it very easy (and efficient) to do elementwise operations on large datasets.
	y1s = [x*x for x in xs]  # If you are unfamiliar, this is called Python's "List Comprehension Syntax"
	y2s = [math.sin(x)*x*x for x in xs]
	# https://matplotlib.org/users/pyplot_tutorial.html is a good starting point for more info.
	
	# [TODO] plot series data here

	line1, = plt.plot(xs, y1s, '.r')
	line2, = plt.plot(xs, y2s, '-b')
	plt.suptitle('Made by: B01532164')
	plt.legend((line1,line2),(r'$x*x$',r'$sin(x)*x*x$'))

	plt.show()


if __name__ == '__main__':
	graph_iris_data()
	graph_series_data()
