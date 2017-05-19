# coding:utf8
import tensorflow as tf
# a = tf.constant(2)
# b = tf.constant(3)
# with tf.Session() as sess:
#     print('a=2,b=3')
#     print('Addition with constants: %i' % sess.run(a+b))
#     print('Multiplication with constants: %i' % sess.run(a*b))

#placeholder
a = tf.placeholder(tf.int16)
b = tf.placeholder(tf.int16)
add = tf.add(a, b)
mul = tf.multiply(a, b)
with tf.Session() as sess:
    print('Addition with variables %i' % sess.run(add, feed_dict={a:2, b:3}))
    print('Multiplication with variables: %i' % sess.run(mul, feed_dict={a:2, b:3}))
