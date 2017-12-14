import random
import collections

#take an discrete instance and convert it using one hot coding
def one_hot_coding(instance, attribute_values): 
	new_instance = []
	for i in range(len(instance)):
		value = instance[i]
		if attribute_values[i] != None:
			values = attribute_values[i]
			one_hot = [0] * (len(values) - 1)
			i = values.index(value.strip())
			if i < len(values) - 1:
				one_hot[i] = 1
			new_instance += one_hot

		else:
			new_instance.append(value)

	return new_instance

#get dictionary of attribute values and labels from data file
def get_info(filename): 
	data_file = open(filename, 'r')
	label_list = []
	labels = {}
	attribute_values = {}

	attributes = data_file.readline().replace('\"','').strip().split(',')[1:]
	first_instance = data_file.readline().strip().split(',')[1:]

	#set up attribute value dictinary - all attribute will have value None
	#if continuous, a list of values if discrete 
	for i in range(len(attributes)):
		try:
			value = float(first_instance[i])
			attribute_values[i] = None
		except ValueError: 
			attribute_values[i] = []

	label_count = 0

	for line in data_file:
		line = line.replace('\"', "")
		data = line.strip().split(',')
		label = data[0] #get label from line
		curr_attributes = data[1:] #get attribute values from line 

		#add label to label list and dictionary if not already seen
		if label not in labels:
			labels[label] = label_count
			label_count += 1
			label_list.append(label)

		for i in range(len(attributes)):
			value = curr_attributes[i].strip()
			if attribute_values[i] != None: #add value to list if it is a discrete attribute
				if value not in attribute_values[i]: 
					attribute_values[i].append(value)

	return label_list, labels, attribute_values

def get_instances(filename, labels, attribute_values):
	data_file = open(filename, 'r')
	data_file.readline()
	instances = []
	contains_discrete = False 

	for value in attribute_values: 
		if attribute_values[value] != None:
			contains_discrete = True

	for line in data_file:
		line = line.replace('\"', "")
		data = line.strip().split(',')
		attributes = data[1:]
		#Set up label list for instance
		if len(labels) == 2:
			label = [labels[data[0]]] 
		else:
			label = [0] * len(labels)
			i = labels[data[0]]
			label[i] = 1

		#if instance contains discrete values - convert with one hot coding 
		if contains_discrete == True:
			attributes = one_hot_coding(attributes, attribute_values)

		instance = (attributes, label) #Create tuple representing instance
		instances.append(instance)

	return instances

def split_data(instances, percent, seed): 
	random.seed(seed)
	random.shuffle(instances)
	count = 0
	train, test = {0: [], 1: []}, {0: [], 1: []} #create traning and test dictionaries: 0 is attributes, 1 is labels

	while (len(train[0]) / len(instances) < percent): 
		train[0].append(instances[count][0])
		train[1].append(instances[count][1])
		count += 1
	while (count < len(instances)): 
		test[0].append(instances[count][0])
		test[1].append(instances[count][1])
		count += 1

	return train, test
