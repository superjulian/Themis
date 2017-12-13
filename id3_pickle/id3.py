"""
id3
with pickling

Maria Stull
"""

import math
import random
import sys
import cPickle as pickle

#nodeVal.val = 0
def nodeVal():
    if not hasattr(nodeVal, "val"):
        nodeVal.val = 0
    nodeVal.val+=1
    return nodeVal.val

class Node():
    def __init__(self, attribute="", parents_attr=set()):
        self.has_next = False
        self.attributeName = attribute
        self.attributeNum = 0
        self.label = ""
        self.children = {}
        self.unusable_attr = parents_attr.union(set(attribute))
        self.name = nodeVal()

def readInput(datafile, labels, points, values):
    line = datafile.readline()
    while line != "":
        line = line.strip().replace('"', '')
        line = line.split(',')
        for i in range(0, len(line)):
            values[i].add(line[i])
        labels.add(line[0])
        points.append(line)
        line = datafile.readline()
        
def calculateEntropy(points, indices, labels):
    sum = 0.0
    total =  len(indices)
   # print "total: ", total
    #print points
    #print
    numWithLabel = {}
#    print 
    for label in labels:
        numWithLabel[label] = 0
    for i in indices:
        numWithLabel[points[i][0]]+=1
     #   print points[i]
   # print
    for label in labels:
        pSy = float(numWithLabel[label])/total
 #       print label, pSy
        if abs(pSy) <= 0.00005:
            sum += 0
        else:
            sum += pSy * math.log(pSy, 2)
#    print "entropy", sum
    return 0 - sum
        
# Return sum(over value in attribute) (|Sv|/|S| * H(Sv))
def calculateInfoGain(S, labels, values, attribute, splitSet):
    #print attribute
    indices = S[1]
    points = S[0]
    #for i in indices:
     #   print points[i]
    sum = 0.0
    num_elms = len(indices)
    gain = 0.0
    for v in values:
        #print v
        if (len(splitSet[v])==0):
            continue
        size_proportion = float(len(splitSet[v])) / float(len(indices))
        entropy = calculateEntropy(points, splitSet[v], labels)
        # print "prop", size_proportion
        gain += size_proportion * entropy
    return gain

def splitByValue(S, attribute, attr_vals):
    indices = S[1]
    points = S[0]
    splitVals = {}
    for val in attr_vals:
        splitVals[val] = set()
    for i in indices:
        splitVals[points[i][attribute]].add(i)
    return splitVals;


def findBestAttribute(S, labels, values, attributes, attribute_names, unusable_attr):
    best_attribute = ""
    best_attribute_score = 999999999999999999999999
    bestSplitSet = {}
    for attribute in attributes:
        if attribute not in unusable_attr:
            splitSet = splitByValue(S, attribute, values[attribute])
            gain = calculateInfoGain(S, labels, values[attribute], attribute, splitSet)
           # print "gain:", gain, "attribute:", attribute_names[attribute]
            # maximizing (0 - the part of gain equation we want to minimize) = maximizing gain (sorry this is gross)
            if gain < best_attribute_score:
                best_attribute_score = gain
                best_attribute = attribute
                bestSplitSet = splitSet
    return (best_attribute, bestSplitSet)

def leafMostCommonLabel(S, labels):
    points = S[0]
    indices = S[1]
    count = {}
    for l in labels:
        count[l] = 0
    for i in indices:
        count[points[i][0]]+=1
    best_label = ""
    best_count = 0
    for l in labels:
        #print l, count[l]
        if count[l] > best_count:
            best_label = l
            best_count = count[l]
            # print "best_label", best_label
    node = Node()
    node.label=best_label
    return node
        
def AllHaveSameLabel(S):
    points = S[0]
    indices = S[1]
    x = indices.pop()
    indices.add(x)
    label = points[x][0]
    for i in indices:
        if points[i][0] != label:
            return False
    return True

# S is (full training set (list of lists), indices being considered (set))
def buildTree(S, labels, values, attributes, attribute_names, unusable_attr):
   #  print "new node. attributes:", (attributes.difference(unusable_attr))
    if len(attributes.difference(unusable_attr)) == 0:
        return leafMostCommonLabel(S, labels)
    if AllHaveSameLabel(S):
        return leafMostCommonLabel(S, labels)
    best_attribute = findBestAttribute(S, labels, values, attributes, attribute_names, unusable_attr)
    attr = best_attribute[0]
    splitSet = best_attribute[1]
