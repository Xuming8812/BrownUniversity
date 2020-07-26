import numpy as np
import random
import copy
import math

def train_error(prob):
    '''
        TODO:
        Calculate the train error of the subdataset and return it.
        For a dataset with two classes, C(p) = min{p, 1-p}
    '''
    return min(prob,1-prob)


def entropy(prob):
    '''
        TODO:
        Calculate the entropy of the subdataset and return it.
        For a dataset with 2 classes, C(p) = -p * log(p) - (1-p) * log(1-p)
        For the purposes of this calculation, assume 0*log0 = 0.
    '''
    if prob <= 0 or prob >= 1:
        return 0
    return -prob*math.log(prob) - (1-prob)*math.log(1-prob)


def gini_index(prob):
    '''
        TODO:
        Calculate the gini index of the subdataset and return it.
        For dataset with 2 classes, C(p) = 2 * p * (1-p)
    '''
    return 2*prob*(1-prob)



class Node:
    '''
    Helper to construct the tree structure.
    '''
    def __init__(self, left=None, right=None, depth=0, index_split_on=0, isleaf=False, label=1):
        self.left = left
        self.right = right
        self.depth = depth
        self.index_split_on = index_split_on
        self.isleaf = isleaf
        self.label = label
        self.info = {} # used for visualization


    def _set_info(self, gain, num_samples):
        '''
        Helper function to add to info attribute.
        You do not need to modify this. 
        '''

        self.info['gain'] = gain
        self.info['num_samples'] = num_samples


