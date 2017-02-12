import numpy as np
import tensorflow as tf
import src.util.util as util
from src.application.MachineLearning.MachineLearningAlgorithm import MachineLearningAlgorithm
from src.application.MachineLearning.Plot_graph import Plot
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

        self.data_points = np.concatenate((self.train_data,self.test_data),axis = 0)
        self.data_labels = np.concatenate((self.train_label,self.test_label),axis = 0)

        print("Tensor Flow initialization:")
        print("method: SVM")
        self.num_features = len(self.train_data[0])
        self.batch_size = util.get_default(params, "batch_size", 1000)
        self.number_step = util.get_default(params, "number_step", 5000)
        self.kernel = util.get_default(params, "kernel", "linear")
        print("Num_features:",self.num_features)
        print("Batch_size:", self.batch_size)
        print("Number_step:", self.number_step)
        self.x = tf.placeholder(tf.float32, [None, self.num_features])
        self.y = tf.placeholder(tf.float32, [None, 1])

        if self.kernel == "linear":
            self.my_cost,self.decision_function = cost(self.x, self.y,self.batch_size,self.num_features, kernel_type= self.kernel, C=1000)
        if self.kernel == "rbf":
            self.my_cost,self.b = cost(self.x, self.y,self.batch_size,self.num_features, kernel_type= self.kernel, C=1000)

        self.train_step = tf.train.GradientDescentOptimizer(0.01).minimize(self.my_cost)


    def train(self,):
        self.session.run(tf.global_variables_initializer())

        for step in range(self.number_step):
            rand_index = np.random.choice(len(self.train_data), size=self.batch_size)
            batch_data = self.train_data[rand_index]
            batch_label = np.transpose([self.train_label[rand_index]])
            self.session.run(self.train_step, feed_dict={self.x: batch_data, self.y: batch_label})
            loss = self.session.run(self.my_cost, feed_dict={self.x: batch_data, self.y: batch_label})

            if (step + 1) % 75 == 0:
                print('Step #' + str(step + 1))
                print('Loss = ' + str(loss))

    def score(self):
        if self.kernel == "linear":
            model = tf.sign(self.decision_function)

            correct_prediction = tf.equal(self.y, model)
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
            logging.debug("Accuracy on test" + str(self.session.run(accuracy, feed_dict={self.x: self.test_data,
                                                                                           self.y: [[l] for l in
                                                                                                    self.test_label]})))
            classification = self.session.run(model, feed_dict={self.x: self.test_data})

            linear_plot = Plot(self.train_data)
            linear_plot.define_grid()

            grid_predictions = self.session.run(model, feed_dict={self.x: linear_plot.grid_points})

            linear_plot.show_decision_bounduaries(grid_predictions,self.data_points,self.data_labels)


            predicted_labels = [int(l[0]) for l in classification]
            probability_events = [-1 for l in classification]

        if self.kernel == "rbf":
            tensor_test = tf.placeholder(tf.float32, [None, self.num_features])
            model = decision_function(self.x,self.y,tensor_test, self.b)
            correct_prediction = tf.equal(self.y, model)
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

            print("Accuracy on test",str(self.session.run(accuracy, feed_dict={self.x: self.train_data,
                                                                                         self.y: [[l] for l in
                                                                                                  self.train_label],
                                                                                         tensor_test: self.test_data})))

            rbf_plot = Plot(self.train_data)
            rbf_plot.define_grid()
            [grid_predictions] = self.session.run(model, feed_dict={self.x: self.train_data,
                                                                                self.y: [[l] for l in
                                                                                         self.train_label],
                                                                                tensor_test: rbf_plot.grid_points})
            rbf_plot.show_decision_bounduaries(grid_predictions,self.test_data,self.test_label)
            classification = self.session.run(model, feed_dict={self.x: self.train_data,
                                               self.y: [[l] for l in
                                                        self.train_label],
                                               tensor_test: rbf_plot.grid_points})
            predicted_labels = [int(l[0]) for l in classification]
            probability_events = [-1 for l in classification]
        return self.post_score(predicted_labels, probability_events)




    def predict(self, data):
        pass


def get_SVM_Linear_train_step(x,num_features):
    b = tf.Variable(tf.zeros([1]))
    w = tf.Variable(tf.zeros([num_features, 1]))
    y_raw = tf.add(tf.matmul(x, w), b)

    return y_raw,w

def get_SVM_Gaussian_kernel(tensor_1, tensor_2):
    gamma = tf.constant(-3.0)
    sq_vec = tf.mul(2., tf.matmul(tensor_1, tf.transpose(tensor_2)))
    kernel = tf.exp(tf.mul(gamma, tf.abs(sq_vec)))
    return kernel


def cost(training, classes, inputs,num_features, kernel_type="rbf", C=1):
    """Returns the kernelised cost to be minimised."""

    if kernel_type == "linear":
        decision_function,w = get_SVM_Linear_train_step(training,num_features)

        hinge_loss = tf.reduce_sum(tf.maximum(tf.zeros(inputs, 1), 1 - classes * decision_function))
        regularization_loss = 0.5 * tf.reduce_sum(tf.square(w))
        svm_loss = regularization_loss + C * hinge_loss
        return svm_loss, decision_function

    if kernel_type == "rbf":
        b = tf.Variable(tf.random_normal(shape=[1, inputs]))
        kernel = get_SVM_Gaussian_kernel(training,training)
        first_term = tf.reduce_sum(b)
        b_vec_cross = tf.matmul(tf.transpose(b), b)
        y_target_cross = tf.matmul(classes, tf.transpose(classes))
        second_term = tf.reduce_sum(tf.mul(kernel, tf.mul(b_vec_cross, y_target_cross)))
        loss = tf.neg(tf.sub(first_term, second_term))
        return loss,b


def decision_function(training, classes,tensor_test,tensor_b):
    kernel = get_SVM_Gaussian_kernel(training, tensor_test)
    model = tf.matmul(tf.mul(tf.transpose(classes), tensor_b), kernel)
    prediction = model-tf.reduce_mean(model)
    return tf.sign(prediction)
