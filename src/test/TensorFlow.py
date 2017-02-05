
from __future__ import print_function

import numpy as np
import tensorflow as tf

class NNAlgorithm(object):
    def __init__(self, train_data, train_label, test_data, test_label,k=1, batch_percentage=0.75, number_step=1000):
        self.train_data = train_data
        self.train_label = train_label
        self.test_data = test_data
        self.test_label = test_label

        for i,label in enumerate(self.train_label):
            if label != 1:
                self.train_label[i] = -1
        for i,label in enumerate(self.test_label):
            if label != 1:
                self.test_label[i] = -1

        num_features = len(self.train_data[0])

        self.x_train = tf.placeholder("float", shape=[None, num_features])
        self.x_test = tf.placeholder("float", shape=[num_features])

        distance = tf.reduce_sum(tf.abs(tf.add(self.x_train, tf.negative(self.x_test))), reduction_indices=1)
        #pred = tf.arg_min(distance, 0)
        distance = 1./distance
        values, indices = tf.nn.top_k(distance, k=k, sorted=True)

        nearest_neighbors = []
        for i in range(k):
            nearest_neighbors.append(indices[i])

        neighbors_tensor = tf.pack(nearest_neighbors)
        y, idx, count = tf.unique_with_counts(neighbors_tensor)
        pred = tf.slice(y, begin=[tf.argmax(count, 0)], size=tf.constant([1], dtype=tf.int64))[0]

        accuracy = 0.
        # Initializing the variables
        init = tf.global_variables_initializer()
        with tf.Session() as sess:
            sess.run(init)

            # loop over test data
            for i in range(len(self.test_data)):
                # Get nearest neighbor

                nn_index = sess.run(pred, feed_dict={self.x_train: self.train_data, self.x_test: self.test_data[i, :]})
                print(nn_index)

                # Get nearest neighbor class label and compare it to its true label
                print("Test", i, "Prediction:", self.train_label[nn_index], \
                      "True Class:",self.test_label[i])
                # Calculate accuracy
                if (self.train_label[nn_index]) == (self.test_label[i]):
                    accuracy += 1. / len(self.test_data)
            print("Done!")
            print("Accuracy:", accuracy)