class DecisionTree:

    def __init__(self, data, validation_data=None, gain_function=entropy, max_depth=40):
        self.max_depth = max_depth
        self.root = Node()
        self.gain_function = gain_function

        indices = list(range(1, len(data[0])))

        self._split_recurs(self.root, data, indices)

        # Pruning
        if validation_data is not None:
            self._prune_recurs(self.root, validation_data)


    def predict(self, features):
        '''
        Helper function to predict the label given a row of features.
        You do not need to modify this.
        '''
        return self._predict_recurs(self.root, features)


    def accuracy(self, data):
        '''
        Helper function to calculate the accuracy on the given data.
        You do not need to modify this.
        '''
        return 1 - self.loss(data)


    def loss(self, data):
        '''
        Helper function to calculate the loss on the given data.
        You do not need to modify this.
        '''
        cnt = 0.0
        test_Y = [row[0] for row in data]
        for i in range(len(data)):
            prediction = self.predict(data[i])
            if (prediction != test_Y[i]):
                cnt += 1.0
        return cnt/len(data)


    def _predict_recurs(self, node, row):
        '''
        Helper function to predict the label given a row of features.
        Traverse the tree until leaves to get the label.
        You do not need to modify this.
        '''
        if node.isleaf or node.index_split_on == 0:
            return node.label
        split_index = node.index_split_on
        if not row[split_index]:
            return self._predict_recurs(node.left, row)
        else:
            return self._predict_recurs(node.right, row)


    def _prune_recurs(self, node, validation_data):
        '''
        TODO:
        Prune the tree bottom up recursively. Nothing needs to be returned.
        Do not prune if the node is a leaf.
        Do not prune if the node is non-leaf and has at least one non-leaf child.
        Prune if deleting the node could reduce loss on the validation data.
        '''
        # #Do not prune if the node is a leaf.
        # if node.isleaf:
        #     return
        # #Do not prune if the node is non-leaf and has at least one non-leaf child.
        # if not node.isleaf:
        #     if not (node.left.isleaf and node.right.isleaf):
        #         return

        # #recursively prune 
        # self._prune_recurs(node.left, validation_data)
        # self._prune_recurs(node.right, validation_data)

        # #if both children are leaves
        # old_loss = self.loss(validation_data)
        # #set the node to leaf and set the label to 1
        # node.isleaf = True
        # node.label = 1
        # new_loss_1 = self.loss(validation_data)
        # #set the node to leaf and set the label to 0
        # node.isleaf = True
        # node.label = 0
        # new_loss_0 = self.loss(validation_data)

        # min_loss = new_loss_0 if new_loss_0<new_loss_1 else new_loss_1
        # min_loss_label = 0 if new_loss_0<new_loss_1 else 1
        # #prune the node
        # if min_loss<old_loss:
        #     node.isleaf = True
        #     node.label = min_loss_label
        # else:
        #     node.isleaf = False

        #Do not prune if the node is a leaf.
        if node.isleaf:
            return
        #recursively children nodes 
        self._prune_recurs(node.left,validation_data)
        self._prune_recurs(node.right,validation_data)

        #if both children are leaves
        if node.left.isleaf and node.right.isleaf:

            old_loss = self.loss(validation_data)
            #set the node to leaf and set the label to 1
            node.isleaf = True
            node.label = 1

            new_loss_1 = self.loss(validation_data)
            #set the node to leaf and set the label to 0
            node.label = 0
            new_loss_0 = self.loss(validation_data)
            #reset the node
            node.isleaf = False
            node.label = -1
            #delete the node by replacing it by the left child
            tempNode = node
            node = node.left
            new_loss_left = self.loss(validation_data)
            #delete the node by replacing it by the right child
            node = node.right
            new_loss_right = self.loss(validation_data)
            #reset the node
            node = tempNode
            #find the minimum loss
            all_loss = np.array([old_loss,new_loss_0,new_loss_1,new_loss_left,new_loss_right])
            min_loss = np.argmin(all_loss)
            #configure the node by minimum loss
            if min_loss == 0:
                node.isleaf = False
                node.label = -1
            elif min_loss == 1:
                node.isleaf = True
                node.label = 0
            elif min_loss == 2:
                node.isleaf = True
                node.label = 1
            elif min_loss == 3:
                node.isleaf = False
                node = node.left
                node.label = -1
            else:
                node.isleaf = False
                node = node.right
                node.label = -1

    def _is_terminal(self, node, data, indices):
        '''
        TODO:
        Helper function to determine whether the node should stop splitting.
        Stop the recursion if:
            1. The dataset is empty.
            2. There are no more indices to split on.
            3. All the instances in this dataset belong to the same class
            4. The depth of the node reaches the maximum depth.
        Return:
            - A boolean, True indicating the current node should be a leaf.
            - A label, indicating the label of the leaf (or the label it would 
              be if we were to terminate at that node)
        '''
        # if dataset is empty
        if len(data) == 0: 
            return (True,random.randint(0,1))
        #if all instances belong to the same class
        if all(d[0] == data[0][0] for d in data): 
            return (True,data[0][0]) 
        #if there are no more indices to split on, or the depth of the node reaches the maximum depth
        if len(indices) == 0 or node.depth > self.max_depth:
            frac = self._vote_by_majority(data)
            if frac <= 0.5:
                c = 0
            else:
                c = 1
            return (True,c)
        else:
            return (False,-1)

    def _vote_by_majority(self,data):
        m = len(data)
        count = 0
        for row in data:
            if row[0] == 1:
                count += 1
        frac = count / m
        return frac

    def _split_recurs(self, node, data, indices):
        '''
        TODO:
        Recursively split the node based on the rows and indices given.
        Nothing needs to be returned.

        First use _is_terminal() to check if the node needs to be split.
        If so, select the column that has the maximum infomation gain to split on.
        Store the label predicted for this node, the split column, and use _set_info()
        to keep track of the gain and the number of datapoints at the split.
        Then, split the data based on its value in the selected column.
        The data should be recursively passed to the children.
        '''
        (is_terminate,label) = self._is_terminal(node,data,indices)
        node.isleaf = is_terminate

        if is_terminate:          
            node.label = label
            node._set_info(0,0)
        else:
            #initialize the max_attribute and max_gain
            max_attribute = indices[0]
            max_gain = -math.inf
            #check each index and its gain
            for index in indices:
                current_gain = self._calc_gain(data,index,self.gain_function)
                if current_gain >= max_gain:
                    max_gain = current_gain
                    max_attribute = index
            
            node._set_info(max_gain, len(data))
            #count the votes by majority to decide the label
            fraction = self._vote_by_majority(data)
            if fraction <= 0.5:
                node.label = 0
            else:
                node.label = 1

            node.index_split_on = max_attribute 

            #split the data based on the value of selected max_attribute
            left_rows = []
            right_rows = []
            for row in range(0,len(data)):
                if data[row][max_attribute]:
                    right_rows.append(data[row])
                else:
                    left_rows.append(data[row])

            new_indices = [index for index in indices if index != max_attribute]

            #recursively split
            node.left = Node(depth=node.depth+1)
            self._split_recurs(node.left,left_rows,new_indices)
            node.right = Node(depth=node.depth+1) 
            self._split_recurs(node.right,right_rows,new_indices)


    def _calc_gain(self, data, split_index, gain_function):
        '''
        TODO:
        Calculate the gain of the proposed splitting and return it.
        Gain = C(P[y=1]) - (P[x_i=True] * C(P[y=1|x_i=True]) + (P[x_i=False] * C(P[y=1|x_i=False]))
        Here the C(p) is the gain_function. For example, if C(p) = min(p, 1-p), this would be
        considering training error gain. Other alternatives are entropy and gini functions.
        '''
        m = len(data)
        if m == 0:
            return 0

        count_x_true = 0
        count_y_1_x_true = 0
        count_y_1_x_false = 0
        for row in range(0,m):
            #count the number of x_i = 1
            if data[row][split_index]:
                count_x_true += 1
                #count the number of y = 1 given x_i = 1
                if data[row][0] == 1:
                    count_y_1_x_true += 1
            else:
                if data[row][0] == 1:
                    count_y_1_x_false += 1

        #calculate the prob of all needed situations
        prob_y_1 = (count_y_1_x_true + count_y_1_x_false)/m 
        prob_x_true = count_x_true/m
        prob_x_false = 1-prob_x_true          
        prob_y_1_x_true = count_y_1_x_true/count_x_true if prob_x_true > 0 else 0
        prob_y_1_x_false = count_y_1_x_false/(m - count_x_true) if prob_x_false > 0 else 0
        #use given function to calculate cp
        cp_y_1 = gain_function(prob_y_1) 
        cp_y_1_x_true = gain_function(prob_y_1_x_true)
        cp_y_1_x_false = gain_function(count_y_1_x_false)

        # compute CPtrue and CPfalse
        gain = abs(cp_y_1 - prob_x_true*cp_y_1_x_true + prob_x_false*cp_y_1_x_false)
        return gain
    

    def print_tree(self):
        '''
        Helper function for tree_visualization.
        Only effective with very shallow trees.
        You do not need to modify this.
        '''
        print('---START PRINT TREE---')
        def print_subtree(node, indent=''):
            if node is None:
                return str("None")
            if node.isleaf:
                return str(node.label)
            else:
                decision = 'split attribute = {:d}; gain = {:f}; number of samples = {:d}'.format(node.index_split_on, node.info['gain'], node.info['num_samples'])
            left = indent + '0 -> '+ print_subtree(node.left, indent + '\t\t')
            right = indent + '1 -> '+ print_subtree(node.right, indent + '\t\t')
            return (decision + '\n' + left + '\n' + right)

        print(print_subtree(self.root))
        print('----END PRINT TREE---')


    def loss_plot_vec(self, data):
        '''
        Helper function to visualize the loss when the tree expands.
        You do not need to modify this.
        '''
        self._loss_plot_recurs(self.root, data, 0)
        loss_vec = []
        q = [self.root]
        num_correct = 0
        while len(q) > 0:
            node = q.pop(0)
            num_correct = num_correct + node.info['curr_num_correct']
            loss_vec.append(num_correct)
            if node.left != None:
                q.append(node.left)
            if node.right != None:
                q.append(node.right)

        return 1 - np.array(loss_vec)/len(data)


    def _loss_plot_recurs(self, node, rows, prev_num_correct):
        '''
        Helper function to visualize the loss when the tree expands.
        You do not need to modify this.
        '''
        labels = [row[0] for row in rows]
        curr_num_correct = labels.count(node.label) - prev_num_correct
        node.info['curr_num_correct'] = curr_num_correct

        if not node.isleaf:
            left_data, right_data = [], []
            left_num_correct, right_num_correct = 0, 0
            for row in rows:
                if not row[node.index_split_on]:
                    left_data.append(row)
                else:
                    right_data.append(row)

            left_labels = [row[0] for row in left_data]
            left_num_correct = left_labels.count(node.label)
            right_labels = [row[0] for row in right_data]
            right_num_correct = right_labels.count(node.label)

            if node.left != None:
                self._loss_plot_recurs(node.left, left_data, left_num_correct)
            if node.right != None:
                self._loss_plot_recurs(node.right, right_data, right_num_correct)
