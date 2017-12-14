import tensorflow as tf
import pickle
import data_reader
import sys

RATE = .001

def predict(num_attributes, num_labels, NEURONS, instance):
    sess = tf.Session()

    hidden_layers = []
    f = open('accuracies.csv', 'w')

    # Set up placeholders for training attribute and label values
    x = tf.placeholder(tf.float32, shape=[None, num_attributes])
    y = tf.placeholder(tf.float32, shape=[None, num_labels])

    # Weights and biases for first hidden layer
    w_hidden = tf.Variable(tf.truncated_normal([num_attributes, NEURONS], stddev=0.1))
    b_hidden = tf.Variable(tf.constant(0.1, shape=[NEURONS]))

    # Output of first hidden layer
    net_hidden = tf.matmul(x, w_hidden) + b_hidden
    out_hidden = tf.sigmoid(net_hidden)

    w_output = tf.Variable(tf.truncated_normal([NEURONS, num_labels], stddev=0.1))
    b_output = tf.Variable(tf.constant(0.1, shape=[num_labels]))

    net_output = tf.matmul(out_hidden, w_output) + b_output

    if num_labels == 1:  # Activation and loss functions for binary predictions
        prediction = tf.sigmoid(net_output)
        loss = tf.reduce_sum((y - prediction) * (y - prediction))
    else:  # activation and loss functions for multinomial regression
        prediction = tf.nn.softmax(net_output)
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=net_output))

    backprop = tf.train.AdamOptimizer(RATE).minimize(loss)  # Set up backprop with given loss function

    saver = tf.train.Saver()
    saver.restore(sess, "/tmp/model.ckpt")

    p = sess.run(prediction, feed_dict = {x : [instance]})
    return p[0][0]



def main():
    pickle_file = open('attribute-values.pickle', 'rb')
    attribute_values = pickle.load(pickle_file)
    fed_instance = sys.argv[1:]

    instance = data_reader.one_hot_coding(fed_instance, attribute_values)

    print(len(instance))
    print(instance)

    result = predict(len(instance), 1, 10, instance)
    if result <= .5:
        print(0)
    else:
        print(1)

main()