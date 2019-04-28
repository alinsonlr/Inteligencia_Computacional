# -*- coding: utf-8 -*-
"""prueba_tf_3_v07_alumnos.ipynb

Automatically generated by Colaboratory.
"""

#https://medium.com/@curiousily/tensorflow-for-hackers-part-ii-building-simple-neural-network-2d6779d2f91b
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from math import floor, ceil
from pylab import rcParams

# %matplotlib inline

random_state = 42
np.random.seed(random_state)
tf.set_random_seed(random_state)

!ls

D = np.loadtxt('sensorless_tarea2_train.txt', delimiter=',')

nc = D.shape[1]-1
data_x = D[:,0:nc]
data_y = D[:,nc] - 1
data_y = data_y.astype(int)

from sklearn.preprocessing import LabelBinarizer
label_binarizer = LabelBinarizer()
label_binarizer.fit(range(max(data_y)+1))
data_y = label_binarizer.transform(data_y).astype(float)

train_size = 0.8

train_cnt = floor(data_x.shape[0] * train_size)
x_train = data_x[0:train_cnt,:]
y_train = data_y[0:train_cnt,:]
x_valid = data_x[train_cnt:,:]
y_valid = data_y[train_cnt:,:]

def multilayer_perceptron(x, weights, biases, keep_prob):
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.sigmoid(layer_1)
    layer_1 = tf.nn.dropout(layer_1, keep_prob)
    out_layer = tf.matmul(layer_1, weights['out']) + biases['out']
    return out_layer

n_hidden_1 = 28
n_input = data_x.shape[1]
n_classes = data_y.shape[1]

weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'out': tf.Variable(tf.random_normal([n_hidden_1, n_classes]))
}

biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

keep_prob = tf.placeholder("float")

training_epochs = 1500
display_step = 100
batch_size = 32

x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, n_classes])

predictions = multilayer_perceptron(x, weights, biases, keep_prob)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=predictions, labels=y))

optimizer = tf.train.AdamOptimizer(learning_rate=0.001).minimize(cost)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    
    for epoch in range(training_epochs):
        avg_cost = 0.0
        total_batch = int(len(x_train) / batch_size)
        x_batches = np.array_split(x_train, total_batch)
        y_batches = np.array_split(y_train, total_batch)
        for i in range(total_batch):
            batch_x, batch_y = x_batches[i], y_batches[i]
            _, c = sess.run([optimizer, cost], 
                            feed_dict={
                                x: batch_x, 
                                y: batch_y, 
                                keep_prob: 0.8
                            })
            avg_cost += c / total_batch
        if epoch % display_step == 0:
            print("Epoch:", '%04d' % (epoch+1), "cost=", \
                "{:.9f}".format(avg_cost))
            correct_prediction = tf.equal(tf.argmax(predictions, 1), tf.argmax(y, 1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
            print("Accuracy validation:", accuracy.eval({x: x_valid, y: y_valid, keep_prob: 1.0}))

    print("Optimization Finished!")

    correct_prediction = tf.equal(tf.argmax(predictions, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy validation:", accuracy.eval({x: x_valid, y: y_valid, keep_prob: 1.0}))
    print("Confusion matrix validation")
    confm = tf.confusion_matrix(tf.argmax(y,1),tf.argmax(predictions, 1), num_classes = y_valid.shape[1])
    print( confm.eval({x: x_valid, y: y_valid, keep_prob: 1.0}) )



