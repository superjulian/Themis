# id3 prediction for Themis

import cPickle as pickle
import sys

class Node():
    def __init__(self, attribute="", parents_attr=set()):
        self.has_next = False
        self.attributeName = attribute
        self.attributeNum = 0
        self.label = ""
        self.children = {}
        self.unusable_attr = parents_attr.union(set(attribute))
        self.name = nodeVal()

def main():

    # python loan.py race green age 18
    
    # Read in instance to predict
    num_attributes = int(float(len(sys.argv)-1)/2)
    
    point = [0]
    for i in range(1, len(sys.argv)):
        print i, sys.argv[i]
        if i%2==1:
            print "continue", i
            continue
        point.append(sys.argv[i])
    print point
        
    
    
    # Read in decision tree
    pkl_file = open('data.pkl', 'rb')
    data1 = pickle.load(pkl_file)
    pkl_file.close()
    #print data1
    tree = data1[0]
    most_common_label = data1[1]
    
        
    predicted_label = ""
    node = tree
    while (predicted_label == ""):
        if node.has_next:
            print node.attributeNum, point
            attribute = point[node.attributeNum]
            if attribute in node.children:
                node = node.children[attribute]
            else:
                predicted_label = most_common_label
        else:
            predicted_label = node.label
    
    print predicted_label

if (__name__ == "__main__"):
    main()