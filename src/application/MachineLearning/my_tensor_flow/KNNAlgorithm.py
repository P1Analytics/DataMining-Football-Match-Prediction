import logging
import numpy as np
import tensorflow as tf
import src.util.util as util

from src.application.MachineLearning.MachineLearningAlgorithm import MachineLearningAlgorithm

class KNNAlgorithm(MachineLearningAlgorithm):
    def __init__(self, train_data
                     , train_label
                     , test_data
                     , test_label
                     , train_description
                     , test_description
                     , **params):
        '''

        :param train_data:
        :param train_label:
        :param test_data:
        :param test_label:
        :param train_description:
        :param test_description:
        :param params:
        '''

        MachineLearningAlgorithm.__init__(self, train_data, train_label, test_data, test_label, train_description,
                                          test_description)

        print("TensorFlow :: KNN > initialization")
        self.k = util.get_default(params, "k", 11)
        print("\t-k:", self.k)
        self.session = tf.Session()

        for i,label in enumerate(self.train_label):
            if label != 1:
                self.train_label[i] = -1
        for i,label in enumerate(self.test_label):
            if label != 1:
                self.test_label[i] = -1

        num_features = len(self.train_data[0])

        self.x_train = tf.placeholder("float", shape=[None, num_features])
        self.x_test = tf.placeholder("float", shape=[num_features])

    def train(self):
        # with KNN nothing to train"
        pass


    def get_distance(self):
        return tf.reduce_sum(tf.abs(tf.add(self.x_train, tf.negative(self.x_test))), reduction_indices=1)

    def get_prediction_function(self):
        distance = self.get_distance()
        if self.k == 1:
            return tf.arg_min(distance, 0)
        else:
            # we have to change this line of code
            distance = 1. / distance
            values, indices = tf.nn.top_k(distance, k=self.k, sorted=True)
            nearest_neighbors = []
            for i in range(self.k):
                nearest_neighbors.append(indices[i])

            neighbors_tensor = tf.pack(nearest_neighbors)
            y, idx, count = tf.unique_with_counts(neighbors_tensor)
            prediction = tf.slice(y, begin=[tf.argmax(count, 0)], size=tf.constant([1], dtype=tf.int64))[0]
            return prediction

    def score(self):
        init = tf.global_variables_initializer()

        self.session.run(init)

        predicted_labels = []
        # loop over test data
        for i in range(len(self.test_data)):
            # Get nearest neighbor

            nn_index = self.session.run(self.get_prediction_function(),
                                        feed_dict={self.x_train: self.train_data, self.x_test: self.test_data[i, :]})

            # Get nearest neighbor class label and compare it to its true label
            predicted_labels.append(self.train_label[nn_index])

            # Calculate accuracy
            accuracy = 0
            if (self.train_label[nn_index]) == (self.test_label[i]):
                accuracy += 1. / len(self.test_data)

        logging.debug("Accuracy on test" + str(accuracy))
        probability_events = [-1 for l in predicted_labels]

        return self.post_score(predicted_labels, probability_events)

