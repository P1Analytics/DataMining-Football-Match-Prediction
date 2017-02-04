import numpy as np
import tensorflow as tf
from src.application.MachineLearning.MachineLearningAlgorithm import MachineLearningAlgorithm

class TensorFlow(MachineLearningAlgorithm):
    def __init__(self, train_data
                     , train_label
                     , test_data
                     , test_label
                     , train_description
                     , test_description
                     , batch_percentage=0.75
                    , number_step=1000):
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

        for i,label in enumerate(self.train_label):
            if label != 1:
                self.train_label[i] = -1
        for i,label in enumerate(self.test_label):
            if label != 1:
                self.test_label[i] = -1

        self.batch_size = int(batch_percentage*len(self.train_data))

        num_features = len(self.train_data[0])

        self.sess = tf.Session()

        self.x = tf.placeholder("float", shape=[None, num_features])
        self.y = tf.placeholder("float", shape=[None, 1])

        w = tf.Variable(tf.zeros([num_features, 1]))
        b = tf.Variable(tf.zeros([1]))

        y_raw = tf.add(tf.matmul(self.x,w),b)

        # Optimization
        C = 1
        regularization_loss = 0.5*tf.reduce_sum(tf.square(w))
        hinge_loss = tf.reduce_sum(tf.maximum(tf.zeros(self.batch_size, 1),1-self.y*y_raw))
        svm_loss = regularization_loss + C*hinge_loss
        self.train_step = tf.train.GradientDescentOptimizer(0.01).minimize(svm_loss)

        #Evaluation
        self.predicted_class = tf.sign(y_raw)
        correct_prediction = tf.equal(self.y, self.predicted_class)
        self.accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

    def train(self,):
        # create local session to run the trainable parameters
        self.sess.run(tf.global_variables_initializer())  # WARNING: trusted to LEO .run()

        for step in range(5000):
            rand_index = np.random.choice(len(self.train_data), size=self.batch_size)
            batch_data = self.train_data[rand_index]
            batch_label = np.transpose([self.train_label[rand_index]])

            self.sess.run(self.train_step, feed_dict={self.x: batch_data, self.y: batch_label})

        print("Accuracy on train",
              self.sess.run(self.accuracy, feed_dict={self.x: self.train_data, self.y: [[l] for l in self.train_label]}))
        pass

    def score(self):
        print("Accuracy on test", self.sess.run(self.accuracy, feed_dict={self.x: self.test_data, self.y: [[l] for l in self.test_label]}))

        classification = self.sess.run(self.predicted_class, feed_dict={self.x: self.test_data})

        predicted_labels = [int(l[0]) for l in classification]
        probability_events = [-1 for l in classification]

        return self.post_score(predicted_labels, probability_events)

    def predict(self, data):
        pass


