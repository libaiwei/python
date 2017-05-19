# coding:utf8
import tensorflow as tf
hello = tf.constant('hell world')
sess = tf.Session()
print(sess.run(hello))