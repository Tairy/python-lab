# encoding:utf-8
import tensorflow as tf
import numpy as np

# a = tf.constant([5, 3], name="input_a")
# b = tf.reduce_prod(a, name="prod_b")
# c = tf.reduce_sum(a, name="sum_c")
# d = tf.add(c, d, name="add_d")

# sess = tf.Session()
# output = sess.run(e)
# writer = tf.summary.FileWriter('./my_graph', sess.graph)
# writer.close()
# sess.close()

a = np.array([2, 3], dtype=np.int32)
print(a)