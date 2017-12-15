import operator

def hamming(x, y):
    sim = 0
    for i in range(len(x)):
        if (x[i] == y[i]):
            sim += 1

    return (len(x) - sim)

def nearest_sum(k, curr_inst, instances):
    #print(curr_inst)
    distances = []
    for instance in instances:
        if instance != curr_inst:
            distance = hamming(curr_inst[0], instance[0])
            distance_pair = (instance, distance)
            distances.append(distance_pair)

    distances.sort(key=operator.itemgetter(1))

    sum = 0
    for i in range(1, k):
        #print(distances[i])
        #print(distances[i][0][1])
        sum += distances[i][0][1]

    return sum


def consistency(k, instances):
    total = 0
    for instance in instances:
        label = instance[1]
        sum = nearest_sum(k, instance, instances)
        total += abs(label - sum)

    total = total / (len(instances) * k)

    return (1 - total)


