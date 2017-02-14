"""
RNN model for stock price movement prediction, sequence to one.
Input is historical features sequence including Open,High,Low,Close,Volume
Output is all stock movement of next moment.

2016-12-15
"""
import tensorflow as tf
from tensorflow.python.ops import rnn_cell
from tensorflow.python.ops import variable_scope
import matplotlib.pyplot as plt

import numpy as np


class Model:
    def __init__(self, args, infer=False):
        self.args = args
        if infer:
            args.batch_size = 1
            # args.seq_length = 1

        if args.model == 'rnn':
            cell_fn = rnn_cell.BasicRNNCell
        elif args.model == 'gru':
            cell_fn = rnn_cell.GRUCell
        elif args.model == 'lstm':
            cell_fn = rnn_cell.BasicLSTMCell
        else:
            raise Exception("model type not supported: {}".format(args.model))

        cell = cell_fn(args.rnn_size, state_is_tuple=True)

        self.cell = cell = rnn_cell.MultiRNNCell([cell] * args.num_layers, state_is_tuple=True)

        self.input_data = tf.placeholder(tf.float32, [args.batch_size, args.seq_length, args.vocab_size, args.feature_size])
        self.targets = tf.placeholder(tf.int32, [args.batch_size, args.vocab_size])

        self.initial_state = cell.zero_state(args.batch_size, tf.float32)

        self.vocab_size = args.vocab_size

        with tf.variable_scope('rnnlm'):
            # initial_state = tf.get_variable("initial_state", [args.batch_size, args.rnn_size])
            softmax_w = tf.get_variable("softmax_w", [args.rnn_size, args.vocab_size])
            softmax_b = tf.get_variable("softmax_b", [args.vocab_size])

            embedding_w = tf.get_variable("element_wise_embedding_w", [args.vocab_size, args.feature_size])
            embedding_b = tf.get_variable("element_wise_embedding_b", [args.vocab_size])
            embedding = tf.get_variable("element_wise_embedding", [args.vocab_size, args.rnn_size])

            # flat_input = tf.reshape(self.input_data, [-1, args.feature_size])
            # xw = tf.matmul(flat_input, tf.transpose(embedding_w)) + embedding_b
            # mask = tf.matrix_diag(tf.ones(shape=self.input_data.get_shape()[:-1]))
            #
            # masked = tf.matmul(tf.reshape(mask, xw.get_shape()), tf.transpose(xw))
            # embedding_lookup = tf.reshape(tf.reduce_sum(masked, 1), self.input_data.get_shape()[:-1])

            flat_input = tf.reshape(self.input_data, [-1, args.feature_size])
            embedding_w = tf.tile(embedding_w, tf.constant([args.batch_size * args.seq_length, 1]))
            xw = tf.reduce_sum(tf.multiply(flat_input, embedding_w), 1)
            embedding_b = tf.tile(embedding_b, tf.constant([args.batch_size * args.seq_length]))
            embedding_lookup = xw + embedding_b

            # embedding_lookup = tf.nn.dropout(embedding_lookup, 0.8)

            embedding_lookup = tf.reshape(tf.matmul(tf.reshape(embedding_lookup, [-1, args.vocab_size]), embedding),
                       [args.batch_size, args.seq_length, args.rnn_size])

            print(embedding_lookup)
            # inputs = tf.split(1, args.seq_length, tf.nn.embedding_lookup(embedding, self.input_data))

            inputs = tf.split(1, args.seq_length, embedding_lookup)
            inputs = [tf.squeeze(input_, [1]) for input_ in inputs]
            self.embedding = embedding

        outputs, last_state = self.rnn_encode(inputs, self.initial_state, cell, scope='rnnlm')
        output = tf.reshape(tf.concat(1, outputs), [-1, args.rnn_size])
        self.logits = tf.sigmoid(tf.matmul(output, softmax_w) + softmax_b)

        loss = tf.reduce_mean(
            tf.square(tf.sub(self.logits, tf.to_float(tf.reshape(self.targets, [-1, args.vocab_size])))))

        self.cost = loss
        self.accuracy = self.compute_accuracy(self.logits, self.targets)

        self.final_state = last_state
        self.lr = tf.Variable(0.0, trainable=False)
        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, tvars),
                                          args.grad_clip)
        optimizer = tf.train.AdamOptimizer(self.lr)
        self.train_op = optimizer.apply_gradients(zip(grads, tvars))

    def rnn_encode(self, encoder_inputs, initial_state, cell, scope=None):
        with variable_scope.variable_scope(scope or "rnn_encoder"):
            state = initial_state
            output = None
            for i, inp in enumerate(encoder_inputs):
                if i > 0:
                    variable_scope.get_variable_scope().reuse_variables()
                output, state = cell(inp, state)
            return output, state

    def compute_accuracy(self, logit, target):
        sign_logit = tf.cast(tf.greater(logit, 0.5), tf.int32)
        int_target = tf.to_int32(tf.reshape(target, [-1, self.vocab_size]))
        return tf.contrib.metrics.accuracy(sign_logit, int_target)

    def test(self, sess, data_loader, start_id, seq_length):
        accu = 0
        for i in range(start_id, len(data_loader.x_batches)):
            # input_data = input_datas[i - seq_length + 1: i + 1]
            input_data = data_loader.x_batches[i]
            # input_data = np.reshape(np.array(input_data), (1, seq_length, len(input_data[seq_length - 1])))
            # target = input_datas[i + 1]
            target = data_loader.y_batches[i]
            # target = np.reshape(np.array(target), (1, len(target)))
            feed = {self.input_data: input_data, self.targets: target}
            logits, accuracy = sess.run([self.logits, self.accuracy], feed)
            accu += accuracy
            print(accu / (i - start_id + 1))
            # accu += compute_accuracy(logits, input_datas[i + 1])
        return accu / (len(data_loader.x_batches) - start_id)

    def plot(self, sess, chars):
        embedding = sess.run(self.embedding)
        for i, symbol in enumerate(chars):
            x, y = embedding[i][0], embedding[i][1]
            plt.scatter(x, y)
            plt.annotate(symbol, xy=(x, y), xytext=(5, 2),
                         textcoords='offset points', ha='right', va='bottom', size=4)
        plt.savefig("market2vec.png", dpi=600)
        # print(len(softmax_w))
        # print(softmax_w)
