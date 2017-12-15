import sys
import random
import math
import pickle
from collections import  OrderedDict

def create_instances(data_file):
    dataset = open(data_file, 'r')
    instances = []
    attributes = dataset.readline().strip().replace('\"', '').split(',')[1:]
    label_counts = OrderedDict()

    for line in dataset:
        line = line.strip().replace('\"', '').split(',')
        instance = (line[1:], line[0])

        if instance[1] in label_counts:
            label_counts[instance[1]] += 1
        else:
            label_counts[instance[1]] = 1

        instances.append(instance)

    return attributes, label_counts, instances

def split_data(instances, percent, seed):
    random.seed(seed)
    random.shuffle(instances)

    training, test = [], []
    cut_off = int(len(instances) * percent)
    training = [instances[i] for i in range(cut_off)]
    test = [instances[i] for i in range(cut_off, len(instances))]

    return training, test

def create_model(attributes, label_counts, training):
    model = {}
    for label in label_counts:
        model[label] = {}
        for attribute in attributes:
            model[label][attribute] = {}

    for instance in training:
        label = instance[1]

        for i in range(len(instance[0])):
            attribute = attributes[i]
            value = instance[0][i]
            if value in model[label][attribute]:
                model[label][attribute][value] +=1
            else:
                model[label][attribute][value] = 1


    return model

def calculate_probability(instance, label, label_count, model, attributes):
    prob_sum = 0
    for i in range(len(attributes)):
        attr = attributes[i]
        val = instance[0][i]
        if val in model[label][attr]:
            count = model[label][attr][val] + 1
        else:
            count = 1

        prob = count / (label_count + len(model[label][attr]))
        prob_sum += math.log(prob)

        #print(attr, len(model[label][attr]))
        #print(attr, count)

    return prob_sum


def predict(instance, attributes, label_counts, total_labels, model):
    max_prob = -1 * sys.maxsize
    max_label = ""

    for label in label_counts:
        label_frac = label_counts[label] / total_labels
        label_prob = math.log(label_frac)
        prob = calculate_probability(instance, label, label_counts[label], model, attributes)
        if prob > max_prob:
            max_prob = prob
            max_label = label

    return max_label


def main():
    data_file = sys.argv[1]
    percent = float(sys.argv[2])
    seed = int(sys.argv[3])

    attributes, label_counts, instances = create_instances(data_file)

    #print(attributes)
    #print(label_counts)

    training, test = split_data(instances, percent, seed)
    #print(len(training), len(test), len(instances))

    model = create_model(attributes, label_counts, training)
    #print(model)

    total_labels = 0
    for label in label_counts:
        total_labels += label_counts[label]

    confusion_matrix = []
    for i in range(len(label_counts)):
        new_list = [0 for i in range(len(label_counts))]
        confusion_matrix.append(new_list)

    labels = list(label_counts)
    print(labels)

    for instance in training:
        label = predict(instance, attributes, label_counts, total_labels, model)
        real_index = labels.index(instance[1])
        pred_index = labels.index(label)
        confusion_matrix[real_index][pred_index] += 1

    for row in confusion_matrix:
        print(row)

    full_model = (attributes, label_counts, total_labels, model)
    pickle_file = open('model.pickle', 'wb')
    pickle.dump(full_model, pickle_file)



if (__name__ == "__main__"):
    main()
