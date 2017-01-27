import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


from src.application.input_preprocess.MatchesResultManagement import MatchesResultReader


def doTest():
    mrr = MatchesResultReader("serie_A")
    matches = mrr.read_matches("Juventus", "Torino", order=False)
    print(matches)

    test_size = 5
    train_size = len(matches)-test_size

    # train_X = np.asarray([float(x) for x in range(train_size)])
    dates_X = []
    for date, result in matches:
        day = str(date).split("/")[0]
        month = str(date).split("/")[1]
        dates_X.append(float(int(month+day))/360.)
    train_X = np.asarray(dates_X[0:-test_size])
    test_X = np.asarray(dates_X[train_size:])


    train_Y = np.asarray([float(m[1]) for m in matches[0:train_size]])

    n_samples = train_X.shape[0]

    X = tf.placeholder("float")
    Y = tf.placeholder("float")

    W = tf.Variable(np.random.randn(), name="weight")
    b = tf.Variable(np.random.randn(), name="bias")

    pred = tf.add(tf.mul(X, W), b)

    cost = tf.reduce_sum(tf.pow(pred - Y, 2)) / (2 * n_samples)
    learning_rate = 0.01
    training_epochs = 1000
    display_step = 50
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)

        # Fit all training data
        for epoch in range(training_epochs):
            for (x, y) in zip(train_X, train_Y):
                sess.run(optimizer, feed_dict={X: x, Y: y})

            # Display logs per epoch step
            if (epoch + 1) % display_step == 0:
                c = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
                print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(c), "W=", sess.run(W), "b=", sess.run(b))

        print("Optimization Finished!")
        training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
        print("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n')

        # Graphic display
        plt.plot(train_X, train_Y, 'ro', label='Original data')
        plt.plot(train_X, sess.run(W) * train_X + sess.run(b), label='Fitted line')
        plt.legend()
        #plt.show()

        # Testing example, as requested (Issue #2)
        #test_X = np.asarray([float(x) for x in range(train_size, train_size+test_size)])
        test_Y = np.asarray([float(m[1]) for m in matches[train_size:]])
        print(test_X)
        print(test_Y)
        print("Testing... (Mean square loss Comparison)")
        testing_cost = sess.run(
            tf.reduce_sum(tf.pow(pred - Y, 2)) / (2 * test_X.shape[0]),
            feed_dict={X: test_X, Y: test_Y})  # same function as cost above
        print("Testing cost=", testing_cost)
        print("Absolute mean square loss difference:", abs(
            training_cost - testing_cost))

        plt.plot(test_X, test_Y, 'bo', label='Testing data')
        plt.plot(train_X, sess.run(W) * train_X + sess.run(b), label='Fitted line')
        plt.legend()
        plt.show()


doTest()


