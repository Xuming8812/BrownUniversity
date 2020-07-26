import random
import numpy as np
import matplotlib.pyplot as plt

from get_data import get_data
from models import DecisionTree, train_error, entropy, gini_index


def loss_plot(ax, title, tree, pruned_tree, train_data, test_data):
    '''
        Example plotting code. This plots four curves: the training and testing
        average loss using tree and pruned tree.
        You do not need to change this code!
        Arguments:
            - ax: A matplotlib Axes instance.
            - title: A title for the graph (string)
            - tree: An unpruned DecisionTree instance
            - pruned_tree: A pruned DecisionTree instance
            - train_data: Training dataset returned from get_data
            - test_data: Test dataset returned from get_data
    '''
    fontsize=8
    ax.plot(tree.loss_plot_vec(train_data), label='train non-pruned')
    ax.plot(tree.loss_plot_vec(test_data), label='test non-pruned')
    ax.plot(pruned_tree.loss_plot_vec(train_data), label='train pruned')
    ax.plot(pruned_tree.loss_plot_vec(test_data), label='test pruned')


    ax.locator_params(nbins=3)
    ax.set_xlabel('number of nodes', fontsize=fontsize)
    ax.set_ylabel('loss', fontsize=fontsize)
    ax.set_title(title, fontsize=fontsize)
    legend = ax.legend(loc='upper center', shadow=True, fontsize=fontsize-2)

def explore_dataset(filename, class_name):
    train_data, validation_data, test_data = get_data(filename, class_name)

    # TODO: Print 12 loss values associated with the dataset.
    # For each measure of gain (training error, entropy, gini):
    #      (a) Print average training loss (not-pruned)
    #      (b) Print average test loss (not-pruned)
    #      (c) Print average training loss (pruned)
    #      (d) Print average test loss (pruned)

    # TODO: Feel free to print or plot anything you like here. Just comment
    # make sure to comment it out, or put it in a function that isn't called
    # by default when you hand in your code!
    
    print("For dataset of "+ filename + ":")
    #Training error
    print("Training error measurement of gain")
    tree_training_error = DecisionTree(train_data,gain_function=train_error)
    print("Training loss(not-pruned) = " + str(tree_training_error.loss(train_data)))
    print("Test loss(not-pruned) = " + str(tree_training_error.loss(test_data)))
    tree_training_error_pruned = DecisionTree(train_data, validation_data = validation_data, gain_function=train_error)
    print("Training loss(pruned) = " + str(tree_training_error_pruned.loss(train_data)))
    print("Test loss(pruned) = " + str(tree_training_error_pruned.loss(test_data)))
    print("")
    #Entropy
    print("Entropy measurement of gain")
    tree_entropy = DecisionTree(train_data,gain_function=entropy)
    print("Training loss(not-pruned) = " + str(tree_entropy.loss(train_data)))
    print("Test loss(not-pruned) = " + str(tree_entropy.loss(test_data))) 
    tree_entropy_pruned = DecisionTree(train_data, validation_data = validation_data, gain_function=entropy)
    print("Training loss(pruned) = " + str(tree_entropy_pruned.loss(train_data)))
    print("Test loss(pruned) = " + str(tree_entropy_pruned.loss(test_data)))
    print("")
    #Gini
    print("Gini measurement of gain")
    tree_gini = DecisionTree(train_data,gain_function=gini_index)
    print("Training loss(not-pruned) = " + str(tree_gini.loss(train_data)))
    print("Test loss(not-pruned) = " + str(tree_gini.loss(test_data)))   
    tree_gini_pruned = DecisionTree(train_data, validation_data = validation_data, gain_function=gini_index)
    print("Training loss(not-pruned) = " + str(tree_gini_pruned.loss(train_data)))
    print("Test loss(not-pruned) = " + str(tree_gini_pruned.loss(test_data)))  
    print("")

    #question2
    # if filename == 'data/spam.csv':
    #     loss = []
    #     for i in range(1,16):
    #         tree = DecisionTree(train_data,gain_function=entropy,max_depth = i)
    #         loss.append(tree.loss(train_data))
    #     print(loss)
    #     x = np.arange(1,16)
    #     plt.plot(x, np.array(loss))
    #     plt.axis([0, 16, 0, 0.25])
    #     plt.xlabel('max depth of decision tree')
    #     plt.ylabel('training loss')
    #     plt.show()



def main():
    ########### PLEASE DO NOT CHANGE THESE LINES OF CODE! ###################
    random.seed(1)
    np.random.seed(1)
    #########################################################################

    explore_dataset('data/chess.csv', 'won')
    explore_dataset('data/spam.csv', '1')



main()
