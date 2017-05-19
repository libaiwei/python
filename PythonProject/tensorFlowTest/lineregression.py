# coding:utf8
import tensorflow as tf
import numpy
import matplotlib.pyplot as plt
rng = numpy.random

# parameters
learning_rate = 0.01
training_epochs = 2000
display_step = 50

# training data
train_X = numpy.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,7.042,10.791,5.313,7.997,5.654,9.27,3.1])
train_Y = numpy.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,2.827,3.465,1.65,2.904,2.42,2.94,1.3])
n_samples = train_X.shape[0]

# tf Graph input
X = tf.placeholder('float')
Y = tf.placeholder('float')

# Create Model
# Set model weights
w = tf.Variable(rng.randn(), name='weight')
b = tf .Variable(rng.randn(),name='bias')

# construct a linear model
activation = tf.add(tf.multiply(X, w), b)

# Minimize the square errors
cost = tf.reduce_sum(tf.pow(activation-Y, 2))/(2*n_samples)
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initialize the variables
init = tf.initialize_all_variables()

# launch the graph
with tf.Session() as sess:
    sess.run(init)

    # Fit all training data
    for epoch in range(training_epochs):
        for(x,y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X:x, Y:y})

        # display logs per epoch step
        if epoch % display_step == 0:
            print 'epoch:', '%04d' % (epoch+1), 'cost=', \
                  '{:.9f}'.format(sess.run(cost, feed_dict={X: train_X, Y: train_Y})), \
                  'w=', sess.run(w), 'b=', sess.run(b)

    print('optimization finished')
    print 'cost', sess.run(cost, feed_dict={X:train_X, Y:train_Y}), \
          'w=', sess.run(w), 'b=', sess.run(b)

    # graphic display
    plt.plot(train_X, train_Y, 'ro', label='Original data')
    plt.plot(train_X, sess.run(w)*train_X+sess.run(b), label='fitted line')
    plt.legend()
    plt.show()
