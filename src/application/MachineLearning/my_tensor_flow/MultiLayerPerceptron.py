import numpy as np
import tensorflow as tf
import src.util.util as util
from src.application.MachineLearning.MachineLearningAlgorithm import MachineLearningAlgorithm
from src.application.MachineLearning.Plot_graph import Plot
import logging
import matplotlib.pyplot as plt


class MultiLayerPerceptron(MachineLearningAlgorithm):
    def __init__(self, train_data
                     , train_label
                     , test_data
                     , test_label
                     , train_description
                     , test_description
                     , **params):
        '''
        The input label must be +1 or -1
        :param train_data:
        :param train_label:
        :param test_data:
        :param test_label:
        :param batch_percentage:
        :param number_step:
        '''
        MachineLearningAlgorithm.__init__(self, train_data, train_label, test_data, test_label, train_description,
                                          test_description)

        self.session = tf.Session()

        self.new_train_labels = []
        for i in self.train_label:
            if i == 0:
                self.new_train_labels.append([1,0,0])
            elif i == 1:
                self.new_train_labels.append([0, 1, 0])
            elif i == 2:
                self.new_train_labels.append([0, 0, 1])
        self.new_train_labels = np.asarray(self.new_train_labels)
        self.num_features = len(self.train_data[0])
        self.batch_size = util.get_default(params, "batch_size", len(self.train_data))
        self.number_step = util.get_default(params, "number_step", 5000)
        print("MLP")
        print("Num_features:",self.num_features)
        print("Batch_size:", self.batch_size)
        print("Number_step:", self.number_step)
        self.x = tf.placeholder(tf.float32, [None, self.num_features])
        self.y = tf.placeholder(tf.float32, [None, 3])

        self.weights = {
            'h1': tf.Variable(tf.random_normal([ self.num_features, 256])),
            'h2': tf.Variable(tf.random_normal([256, 256])),
            'out': tf.Variable(tf.random_normal([256, 3]))
        }
        self.biases = {
            'b1': tf.Variable(tf.random_normal([256])),
            'b2': tf.Variable(tf.random_normal([256])),
            'out': tf.Variable(tf.random_normal([3]))
        }
        self.pred = multilayer_perceptron(self.x, self.weights, self.biases)

        # Define loss and optimizer
        self.my_cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.pred, labels=self.y))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=0.01).minimize(self.my_cost)

    def train(self, ):
        self.session.run(tf.global_variables_initializer())
        for step in range(self.number_step):
            rand_index = np.random.choice(len(self.train_data), size=self.batch_size)
            batch_data = self.train_data[rand_index]
            batch_label = self.new_train_labels[rand_index]
            self.session.run(self.optimizer, feed_dict={self.x: batch_data, self.y: batch_label})
            loss = self.session.run(self.my_cost, feed_dict={self.x: batch_data, self.y: batch_label})

    def predict(self,data):

        classification = self.session.run(tf.argmax(self.pred, 1), feed_dict={self.x: data})
        return classification,[-1 for i in classification]


def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    layer_1 = tf.add(tf.matmul(x ,weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # Hidden layer with RELU activation
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    # Output layer with linear activation
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

# Store layers weight & bias
