#!/usr/bin/python3

#K nearest neighbor program
#Fall 2017
#By Julian Meltzer

import sys
import random
import math

def fail():
    print ("Usage: knn.py <file path> <{H,E}> <value of k> <% of instances for training> <random seed>")
    sys.exit(1)

def hamming(first, second):
    dist = 0
    for i in range (1, len (first)):
        if first[i] != second [i]:
            dist+=1
    return dist

def euclid(first, second):
    dist = 0
    try:
        for i in range (1, len(first)):
            dist += abs( first[i] - second[i]) ** 2
        return math.sqrt(dist)
    except TypeError:
        print ("Error: Your data contains nominal atributes, please use the Hamming distance fuction.")
        sys.exit(1)

#returns a sorted list of distances from item to each thing in training set
def getDistances(distf, item, training_set):
    distances=[]
    for element in training_set:
        distances.append((element[0], distf(item, element)))
    distances.sort(key=lambda tup: tup[1]) #sorts list by second element of each tuple
    #Source: https://stackoverflow.com/questions/3121979/how-to-sort-list-tuple-of-lists-tuples

    return distances

def predictLabels (distf, training_set, test_set, k, labels):
    predicted_labels=[]
    counts={}
    for item in test_set:
        distances = (getDistances(distf, item, training_set))
        for i in range (0, k):
            l = distances[i][0]
            counts[l] = counts.setdefault(l,0) + 1
        label = ("none", 0)
        for key in counts.keys():
            if counts[key] > label [1]:
                label = (key, counts[key])
        counts.clear()
        predicted_labels.append(label[0])
    return (predicted_labels)

def cMatrix(predicted_labels, test_set, labels):
    #make 2d dictionary. Outer dict is actual labels as keys and values are each an inner dictionary of predicted labels and counts
    matrix = {}
    
    #should intialize keys in the inner and outer dictionaries automatically. Only the outer dictionary is garenteed a label for every key
    for i in range (0, len(test_set)):
        label_dict = matrix.setdefault(test_set[i][0], dict()) 
        # grab dict assosiated w actual label, initializing a new one if nessisary
        
        label_dict [predicted_labels[i]] = label_dict.get(predicted_labels[i], 0) + 1 
        #increment actual label x predicted label count init if needed

    return matrix


def printMatrix (cMatrix):
    labels = sorted (cMatrix.keys())
    matrix_string=""
    for label in labels:
        matrix_string = matrix_string + label + ","
    matrix_string += '\n'
    for actual in list(labels):
        row=""
        for pred in list(labels):
            row = row + str(cMatrix[actual].get(pred, 0)) + ","
        matrix_string += row + actual + '\n'
    return matrix_string

def main():
    input_table=[]
    test_start=0
    try: #get some command line inputs
        output= open ("results"+"_"+sys.argv[1]+"_"+sys.argv[3]+"_"+sys.argv[5]+".csv", 'w')
        source = open(sys.argv[1], 'r')
        distance = sys.argv[2].lower()
        k = eval(sys.argv[3])
        percent = eval (sys.argv[4])
        seed = eval (sys.argv[5])
    except: #exit if they are broken
        fail()
    #pick distance function
    if distance=="h":
        distf=hamming
    elif distance=="e":
        distf=euclid
    else:
        fail()
    if k <= 0:
        fail()
    if percent <= 0 or percent >= 1:
        fail()

    #read in data
    for line in source:
        line = line.rstrip('\n')
        row=line.split(',')
        new_row=[]
        for item in row:
            if item[0] == '\"':
                new_row.append(item.rstrip('\"').lstrip('\"'))
            else:
                new_row.append(eval (item))
        input_table.append(new_row)
    labels = input_table[0]
    #randomize it
    random.seed(seed)
    input_table = input_table[1:] #cut out first row
    random.shuffle(input_table)
    test_start=int (len(input_table) * percent)
    #if test_start < 1:
    #    print ("Error: The specified percent results in an empty training set.")
    #    sys.exit(1)
    #if test_start >= len(input_table):
    #    print ("Error: The specified percent results in an empty test set.")
    #training_set = input_table [0:test_start]
    training_set = input_table [0:test_start] 
    #test_set= input_table [test_start:]
    predicted_labels = predictLabels (distf, training_set, test_set, k, labels)
    M=cMatrix (predicted_labels, test_set, labels) 
    output.write(printMatrix(M))    
main()
