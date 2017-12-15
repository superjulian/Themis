import data_reader
import tensorflow as tf
import sys
import pickle

ITER = 1000
NEURONS = 10
RATE = 0.002

#Function to find index of maximum value in list
def arg_max(list):
	index = 0
	for i in range(len(list)):
		if list[i] > list[index]:
			index = i

	return index

#Calculate accuracy given a confusion matrix
def calc_accuracy(confusion_matrix):
	total, correct = 0, 0
	for i in range(len(confusion_matrix)):
		for j in range(len(confusion_matrix[i])):
			total += confusion_matrix[i][j]
			if i == j:
				correct += confusion_matrix[i][j]

	return (correct / total)

#Create a matrix given a list of predictions, actual labels and the number of labels
def create_matrix(predictions, labels, num_labels):
	confusion_matrix = []
	if num_labels == 1:
		num_labels += 1

	for i in range(num_labels):
		list = [0 for i in range(num_labels)]
		confusion_matrix.append(list)

	#Update confusion matrix for each prediction
	for i in range(len(predictions)):
		if len(labels[i]) == 1:  # If binary label 
			pred_index = 0 if (predictions[i][0] >= 0.5) else 1
			real_index = 0 if (labels[i][0] == 1) else 1
		else: #For multinomial predictions
			pred_index = arg_max(predictions[i]) #Find index for maximum prediction
			real_index = labels[i].index(1) #Find actual label

		confusion_matrix[real_index][pred_index] += 1

	return confusion_matrix

#Given a confusion matrix and data, print confusion matrix and accuracy to file
def print_to_file(seed, data_name, percent, layers, labels, confusion_matrix):
	length = len(data_name) - 4
	output_file_name = 'results_' + data_name[:length] + "_" + str(NEURONS) + "n_" + str(RATE) + "r_" + str(ITER) + "i_"
	output_file_name += str(percent) + "p_" + str(seed) + "s_" + str(layers) + ".csv"
	f = open(output_file_name, 'w')
	for label in labels:
		f.write(label + ",")
	f.write('\n')
	total = 0
	correct = 0
	for i in range(len(confusion_matrix)):
		for j in range(len(confusion_matrix[i])):
			f.write(str(confusion_matrix[i][j]) + ",")
			total += confusion_matrix[i][j]
			if i == j:
				correct += confusion_matrix[i][j]
		f.write(labels[i])
		f.write('\n')

	f.write("\nAccuracy:" + str(correct / total))


def train_network(train, test, num_attributes, num_labels, layer_num):
	hidden_layers = []
	f = open('accuracies.csv', 'w')

	#Set up placeholders for training attribute and label values
	x = tf.placeholder(tf.float32, shape=[None, num_attributes])
	y = tf.placeholder(tf.float32, shape=[None, num_labels])

	#Weights and biases for first hidden layer
	w_hidden = tf.Variable(tf.truncated_normal([num_attributes, NEURONS], stddev=0.1))
	b_hidden = tf.Variable(tf.constant(0.1, shape=[NEURONS]))

	#Output of first hidden layer
	net_hidden = tf.matmul(x, w_hidden) + b_hidden
	out_hidden = tf.sigmoid(net_hidden)

	w_output = tf.Variable(tf.truncated_normal([NEURONS, num_labels], stddev=0.1))
	b_output = tf.Variable(tf.constant(0.1, shape = [num_labels]))

	net_output = tf.matmul(out_hidden, w_output) + b_output

	if num_labels == 1: #Activation and loss functions for binary predictions
		prediction = tf.sigmoid(net_output)
		loss = tf.reduce_sum((y - prediction) * (y - prediction))
	else: #activation and loss functions for multinomial regression
		prediction = tf.nn.softmax(net_output)
		loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=net_output))

	backprop = tf.train.AdamOptimizer(RATE).minimize(loss) #Set up backprop with given loss function

	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())
		saver = tf.train.Saver()
		iterations = 1

		for step in range(ITER):
			_, p = sess.run([backprop, prediction], feed_dict={x: train[0], y: train[1]}) #Run backprop

			if iterations % 50 == 0:
				matrix_train = create_matrix(p, train[1], num_labels)
				train_acc = calc_accuracy(matrix_train)
				p = sess.run(prediction, feed_dict={x: test[0], y: test[1]})
				matrix_test = create_matrix(p, test[1], num_labels)
				test_acc = calc_accuracy(matrix_test)
				f.write(str(train_acc) + "," + str(test_acc) + "\n")

			iterations += 1

		save_path = saver.save(sess, "/tmp/model.ckpt")
		print("Model saved in file: %s " % save_path)
		p = sess.run(prediction, feed_dict={x: test[0], y: test[1]}) #get predictions on test set

	return p

def main():
	global NEURONS
	global RATE
	global ITER
	data_set, NEURONS, RATE = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]),
	ITER, percent, seed, layers = int(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])


	label_list, labels, attribute_values = data_reader.get_info(data_set) #get label list, and dictionary of attribute values

	instances = data_reader.get_instances(data_set, labels, attribute_values) #get instances from data set
	train, test = data_reader.split_data(instances, percent, seed) #split instances into train and test sets

	num_attributes, num_labels = len(train[0][0]), len(train[1][0])
	predictions = train_network(train, test, num_attributes, num_labels, layers) #create and train neural network

	matrix = create_matrix(predictions, test[1], num_labels) #create confusion matrix from predictions
	print_to_file(seed, data_set, percent, layers, label_list, matrix) #print confusion matrix to file

	output_data = (attribute_values, num_attributes, NEURONS)
	pickle_file = open('neural-model.pickle', 'wb')
	pickle.dump(output_data, pickle_file)


main()