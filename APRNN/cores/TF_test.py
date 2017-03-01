import tensorflow as tf
import numpy as np
from tensorflow.python.framework import ops

with tf.Session() as sess:
    o = tf.constant([[1, 2, 3], [4, 5, 6]])
    x = tf.constant([[7, 8, 9], [10, 11, 12]])
    # y = tf.constant([0, 1, 1, 0])
    # z = tf.cast(tf.equal(x, y), tf.float32)
    print(sess.run(tf.concat(1, [o, x])))