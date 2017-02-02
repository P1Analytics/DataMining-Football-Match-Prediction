import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

class TensorFlow(object):
    def __init__(self, train_data, train_label, test_data, test_label, batch_percentage=0.75, number_step=1000):

        self.train_data = train_data
        self.train_label = train_label
        self.test_data = test_data
        self.test_label = test_label

        self.batch_size = int(len(self.train_data)*batch_percentage)
        self.number_step = number_step

        # Create graph
        self.sess = tf.Session()

        # Initialize placeholders
        number_of_train_element = len(train_data)
        number_of_features = len(train_data[0])
        self.x_data = tf.placeholder(shape=[None, number_of_features], dtype=tf.float32)
        self.y_target = tf.placeholder(shape=[None, 1], dtype=tf.float32)
        self.prediction_grid = tf.placeholder(shape=[None, 6], dtype=tf.float32)

        # Create variables for svm
        b = tf.Variable(tf.random_normal(shape=[1, self.batch_size]))

        # Gaussian (RBF) kernel
        gamma = tf.constant(-25.0)
        dist = tf.reduce_sum(tf.square(self.x_data), 1)
        dist = tf.reshape(dist, [-1, 1])
        sq_dists = tf.add(tf.sub(dist, tf.mul(2., tf.matmul(self.x_data, tf.transpose(self.x_data)))), tf.transpose(dist))
        my_kernel = tf.exp(tf.mul(gamma, tf.abs(sq_dists)))

        # Compute SVM Model
        self.model_output = tf.matmul(b, my_kernel)
        first_term = tf.reduce_sum(b)
        b_vec_cross = tf.matmul(tf.transpose(b), b)
        y_target_cross = tf.matmul(self.y_target, tf.transpose(self.y_target))
        second_term = tf.reduce_sum(tf.mul(my_kernel, tf.mul(b_vec_cross, y_target_cross)))
        self.loss = tf.neg(tf.sub(first_term, second_term))

        # Gaussian (RBF) prediction kernel
        rA = tf.reshape(tf.reduce_sum(tf.square(self.x_data), 1), [-1, 1])
        rB = tf.reshape(tf.reduce_sum(tf.square(self.prediction_grid), 1), [-1, 1])
        pred_sq_dist = tf.add(tf.sub(rA, tf.mul(2., tf.matmul(self.x_data, tf.transpose(self.prediction_grid)))),
                              tf.transpose(rB))
        pred_kernel = tf.exp(tf.mul(gamma, tf.abs(pred_sq_dist)))

        prediction_output = tf.matmul(tf.mul(tf.transpose(self.y_target), b), pred_kernel)
        self.prediction = tf.sign(prediction_output - tf.reduce_mean(prediction_output))
        self.accuracy = tf.reduce_mean(tf.cast(tf.equal(tf.squeeze(self.prediction), tf.squeeze(self.y_target)), tf.float32))

        # Declare optimizer
        my_opt = tf.train.GradientDescentOptimizer(0.01)
        self.train_step = my_opt.minimize(self.loss)

        # Initialize variables
        init = tf.global_variables_initializer()
        self.sess.run(init)


    def train(self,):
        # Training loop
        loss_vec = []
        batch_accuracy = []
        for i in range(self.number_step):
            rand_index = np.random.choice(len(self.train_data), size=self.batch_size)
            rand_x = self.train_data[rand_index]
            rand_y = np.transpose([self.train_label[rand_index]])
            self.sess.run(self.train_step, feed_dict={self.x_data: rand_x, self.y_target: rand_y})

            temp_loss = self.sess.run(self.loss, feed_dict={self.x_data: rand_x, self.y_target: rand_y})
            loss_vec.append(temp_loss)

            acc_temp = self.sess.run(self.accuracy, feed_dict={self.x_data: rand_x,
                                                     self.y_target: rand_y,
                                                     self.prediction_grid: rand_x})
            batch_accuracy.append(acc_temp)

            if (i + 1) % 75 == 0:
                print('Step #' + str(i + 1))
                print('Loss = ' + str(temp_loss))

        # Create a mesh to plot points in
        '''
        x_min, x_max = self.train_data[:, 0].min() - 1, self.train_data[:, 0].max() + 1
        y_min, y_max = self.train_data[:, 1].min() - 1, self.train_data[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                             np.arange(y_min, y_max, 0.02))
        grid_points = np.c_[xx.ravel(), yy.ravel()]
        print(grid_points.shape)
        [grid_predictions] = self.sess.run(self.prediction, feed_dict={self.x_data: rand_x,
                                                             self.y_target: rand_y,
                                                             self.prediction_grid: grid_points})
        grid_predictions = grid_predictions.reshape(xx.shape)


        # Plot points and grid
        plt.contourf(xx, yy, grid_predictions, cmap=plt.cm.Paired, alpha=0.8)
        plt.plot(class1_x, class1_y, 'ro', label='I. setosa')
        plt.plot(class2_x, class2_y, 'kx', label='Non setosa')
        plt.title('Gaussian SVM Results on Iris Data')
        plt.xlabel('Pedal Length')
        plt.ylabel('Sepal Width')
        plt.legend(loc='lower right')
        plt.ylim([-0.5, 3.0])
        plt.xlim([3.5, 8.5])
        plt.show()

        # Plot batch accuracy
        plt.plot(batch_accuracy, 'k-', label='Accuracy')
        plt.title('Batch Accuracy')
        plt.xlabel('Generation')
        plt.ylabel('Accuracy')
        plt.legend(loc='lower right')
        plt.show()

        # Plot loss over time
        plt.plot(loss_vec, 'k-')
        plt.title('Loss per Generation')
        plt.xlabel('Generation')
        plt.ylabel('Loss')
        plt.show()
        '''
    def score(self):
        y = self.sess.run(self.prediction, feed_dict={self.x_data: self.test_data,
                                                             self.y_target: None})
        print(y)


    def predict(self, data):
        pass

    