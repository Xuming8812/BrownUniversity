import numpy as np

class NaiveBayes(object):
    """ Bernoulli Naive Bayes model
    @attrs:
        n_classes: the number of classes
    """

    def __init__(self, n_classes):
        """ Initializes a NaiveBayes model with n_classes. """
        self.n_classes = n_classes
        self.py = np.zeros(n_classes)
        self.px = np.zeros((n_classes,69))

    def train(self, X_train, y_train):
        """ Trains the model, using maximum likelihood estimation.
        @params:
            X_train: a n_examples x n_attributes numpy array
            y_train: a n_examples numpy array
        @return:
            a tuple consisting of:
                1) a 2D numpy array of the attribute distributions
                2) a 1D numpy array of the priors distribution
        """
        
        (n_examples,n_features) = X_train.shape
        #np.reshape(self.px, (self.n_classes, n_features))
        #count py for each class 
        label, count = np.unique(y_train, return_counts=True)
        for i in label:
            #apply laplace smoothing here
            self.py[i] = (count[i]+1)/(n_examples+self.n_classes)

        #count px given y
        for i in range(n_examples):
            example = X_train[i]
            for j in range(len(example)):
                if example[j] == 1:
                    self.px[y_train[i]][j] += 1
        #apply laplace smoothing again
        for i in range(self.n_classes):
            features = self.px[i]
            for j in range(n_features):
                self.px[i][j] = (features[j]+1)/(count[i]+self.n_classes)
        



    def predict(self, inputs):
        """ Outputs a predicted label for each input in inputs.

        @params:
            inputs: a NumPy array containing inputs
        @return:
            a numpy array of predictions
        """
        n_examples = len(inputs)
        predictions = np.zeros(n_examples)
        #loop each example
        for index in range(n_examples):
            example = inputs[index]

            px = np.copy(self.px)
            py = np.zeros(self.n_classes)
            #loop each attribute
            for attr in range(len(example)):
                #flip
                if example[attr] == 0:
                    px[:,attr] = np.subtract(1, self.px[:,attr])
            #find the max prob to decide class
            for label in range(self.n_classes):
                p = px[label]
                #use log
                p = np.log(p)
                py[label] = np.log(self.py[label])+np.sum(p)

            predictions[index] = np.argmax(py)

        return predictions

    def accuracy(self, X_test, y_test):
        """ Outputs the accuracy of the trained model on a given dataset (data).

        @params:
            X_test: 2D numpy array of examples
            y_test: numpy array of labels
        @return:
            a float number indicating accuracy (between 0 and 1)
        """
        n_examples = len(X_test)
        predictions = self.predict(X_test)
        count = 0

        for i in range(n_examples):
            if(predictions[i] == y_test[i]):
                count = count+1
        return count/n_examples

    def print_fairness(self, X_test, y_test, x_sens):
        """ 
        ***DO NOT CHANGE what we have implemented here.***
        
        Prints measures of the trained model's fairness on a given dataset (data).

        For all of these measures, x_sens == 1 corresponds to the "privileged"
        class, and x_sens == 1 corresponds to the "disadvantaged" class. Remember that
        y == 1 corresponds to "good" credit. 

        @params:
            X_test: 2D numpy array of examples
            y_test: numpy array of labels
            x_sens: numpy array of sensitive attribute values
        @return:

        """
        predictions = self.predict(X_test)

        # Disparate Impact (80% rule): A measure based on base rates: one of
        # two tests used in legal literature. All unprivileged lasses are
        # grouped together as values of 0 and all privileged classes are given
        # the class 1. . Given data set D = (X,Y, C), with protected
        # attribute X (e.g., race, sex, religion, etc.), remaining attributes Y,
        # and binary class to be predicted C (e.g., “will hire”), we will say
        # that D has disparate impact if:
        # P[Y^ = 1 | S != 1] / P[Y^ = 1 | S = 1] <= (t = 0.8). 
        # Note that this 80% rule is based on US legal precedent; mathematically,
        # perfect "equality" would mean

        di = np.mean(predictions[np.where(x_sens==0)])/np.mean(predictions[np.where(x_sens==1)])
        print("Disparate impact: " + str(di))

        # Group-conditioned error rates! False positives/negatives conditioned on group
        
        pred_priv = predictions[np.where(x_sens==1)]
        pred_unpr = predictions[np.where(x_sens==0)]
        y_priv = y_test[np.where(x_sens==1)]
        y_unpr = y_test[np.where(x_sens==0)]

        # s-TPR (true positive rate) = P[Y^=1|Y=1,S=s]
        priv_tpr = np.sum(np.logical_and(pred_priv == 1, y_priv == 1))/np.sum(y_priv)
        unpr_tpr = np.sum(np.logical_and(pred_unpr == 1, y_unpr == 1))/np.sum(y_unpr)

        # s-TNR (true negative rate) = P[Y^=0|Y=0,S=s]
        priv_tnr = np.sum(np.logical_and(pred_priv == 0, y_priv == 0))/(len(y_priv) - np.sum(y_priv))
        unpr_tnr = np.sum(np.logical_and(pred_unpr == 0, y_unpr == 0))/(len(y_unpr) - np.sum(y_unpr))

        # s-FPR (false positive rate) = P[Y^=1|Y=0,S=s]
        priv_fpr = 1 - priv_tnr 
        unpr_fpr = 1 - unpr_tnr 

        # s-FNR (false negative rate) = P[Y^=0|Y=1,S=s]
        priv_fnr = 1 - priv_tpr 
        unpr_fnr = 1 - unpr_tpr

        print("FPR (priv, unpriv): " + str(priv_fpr) + ", " + str(unpr_fpr))
        print("FNR (priv, unpriv): " + str(priv_fnr) + ", " + str(unpr_fnr))
    
    
        # #### ADDITIONAL MEASURES IF YOU'RE CURIOUS #####

        # Calders and Verwer (CV) : Similar comparison as disparate impact, but
        # considers difference instead of ratio. Historically, this measure is
        # used in the UK to evalutate for gender discrimination. Uses a similar
        # binary grouping strategy. Requiring CV = 1 is also called demographic
        # parity.

        cv = 1 - (np.mean(predictions[np.where(x_sens==1)]) - np.mean(predictions[np.where(x_sens==0)]))

        # Group Conditioned Accuracy: s-Accuracy = P[Y^=y|Y=y,S=s]

        priv_accuracy = np.mean(predictions[np.where(x_sens==1)] == y_test[np.where(x_sens==1)])
        unpriv_accuracy = np.mean(predictions[np.where(x_sens==0)] == y_test[np.where(x_sens==0)])

        return predictions
