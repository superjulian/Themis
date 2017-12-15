from discrimination import kNN
import random

class Dataset:
    def __init__(self, filename, label_values):
        self.instances = []
        self.label_values = label_values
        self.prot_attr, self.prot_group = "", ""
        self.p1, self.p2 = 0, 0
        self.prot_dict = {}

        self.attr_ind, self.instances = self.__init_instances(filename)

    def init_protected(self, prot_dict):
        self.prot_dict = prot_dict
        self.__get_proportions()

    def risk_diff(self):
        return self.p1 - self.p2

    def risk_ratio(self):
        return self.p1 / self.p2

    def rel_chance(self):
        return (1 - self.p1) / (1 - self.p2)

    def get_consistency(self, k):
        cont = input("Operation can be time intensive. Continue? (yes/no) ")
        if cont == "no":
            return 0
        return kNN.consistency(k, self.instances)

    def get_consistency_subset(self, k, percentage, seed):
        random.seed(seed)
        instances = self.instances
        random.shuffle(instances)
        subset = [instances[i] for i in range(int(percentage * len(instances)))]

        return kNN.consistency(k, subset)

    def get_avg_consistency(self, iterations, k, percentage):
        total = 0
        for i in range(iterations):
            num = random.randint(1, 5000)
            consistency = self.get_consistency_subset(k, percentage, num)
            total += consistency

        return (total / iterations)

    def __init_instances(self, filename):
        data_file = open(filename, 'r')
        instances, attr_ind = [], {}

        attributes = data_file.readline().strip().split(',')[:-1]
        length = len(attributes)

        for i in range(len(attributes)):
            attr_ind[attributes[i].strip()] = i

        for line in data_file:
            instance = line.strip().split(',')
            for i in range(len(instance)):
                instance[i] = instance[i].strip()

            if instance[length] == self.label_values[0]:
                label = 0
            else:
                label = 1

            final_instance = (instance[:-1], label)
            instances.append(final_instance)

        return attr_ind, instances

    def __get_proportions(self):
        a, b, c, d = 0, 0, 0, 0
        #indices = [self.attr_ind[attr] for attr in self.prot_dict]
        for instance in self.instances:
            protected = True
            for attr in self.prot_dict:
                if instance[0][self.attr_ind[attr]] != self.prot_dict[attr]:
                    protected = False
                    if instance[1] == 0:
                        c += 1
                    else:
                        d += 1
            if protected:
                if instance[1] == 0:
                    a += 1
                else:
                    b += 1

        self.p1 = a / (a + b)
        self.p2 = c / (c + d)
