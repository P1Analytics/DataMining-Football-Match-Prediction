import numpy as np
import tensorflow as tf
import src.util.util as util
from src.application.MachineLearning.MachineLearningAlgorithm import MachineLearningAlgorithm
import logging
import matplotlib.pyplot as plt


class SVM(MachineLearningAlgorithm):
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

        for i,label in enumerate(self.train_label):
            if label != 1:
                self.train_label[i] = -1
        for i,label in enumerate(self.test_label):
            if label != 1:
                self.test_label[i] = -1

        print("Tensor Flow initialization:")
        print("method: SVM")

        self.num_features = len(self.train_data[0])

        print(self.num_features)
        self.batch_size = util.get_default(params, "batch_size", 1000)
        self.number_step = util.get_default(params, "number_step", 5000)
        self.kernel = util.get_default(params, "kernel", "linear")
        print("Batch_size:", self.batch_size)
        print("Number_step:", self.number_step)
        self.x = tf.placeholder(tf.float32, [None, self.num_features])
        self.y = tf.placeholder(tf.float32, [None, 1])

        if self.kernel == "linear":
            self.my_cost,self.decision_function = cost(self.x, self.y,self.batch_size,self.num_features, kernel_type= self.kernel, C=1, gamma=1)
        else:
            self.beta, self.offset, self.my_cost = cost(self.x, self.y,self.batch_size,self.num_features, kernel_type= "rbf", C=1, gamma=25)

        self.train_step = tf.train.GradientDescentOptimizer(0.01).minimize(self.my_cost)


    def train(self,):
        self.session.run(tf.global_variables_initializer())
        for step in range(self.number_step):
            rand_index = np.random.choice(len(self.train_data), size=self.batch_size)
            batch_data = self.train_data[rand_index]
            batch_label = np.transpose([self.train_label[rand_index]])
            self.session.run(self.train_step, feed_dict={self.x: batch_data, self.y: batch_label})


    def score(self):
        test_tensor = tf.placeholder(tf.float32, [None,self.num_features ])

        if self.kernel == "rbf":
            model = decide(
                self.x, self.batch_size, test_tensor, len(self.test_data), self.beta, self.offset, kernel_type="rbf",
                gamma=1)

            correct_prediction = tf.equal(self.y, model)
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
            print("Test data classified as signal: %f%%" % self.session.run(
                accuracy, feed_dict={self.x: self.train_data,
                                     test_tensor: self.test_data,
                                     self.y: [[l] for l in self.test_label]}))

            classification = self.session.run(model, feed_dict={self.x: self.train_data, test_tensor: self.test_data})

            x_min, x_max = self.train_data[:, 0].min() - 1, self.train_data[:, 0].max() + 1
            y_min, y_max = self.train_data[:, 1].min() - 1, self.train_data[:, 1].max() + 1
            xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                                 np.arange(y_min, y_max, 0.02))
            grid_points = np.c_[xx.ravel(), yy.ravel()]
            model = decide(
                self.x, self.batch_size, test_tensor, len(grid_points), self.beta, self.offset, kernel_type="rbf",
                gamma=1)

            grid_predictions = self.session.run(model, feed_dict={self.x: self.train_data,
                                                                    test_tensor: grid_points})
            print(grid_predictions)
            grid_predictions = grid_predictions.reshape(xx.shape)
            plt.figure()
            plt.contourf(xx, yy, grid_predictions, cmap=plt.cm.Paired, alpha=0.8)
            plt.scatter(self.test_data[:, 0], self.test_data[:, 1], c=self.test_label)
            plt.show()

            predicted_labels = [int(l[0]) for l in classification]
            probability_events = [-1 for l in classification]
            return self.post_score(predicted_labels, probability_events)

        elif self.kernel == "linear":

            model = tf.sign(self.decision_function)
            correct_prediction = tf.equal(self.y, model)
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
            logging.debug("Accuracy on test" + str(self.session.run(accuracy, feed_dict={self.x: self.test_data,
                                                                                           self.y: [[l] for l in
                                                                                                    self.test_label]})))

            classification = self.session.run(model, feed_dict={self.x: self.test_data})

            for clas in classification:
                print(clas)

            predicted_labels = [int(l[0]) for l in classification]
            probability_events = [-1 for l in classification]

            return self.post_score(predicted_labels, probability_events)




    def predict(self, data):
        pass



def cross_matrices(tensor_a, a_inputs, tensor_b, b_inputs):
    """Tiles two tensors in perpendicular dimensions."""
    expanded_a = tf.expand_dims(tensor_a, 1)
    expanded_b = tf.expand_dims(tensor_b, 0)
    tiled_a = tf.tile(expanded_a, tf.constant([1, b_inputs, 1]))
    tiled_b = tf.tile(expanded_b, tf.constant([a_inputs, 1, 1]))

    return [tiled_a, tiled_b]


def get_SVM_Linear_train_step(x,num_features):
    b = tf.Variable(tf.zeros([1]))
    w = tf.Variable(tf.zeros([num_features, 1]))
    y_raw = tf.add(tf.matmul(x, w), b)

    return y_raw,w

def gaussian_kernel(tensor_a, a_inputs, tensor_b, b_inputs, gamma):
    """Returns the Gaussian kernel matrix of two matrices of vectors
    element-wise."""
    cross = cross_matrices(tensor_a, a_inputs, tensor_b, b_inputs)

    kernel = tf.exp(tf.mul(tf.reduce_sum(tf.square(
        tf.sub(cross[0], cross[1])), reduction_indices=2),
        tf.neg(tf.constant(gamma, dtype=tf.float32))))

    return kernel


def cost(training, classes, inputs,num_features, kernel_type="rbf", C=1, gamma=1):
    """Returns the kernelised cost to be minimised."""
    beta = tf.Variable(tf.zeros([inputs, 1]))
    offset = tf.Variable(tf.zeros([1]))

    if kernel_type == "linear":
        decision_function,w = get_SVM_Linear_train_step(training,num_features)

        hinge_loss = tf.reduce_sum(tf.maximum(tf.zeros(inputs, 1), 1 - classes * decision_function))
        regularization_loss = 0.5 * tf.reduce_sum(tf.square(w))
        svm_loss = regularization_loss + C * hinge_loss
        return svm_loss, decision_function

    elif kernel_type == "rbf":
        kernel = gaussian_kernel(training, inputs, training, inputs, gamma)

        x = tf.reshape(tf.div(tf.matmul(tf.matmul(
            beta, kernel, transpose_a=True), beta), tf.constant([2.0])), [1])
        y = tf.sub(tf.ones([1]), tf.mul(classes, tf.add(
            tf.matmul(kernel, beta, transpose_a=True), offset)))
        z = tf.mul(tf.reduce_sum(tf.reduce_max(
            tf.concat(1, [y, tf.zeros_like(y)]), reduction_indices=1)),
            tf.constant([C], dtype=tf.float32))
        cost = tf.add(x, z)

        return beta, offset, cost

def decide(training, training_instances, testing, testing_instances,
           beta, offset, kernel_type="rbf", gamma=1):

    kernel = gaussian_kernel(
        testing, testing_instances, training, training_instances, gamma)

    return tf.sign(tf.add(tf.matmul(kernel, beta), offset))