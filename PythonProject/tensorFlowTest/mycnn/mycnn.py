import xlrd
import tensorflow as tf
import cv2

#get image and label
data = xlrd.open_workbook('/Users/lbw/Desktop/img1.xlsx')
table = data.sheets()[0]
nrows = table.nrows
images = []
labels = []
for i in xrange(0,nrows,5):
    image = str(table.row_values(i)[0]).split('/')[-1]
    label = 0.0
    for j in xrange(5):
        label += float(table.row_values(i+j)[1])
    if label > 3.0:
        label = 1
    else:
        label = 0
    images.append(image)
    labels.append(label)
print images[0]
path = '/Users/lbw/Desktop/Agg_AMT_Candidates/'
reader = tf.WholeFileReader()

key, value = reader.read(tf.train.string_input_producer([path+str(images[0])]))
image0 = tf.image.decode_jpeg(value)
image = tf.expand_dims(image0, 0)
image_summary = tf.summary.image('origin image', image)
histogram_summary = tf.summary.histogram('image hist',image)
e = tf.reduce_mean(image)
scalar_summary = tf.summary.scalar('image mean', e)

resized_image = tf.image.resize_images(image0, [150, 150], method=tf.image.ResizeMethod.AREA)
img_resize_summary = tf.summary.image('image resized', tf.expand_dims(resized_image, 0))
cropped_image = tf.image.crop_to_bounding_box(image0, 20, 20, 150, 150)
cropped_image_summary = tf.summary.image('image cropped', tf.expand_dims(cropped_image, 0))
flipped_image = tf.image.flip_left_right(image0)
flipped_image_summary = tf.summary.image('image flipped', tf.expand_dims(flipped_image, 0))
rotated_image = tf.image.rot90(image0, k=1)
rotated_image_summary = tf.summary.image('image rotated', tf.expand_dims(rotated_image, 0))
grayed_image = tf.image.rgb_to_grayscale(image0)
grayed_image_summary = tf.summary.image('image grayed', tf.expand_dims(grayed_image, 0))

merged = tf.summary.merge_all()
init_op = tf.initialize_all_variables()

with tf.Session() as sess:
    print sess.run(init_op)
    cord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=cord)
    img = image.eval()
    print img.shape
    cord.request_stop()
    cord.join(threads)
    summary_writer = tf.summary.FileWriter('/tmp/tensorboard', sess.graph)

    summary_all = sess.run(merged)

    summary_writer.add_summary(summary_all, 0)

    summary_writer.close()



# def weight_variable(shape):
#     #produce random noise by truncated normal distribution to avoid symmetry
#     initial = tf.truncated_normal(shape,stddev=0.1)
#     return tf.Variable(initial)
# #add some positive numbers(0.1) to avoid dead neurons
# def bias_variable(shape):
#     initial = tf.constant(0.1, shape=shape)
#     return tf.Variable(initial)
# #curve
# def conv2d(x,w):
#     #strides behalf the step length. All of them are 1 which means sweep every point without miss
#     #padding behalf the way to deal with the broader. The same size between input and output of curve
#     return tf.nn.conv2d(x,w,strides=[1,1,1,1],padding='SAME')
# def max_pool_2x2(x):
#     #step of pooling is 2
#     return tf.nn.max_pool(x,ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')
# image = tf.placeholder("uint8", [None, None, 3])
# slice = tf.slice(image, [1000, 0, 0], [3000, -1, -1])
#
# #x is feature, y_ is real label
# x = tf.placeholder(tf.float32,[None,784])
# y_ = tf.placeholder(tf.float32,[None,10])
# x_image = tf.reshape(x,[-1,28,28,1])
# #initial parameters
# #shape of curve kernel is
# w_conv1 = weight_variable([5,5,1,32])
# b_conv1 = bias_variable([32])
# h_conv1 = tf.nn.relu(conv2d(x_image,w_conv1)+b_conv1)
# h_pool1 = max_pool_2x2(h_conv1)
# #the second curve. kernel num. is 64
# w_conv2 = weight_variable([5,5,32,64])
# b_conv2 = bias_variable([64])
# h_conv2 = tf.nn.relu(conv2d(h_pool1,w_conv2)+b_conv2)
# h_pool2 = max_pool_2x2(h_conv2)
# #use tf.shape to output tensor format to transfer it into 1D vector
# #construct full connection and hidden nodes num. is 1024
# w_fc1 = weight_variable([7*7*64, 1024])
# b_fc1 = bias_variable([1024])
# h_pool2_flat = tf.reshape(h_pool2,[-1, 7*7*64])
# h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat,w_fc1)+b_fc1)
# #abandon some nodes to avoid overfitting
# keep_prob = tf.placeholder(tf.float32)
# h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
# #connect output of dropout layer to softmax layer and get the last probability
# w_fc2 = weight_variable([1024,10])
# b_fc2 = bias_variable([10])
# y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)
# #define cross Entropy using Adam. learning rate is 1e-4
# cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_*tf.log(y_conv),
#                                               reduction_indices=[1]))
# train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
# #define accuracy
# correct_prediction = tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1))
# accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
#
# #start training. iterations 20000, keep_prob 0.5, mini-batch 50, train dataset 1 million.
# tf.global_variables_initializer().run()
# for i in range(20000):
#     #mini batch is a method to calculate gradient
#     batch = mnist.train.next_batch(50)
#     print type(batch),batch
#     if i%100 == 0:
#         train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
#         print('step %d, training accuracy %g'%(i, train_accuracy))
#     train_step.run(feed_dict={x:batch[0], y_:batch[1], keep_prob:1.0})
# print 'test accuracy %g'%accuracy.eval(feed_dict={x: mnist.test.images, y_:mnist.test.lables, keep_prob:1.0})