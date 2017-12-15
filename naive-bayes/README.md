This folder contains the code for a naive-bayes classifier (not just for authors, lol), which can interface with 
Themis. The first program, nbayes.py, builds the model from a given dataset and pickles it. The dataset is assumed 
to be a csv file, where the first column is the value of a BINARY decision variable. In particular, it is assumed 
that this input file has been edited so that the decision variable is given as either 0 or 1. For example, one might 
input a modified Adult data set where the class "<=50K" has been changed to 0 and ">50K" has been changed to 1. To 
build the model, one should call the program in the following way:

      python3 nbayes.py data_file.csv percentage seed

where percentage is a decimal value denoting the amount of the dataset to use for training. 


The second program, pred-bayes.py is used to interface with Themis. It loads the pickled model and, given arbirtrary
Themis command line input representing an instance created in the Themis test set, predicts whether the instance is of 
class 0 or 1. 