#    print "best attribute ", attribute_names[attr]

    root = Node()
    root.attributeName = attribute_names[attr]
    root.attributeNum = attr
    root.has_next = True
    # root.unusable_attr = unusable_attr
    for v in values[attr]:
        if(len(splitSet[v]) == 0):
            root.children[v] = leafMostCommonLabel(S, labels)
        else:
            Sv = (S[0], splitSet[v])
            child_unusable = unusable_attr.union(set([attr]))
            root.children[v] = buildTree(Sv, labels, values, attributes, attribute_names, child_unusable)
    return root
    

def printTree(tree, parent):
    if tree.has_next:
        print "attribute:", tree.attributeName.split("\r")[0], "name:", tree.name, "parent:", parent
        for value in tree.children:
            print "branch: ", value.split("\r")[0]
            printTree(tree.children[value], tree.name)
    else:
        print "label:", tree.label, "name:", tree.name, "parent: ", parent


def main():
    # Read parameters
    if len(sys.argv) <= 3:
        print("Usage: python id3.py dataset_filepath, training_percent, random_seed [p (to print tree)]")
        sys.exit(-1)
    filepath = sys.argv[1]
    training_pct = float(sys.argv[2])
    seed = int(sys.argv[3])
    
#    for seed in range(1, 51):
    random.seed(seed)

    output_tree = False

    if len(sys.argv) > 4:
        output_tree = sys.argv[4]=="p"

    # Open file
    datafile = open(filepath, 'r')
    line = datafile.readline().split(",")
    # num_attributes = len(line)-1
    attribute_names = line
    attribute_indices = set(range(1, len(line)))
    values = {}
    for i in attribute_indices:
        values[i] = set()
    values[0]=set()

    # Read input
    labels = set()
    points = []
    readInput(datafile, labels, points, values)

    # Separate into training and test_sets
    random.shuffle(points)
    training_index = int(len(points)*training_pct)
    training_set = points[:training_index]
    test_set = points[training_index:]
    
    # Create confusion matrix--keys are (predicted, actual)
    list_labels = list(labels)
    confusion_matrix = {}
    for x in list_labels:
        for y in list_labels:
            confusion_matrix[x+","+y] = 0

    # Build decision tree    
    indices = set(range(0, len(training_set)))
    S = (training_set, indices)
    tree = buildTree(S, list_labels, values, attribute_indices, attribute_names, set())

    mcl_node = leafMostCommonLabel(S, list_labels)
    most_common_label = mcl_node.label
#     print "mcl", most_common_label1
    
    data2save = (tree, most_common_label)
      
    output = open('data.pkl', 'wb')
    pickle.dump(data2save, output)
    output.close()
#     
#     if output_tree:
#         print "Printing tree: "
#         printTree(tree, "none")
# 
#     for point in test_set:
#         real_label = point[0]
#         predicted_label = ""
#         node = tree
#         while (predicted_label == ""):
#             if node.has_next:
#                 attribute = point[node.attributeNum]
#                 if attribute in node.children:
#                     node = node.children[attribute]
#                 else:
#                     predicted_label = most_common_label
#             else:
#                 predicted_label = node.label
#         confusion_matrix[predicted_label + "," + real_label] += 1
# 
#     # Output confusion matrix
#     output = ""
#     for label in list_labels:
#         output += label+","
#     output += "\n"
#     for actual in list_labels:
#         for predicted in list_labels:
#             output+=str(confusion_matrix[predicted + "," + actual]) + ","
#         output += actual + "\n"
# 
#     data_name = filepath.split(".")[0]
#     outfile_name = "results_" + data_name + "_" + str(seed) + ".csv"
#     outfile = open(outfile_name, "w")
#     outfile.write(output)
# 
#     # """  
#     n = len(test_set)
#     correct_predictions = 0
#     for label in list_labels:
#         correct_predictions += confusion_matrix[label + "," + label]
#     accuracy = float(correct_predictions) / n
#     print accuracy
#       
#     p = accuracy
#     root = ((p*(1-p))/n)**.5
#     root = 1.95*root
#     print "conf int: (", p- root, ",", p + root, ")"
    
        
        
       # print output
            
    
if (__name__ == "__main__"):
    main()
