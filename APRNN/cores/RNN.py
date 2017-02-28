"""
RNN model for anomaly prediction

2016-12-12
"""
import tensorflow as tf
from tensorflow.python.ops import rnn_cell
from tensorflow.python.ops import seq2seq
import matplotlib.pyplot as plt
from tensorflow.python.ops import variable_scope

import numpy as np


class Model:
    def __init__(self, args, infer=False):
        self.args = args
        # if infer:
        #     args.batch_size = 1
        #     args.seq_length = 1

        if args.model == 'rnn':
            cell_fn = rnn_cell.BasicRNNCell
        elif args.model == 'gru':
            cell_fn = rnn_cell.GRUCell
        elif args.model == 'lstm':
            cell_fn = rnn_cell.BasicLSTMCell
        else:
            raise Exception("model type not supported: {}".format(args.model))

        args.num_layers = 1

        # cell = cell_fn(args.rnn_size, state_is_tuple=True)
        cell = cell_fn(args.rnn_size)

        self.cell = cell = rnn_cell.MultiRNNCell([cell] * args.num_layers, state_is_tuple=True)

        self.output_size = 1

        self.input_data = tf.placeholder(tf.float32, [args.batch_size, args.seq_length, args.vocab_size])
        self.targets = tf.placeholder(tf.int32, [args.batch_size, self.output_size])

        self.initial_state = cell.zero_state(args.batch_size, tf.float32)

        self.vocab_size = args.vocab_size

        # merged_summary_op = tf.merge_all_summaries()
        # summary_writer = tf.train.SummaryWriter('/tmp/mnist_logs', sess.graph)

        with tf.variable_scope('rnn_input'):
            input_w = tf.get_variable("input_w", [args.vocab_size, args.rnn_size])
            input_b = tf.get_variable("input_b", [args.rnn_size])

            flat_input = tf.reshape(self.input_data, [-1, args.vocab_size])

            flat_input = tf.matmul(flat_input, input_w) + input_b

            flat_input = tf.reshape(flat_input, [args.batch_size, args.seq_length, args.rnn_size])

            # flat_input: shape: args.batch_size, args.seq_length, args.rnn_size
            inputs = tf.split(1, args.seq_length, flat_input)
            inputs = [tf.squeeze(input_, [1]) for input_ in inputs]

        with tf.variable_scope('rnn_hidden'):
            outputs, last_state = self.rnn_encode(inputs, self.initial_state, cell, scope='rnn_hidden')

        with tf.variable_scope('rnn_output'):
            output = tf.reshape(tf.concat(1, outputs), [-1, args.rnn_size])

            softmax_w = tf.get_variable("softmax_w", [args.rnn_size, self.output_size])
            softmax_b = tf.get_variable("softmax_b", [self.output_size])
            # self.logits = tf.sigmoid(tf.matmul(output, softmax_w) + softmax_b)
            self.logits = tf.matmul(output, softmax_w) + softmax_b

        loss = tf.reduce_mean(
            tf.square(tf.sub(self.logits, tf.to_float(self.targets))))

        self.cost = loss

        tf.histogram_summary('loss_act', loss)
        tf.scalar_summary('loss', loss)

        self.accuracy = self.compute_accuracy(self.logits, self.targets)

        self.final_state = last_state
        self.lr = tf.Variable(0.0, trainable=False)
        tvars = tf.trainable_variables()
        grads, _ = tf.clip_by_global_norm(tf.gradients(self.cost, tvars),
                                          args.grad_clip)
        optimizer = tf.train.AdamOptimizer(self.lr)
        self.train_op = optimizer.apply_gradients(zip(grads, tvars))

        self.merged = tf.merge_all_summaries()

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
        # int_target = tf.to_int32(tf.reshape(target, [-1, self.vocab_size]))
        return tf.contrib.metrics.accuracy(sign_logit, target)

    def test(self, sess, input_datas):
        accu = 0
        for i in range(len(input_datas) - 1):
            input_data = input_datas[i]
            input_data = np.reshape(np.array(input_data), (1, 1, len(input_data)))
            target = input_datas[i + 1]
            target = np.reshape(np.array(target), (1, 1, len(target)))
            feed = {self.input_data: input_data, self.targets: target}
            logits, accuracy = sess.run([self.logits, self.accuracy], feed)
            accu += accuracy
            # accu += compute_accuracy(logits, input_datas[i + 1])
        return accu / (len(input_datas) - 1)

    def plot(self, sess, chars):
        pass
        # embedding = sess.run(self.embedding)
        # for i, symbol in enumerate(chars):
        #     x, y = embedding[i][0], embedding[i][1]
        #     plt.scatter(x, y)
        #     plt.annotate(symbol, xy=(x, y), xytext=(5, 2),
        #                  textcoords='offset points', ha='right', va='bottom', size=4)
        # plt.savefig("market2vec.png", dpi=600)
        # print(len(softmax_w))
        # print(softmax_w)
