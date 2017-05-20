#coding:utf8
#simple CNN realization
import mycnn1
import tensorflow as tf
import numpy as np
import scipy.io as sio
#load dataset
sess = tf.InteractiveSession()
#define initial function to reuse weights and deviations

def weight_variable(shape):
    #produce random noise by truncated normal distribution to avoid symmetry
    initial = tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(initial)
#add some positive numbers(0.1) to avoid dead neurons
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)
#curve
def conv2d(x,w):
    #strides behalf the step length. All of them are 1 which means sweep every point without miss
    #padding behalf the way to deal with the broader. The same size between input and output of curve
    return tf.nn.conv2d(x,w,strides=[1,4,4,1],padding='SAME')
def conv2d_1(x,w):
    #strides behalf the step length. All of them are 1 which means sweep every point without miss
    #padding behalf the way to deal with the broader. The same size between input and output of curve
    return tf.nn.conv2d(x,w,strides=[1,2,2,1],padding='SAME')
def max_pool_2x2(x):
    #step of pooling is 2
    return tf.nn.max_pool(x,ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
#x is feature, y_ is real label
x = tf.placeholder(tf.float32,[None,256,256,3])
y_ = tf.placeholder(tf.float32,[None,2])
x_image = tf.reshape(x,[-1,256,256,3])
#initial parameters
#shape of curve kernel is
w_conv1 = weight_variable([11,11,3,96])
b_conv1 = bias_variable([96])
h_conv1 = tf.nn.relu(conv2d(x_image,w_conv1)+b_conv1)
h_pool1 = max_pool_2x2(h_conv1)
#the second curve. kernel num. is 64
w_conv2 = weight_variable([5,5,96,256])
b_conv2 = bias_variable([256])
h_conv2 = tf.nn.relu(conv2d_1(h_pool1,w_conv2)+b_conv2)
h_pool2 = max_pool_2x2(h_conv2)
#use tf.shape to output tensor format to transfer it into 1D vector
#construct first full connection and hidden nodes num. is 1024
w_fc1 = weight_variable([8*8*256, 512])
b_fc1 = bias_variable([512])
h_pool2_flat = tf.reshape(h_pool2,[-1, 8*8*256])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,w_fc1)+b_fc1)
#construct second full connection and hidden nodes num. is 1024
w_fc2 = weight_variable([512, 24])
b_fc2 = bias_variable([24])
h_fc2 = tf.nn.relu(tf.matmul(h_fc1,w_fc2)+b_fc2)
#abandon some nodes to avoid overfitting
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc2, keep_prob)
#connect output of dropout layer to softmax layer and get the last probability
w_fc2 = weight_variable([24,2])
b_fc2 = bias_variable([2])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)
#define cross Entropy using Adam. learning rate is 1e-4
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y_conv),
                                              reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
#define accuracy
correct_prediction = tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

#start training. iterations 20000, keep_prob 0.5, mini-batch 50, train dataset 1 million.
tf.global_variables_initializer().run()

# 调用mycnn1
data = sio.loadmat('data.mat')
train = data['train']
train_labels = data['train_labels']
test = data['test']
# test = np.reshape(test, [len(test), 256*256])
test_labels = data['test_labels']
for i in range(2000):
    #mini batch is a method to calculate gradient
    batch = mycnn1.getbatch(train, train_labels, 50)
    if i%10 == 0:
        train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
        print('step %d, training accuracy %g'%(i, train_accuracy))
    train_step.run(feed_dict={x:batch[0], y_:batch[1], keep_prob:1.0})
    if i%20 == 0:
        print 'test accuracy %g'%accuracy.eval(feed_dict={x: test, y_: test_labels, keep_prob: 1.0})