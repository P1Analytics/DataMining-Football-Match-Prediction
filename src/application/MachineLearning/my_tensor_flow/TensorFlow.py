import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

class TensorFlow(object):
    def __init__(self, train_data, train_label, test_data, test_label, batch_percentage=0.75, number_step=1000):
        '''
        The input label must be +1 or -1
        :param train_data:
        :param train_label:
        :param test_data:
        :param test_label:
        :param batch_percentage:
        :param number_step:
        '''

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

        x = tf.placeholder("float", shape=[None, num_features])
        y = tf.placeholder("float", shape=[None, 1])

        w = tf.Variable(tf.zeros([num_features, 1]))
        b = tf.Variable(tf.zeros([1]))

        y_raw = tf.add(tf.matmul(x,w),b)

        # Optimization
        BATCH_SIZE = int(batch_percentage*len(self.train_data))
        C = 1
        regularization_loss = 0.5*tf.reduce_sum(tf.square(w))
        hinge_loss = tf.reduce_sum(tf.maximum(tf.zeros(BATCH_SIZE, 1),1-y*y_raw))
        svm_loss = regularization_loss + C*hinge_loss
        train_step = tf.train.GradientDescentOptimizer(0.01).minimize(svm_loss)

        #Evaluation
        predicted_class = tf.sign(y_raw)
        correct_prediction = tf.equal(y, predicted_class)
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        # create local session to run the trainable parameters
        with tf.Session() as s:
            tf.global_variables_initializer().run()  # WARNING: trusted to LEO .run()

            for step in range(5000):
                rand_index = np.random.choice(len(self.train_data), size=BATCH_SIZE)
                batch_data = self.train_data[rand_index]
                batch_label = np.transpose([self.train_label[rand_index]])

                train_step.run(feed_dict={x:batch_data, y:batch_label})

                #print("loss", svm_loss.eval(feed_dict={x:batch_data, y:batch_label}))
                #print("Weight matrix", s.run(w))
                #print("Bias vector", s.run(b))
            print("Accuracy on train", accuracy.eval(feed_dict={x:self.train_data, y:[[l] for l in self.train_label]}))
            print("Accuracy on test", accuracy.eval(feed_dict={x: self.test_data, y:[[l] for l in self.test_label]}))


            classification = predicted_class.eval(feed_dict={x: self.test_data})
            print(classification)



    def train(self,):
        pass

    def score(self):
        return [],[]

    def predict(self, data):
        pass


