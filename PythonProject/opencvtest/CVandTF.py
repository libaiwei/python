import tensorflow as tf
import cv2

# First, load the image again
filename = "/Users/lbw/Desktop/user.png"
raw_image_data = cv2.imread(filename)

image = tf.placeholder("uint8", [None, None, 3])
slice = tf.slice(image, [200, 0, 0], [300, -1, -1])

with tf.Session() as session:
    result = session.run(slice, feed_dict={image: raw_image_data})
    print 'Slice image shape:', result.shape

cv2.namedWindow('image', 0)
cv2.imshow('image', result)
cv2.waitKey(0)