import sys
import math
import pickle

def calc_prob(instance, label, label_count, model, attributes):
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
        prob = calc_prob(instance, label, label_counts[label], model, attributes)
        if prob > max_prob:
            max_prob = prob
            max_label = label

    return max_label

def main(): 
    pickle_file = open('model.pickle', 'rb')
    attributes, label_counts, total_labels, model = pickle.load(pickle_file)

    fed_instance = sys.argv[1:]
    instance = (fed_instance, 0)

    result = predict(instance, attributes, label_counts, total_labels, model)
    print(result)


if (__name__ == "__main__"):
    main()
