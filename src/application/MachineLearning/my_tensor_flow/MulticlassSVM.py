import numpy as np
import tensorflow as tf
import src.util.util as util
from src.application.MachineLearning.MachineLearningAlgorithm import MachineLearningAlgorithm


class SVM_Multiclass(MachineLearningAlgorithm):
    def __init__(self, train_data
                 , train_label
                 , test_data
                 , test_label
                 , train_description
                 , test_description
                 , **params):
        MachineLearningAlgorithm.__init__(self, train_data, train_label, test_data, test_label, train_description,
                                          test_description)

        self.session = tf.Session()

        self.data_points = np.concatenate((self.train_data, self.test_data), axis=0)
        self.data_labels = np.concatenate((self.train_label, self.test_label), axis=0)

        labels_vals1 = np.array([1 if y == 0 else -1 for y in self.data_labels])
        labels_vals2 = np.array([1 if y == 1 else -1 for y in self.data_labels])
        labels_vals3 = np.array([1 if y == 3 else -1 for y in self.data_labels])

        self.data_labels = np.array([labels_vals1, labels_vals2, labels_vals3])

        labels_vals1 = np.array([1 if y == 0 else -1 for y in self.train_label])
        labels_vals2 = np.array([1 if y == 1 else -1 for y in self.train_label])
        labels_vals3 = np.array([1 if y == 3 else -1 for y in self.train_label])

        self.new_train_label = np.array([labels_vals1, labels_vals2, labels_vals3])

        labels_vals1 = np.array([1 if y == 0 else -1 for y in self.test_label])
        labels_vals2 = np.array([1 if y == 1 else -1 for y in self.test_label])
        labels_vals3 = np.array([1 if y == 3 else -1 for y in self.test_label])

        self.new_test_label = np.array([labels_vals1, labels_vals2, labels_vals3])
        self.num_features = len(self.train_data[0])
        self.batch_size = util.get_default(params, "batch_size", 1000)
        self.number_step = util.get_default(params, "number_step", 5000)
        self.kernel = util.get_default(params, "kernel", "linear")

        print("Num_features:", self.num_features)
        print("Batch_size:", self.batch_size)
        print("Number_step:", self.number_step)

        self.x = tf.placeholder(tf.float32, [None, self.num_features])
        self.y = tf.placeholder(tf.float32, [3, None])

        if self.kernel == "rbf":
            self.my_cost,self.b = self.cost(self.x, self.y,self.batch_size,self.num_features, kernel_type= self.kernel, C=1)
        self.train_step = tf.train.GradientDescentOptimizer(0.01).minimize(self.my_cost)

    def train(self):
        self.session.run(tf.global_variables_initializer())

        for step in range(self.number_step):
            rand_index = np.random.choice(len(self.train_data), size=self.batch_size)
            batch_data = self.train_data[rand_index]
            batch_label = self.new_train_label[:,rand_index]
            self.session.run(self.train_step, feed_dict={self.x: batch_data, self.y: batch_label})
            loss = self.session.run(self.my_cost, feed_dict={self.x: batch_data, self.y: batch_label})

            if (step + 1) % 75 == 0:
                print('Step #' + str(step + 1))
                print('Loss = ' + str(loss))

    def score(self):

        tensor_test_data = tf.placeholder(tf.float32, [None, self.num_features])
        model = decision_function(self.x, self.y, tensor_test_data, self.b)

        classification = self.session.run(model, feed_dict={self.x: self.train_data,
                                                            self.y: self.new_train_label,
                                                            tensor_test_data: self.test_data})
        predicted_labels = [int(l) for l in classification]
        probability_events = [-1 for l in classification]

        return self.post_score(predicted_labels, probability_events)


    def reshape_matmul(self,mat):
        v1 = tf.expand_dims(mat, 1)
        v2 = tf.reshape(v1, [3, self.batch_size, 1])
        return (tf.batch_matmul(v2, v1))

    def cost(self,training, classes, inputs, num_features, kernel_type="rbf", C=1):
        """Returns the kernelised cost to be minimised."""

        if kernel_type == "rbf":
            b = tf.Variable(tf.random_normal(shape=[3, inputs]))
            kernel = get_SVM_Gaussian_kernel(training, training)

            first_term = tf.reduce_sum(b)
            b_vec_cross = tf.matmul(tf.transpose(b), b)
            y_target_cross = self.reshape_matmul(classes)
            first_mul = tf.mul(b_vec_cross, y_target_cross)
            second_mul = tf.mul(kernel, first_mul)

            second_term = tf.reduce_sum(second_mul, [1, 2])
            loss = tf.reduce_sum(tf.neg(tf.sub(first_term, second_term)))
            return loss, b


def get_SVM_Gaussian_kernel(tensor_1, tensor_2):
    gamma = tf.constant(-1.0)
    dist = tf.reduce_sum(tf.square(tensor_1), 1)
    dist = tf.reshape(dist, [-1, 1])
    sq_dists = tf.add(tf.sub(dist, tf.mul(2., tf.matmul(tensor_1, tf.transpose(tensor_2)))), tf.transpose(dist))
    kernel = tf.exp(tf.mul(gamma, tf.abs(sq_dists)))
    return kernel

def decision_function(training, classes,tensor_test,tensor_b):
    gamma = tf.constant(-1.0)
    rA = tf.reshape(tf.reduce_sum(tf.square(training), 1), [-1, 1])
    rB = tf.reshape(tf.reduce_sum(tf.square(tensor_test), 1), [-1, 1])
    pred_sq_dist = tf.add(tf.sub(rA, tf.mul(2., tf.matmul(training, tf.transpose(tensor_test)))), tf.transpose(rB))
    pred_kernel = tf.exp(tf.mul(gamma, tf.abs(pred_sq_dist)))

    prediction_output = tf.matmul(tf.mul(classes, tensor_b), pred_kernel)
    prediction = tf.arg_max(prediction_output - tf.expand_dims(tf.reduce_mean(prediction_output, 1), 1), 0)
    return prediction
