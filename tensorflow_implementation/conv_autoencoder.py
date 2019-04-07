import tensorflow as tf
import os
from keras.datasets import cifar10
import keras.layers
from datetime import datetime
from image_proc import get_processed_data

net_input = (32, 32, 1)
net_outputs = (32, 32, 2)
hidden_filters = [64, 128, 256]
learning_rate = 0.01

kernel_size = 4

n_epochs = 100
batch_size = 1

X = tf.placeholder(tf.float32, shape=(None, )+net_input)
y = tf.placeholder(tf.float32, shape=(None, )+net_outputs)

with tf.name_scope("convolving_layers"):
    hidden1 = tf.layers.conv2d(X,
                               filters=hidden_filters[0],
                               kernel_size=kernel_size,
                               name="Conv1/input",
                               padding="SAME",
                               activation=tf.nn.relu)
    max_1 = tf.nn.max_pool(hidden1,
                           ksize=[1, 2, 2, 1],
                           strides=[1, 2, 2, 1],
                           padding="VALID",
                           name="pool1")
    hidden2 = tf.layers.conv2d(max_1,
                               filters=hidden_filters[1],
                               kernel_size=kernel_size,
                               name="Conv2",
                               padding="SAME",
                               activation=tf.nn.relu)
    max_2 = tf.nn.max_pool(hidden2,
                           ksize=[1, 2, 2, 1],
                           strides=[1, 2, 2, 1],
                           padding="VALID",
                           name="pool2")
    hidden3 = tf.layers.conv2d(max_2,
                               filters=hidden_filters[2],
                               kernel_size=kernel_size,
                               name="Conv3",
                               padding="SAME",
                               activation=tf.nn.relu)
    max_3 = tf.nn.max_pool(hidden2,
                           ksize=[1, 2, 2, 1],
                           strides=[1, 2, 2, 1],
                           padding="VALID",
                           name="pool3")

with tf.name_scope("deconvolving_layers"):
    hidden4 = tf.layers.conv2d(max_3,
                               filters=hidden_filters[2],
                               name="Conv4",
                               activation=tf.nn.relu,
                               padding="SAME",
                               kernel_size=kernel_size)
    up_1 = tf.keras.layers.UpSampling2D(size=(2, 2),
                                        name="upsample1")(hidden4)
    hidden5 = tf.layers.conv2d(up_1,
                               filters=hidden_filters[1],
                               name="Conv5",
                               activation=tf.nn.relu,
                               padding="SAME",
                               kernel_size=kernel_size)
    up_2 = tf.keras.layers.UpSampling2D(size=(2, 2),
                                        name="upsample2")(hidden5)
    hidden6 = tf.layers.conv2d(up_2,
                               filters=hidden_filters[0],
                               name="Conv6",
                               activation=tf.nn.relu,
                               padding="SAME",
                               kernel_size=kernel_size)
    up3 = tf.keras.layers.UpSampling2D(size=(2, 2),
                                       name="upsample3")(hidden6)
    output = tf.layers.conv2d(hidden6,
                              filters=2,
                              activation=tf.nn.sigmoid,
                              padding="SAME",
                              name="output",
                              kernel_size=3)

with tf.name_scope("loss"):
    mse = tf.reduce_mean(tf.squared_difference(output, y))

with tf.name_scope("train"):
    optimizer = tf.train.AdamOptimizer(learning_rate)
    training_op = optimizer.minimize(mse)

init = tf.global_variables_initializer()
saver = tf.train.Saver()

now = datetime.utcnow().strftime("%X%m%d%H%M%S")
root_logdir = "tf_logs"
logdir = "{}/{}/run-{}/".format(os.getcwd(), root_logdir, now)

mse_summary = tf.summary.scalar('MSE', mse)
file_writer = tf.summary.FileWriter(logdir, tf.get_default_graph())

(x_train_rgb, _), (x_test_rgb, _) = cifar10.load_data()[:100]
x_train, y_train = get_processed_data(x_train_rgb)

with tf.Session() as sess:
    init.run()
    for epoch in range(n_epochs):
        for itr in range(len(x_train) // batch_size):
            X_batch = x_train[itr*batch_size:min((itr+1)*batch_size, len(x_train))]
            y_batch = y_train[itr*batch_size:min((itr+1)*batch_size, len(x_train))]
            sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
        acc_train = mse.eval(feed_dict={X: X_batch, y: y_batch})
        file_writer.add_summary(acc_train, epoch)
        print(epoch, "Training Loss:", acc_train)
    save_path = saver.save(sess, "./my_model_final.ckpt")

file_writer.close()