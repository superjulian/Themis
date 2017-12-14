#!/usr/bin/python3

#K nearest neighbor program
#Fall 2017
#By Julian Meltzer

import sys
import random
import math
import os
import pickle

def fail():
    print ("Usage: knn.py <file path> <{H,E}> <value of k>  <random seed>")
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

def predictLabel (distf, training_set, test_instance, k):
    counts = {}
    distances = (getDistances(distf, test_instance, training_set))
    for i in range (0, k):
        l = distances[i][0]
        counts[l] = counts.setdefault(l,0) + 1
    label = ("none", 0)
    for key in counts.keys():
        if counts[key] > label [1]:
            label = (key, counts[key])
    print (label[0])



def main():
    pickle_path = "knn.pickle"
    input_table=[]
    test_start=0
    ###If pickle file exists, make prediction
    if os.path.exists (pickle_path):
        with open (pickle_path, 'rb') as pickle_handle:
            distf, training_set, k = pickle.load(pickle_handle)
            length = len (training_set[0])
            instance = [0]* length
            print (length)
            print (instance)
            for i in range (len(sys.argv)):
                if i % 2 == 1:
                    print (i, sys.argv[i])
                    instance[int(sys.argv[i])] = sys.argv[i+1]
            print(instance)
            predictLabel(distf, training_set, instance, k)
            sys.exit(0)
    ###Otherwise make pickle file from dataset
    try: #get some command line inputs
        source = open(sys.argv[1], 'r')
        distance = sys.argv[2].lower()
        k = eval(sys.argv[3])
        seed = eval (sys.argv[4])
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
    atributes = input_table[0]
    #randomize it
    random.seed(seed)
    input_table = input_table[1:] #cut out first row
    random.shuffle(input_table)
    training_set = input_table
    with open (pickle_path, 'wb') as pickle_handle:
        pickle.dump((distf, training_set, k) , pickle_handle)
main()
