"""
RNN model for stock price movement prediction,
sequence 2 sequence.
2016-12-12
"""
import tensorflow as tf
from tensorflow.python.ops import rnn_cell
from tensorflow.python.ops import seq2seq
import matplotlib.pyplot as plt

import numpy as np


class Model:
    def __init__(self, args, infer=False):
        self.args = args
        if infer:
            args.batch_size = 1
            args.seq_length = 1

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

        self.input_data = tf.placeholder(tf.int32, [args.batch_size, args.seq_length, args.vocab_size])
        self.targets = tf.placeholder(tf.int32, [args.batch_size, args.seq_length, args.vocab_size])

        # self.input_data = tf.placeholder(tf.int32, [args.batch_size, args.seq_length])
        # self.targets = tf.placeholder(tf.int32, [args.batch_size, args.seq_length])

        self.initial_state = cell.zero_state(args.batch_size, tf.float32)

        self.vocab_size = args.vocab_size

        with tf.variable_scope('rnnlm'):
            softmax_w = tf.get_variable("softmax_w", [args.rnn_size, args.vocab_size])
            softmax_b = tf.get_variable("softmax_b", [args.vocab_size])
            with tf.device("/cpu:0"):
                embedding = tf.get_variable("embedding", [args.vocab_size, args.rnn_size])
                print(embedding)
                print(self.input_data)
                # print(tf.batch_matmul(self.input_data, embedding))
                embedding_lookup = tf.reduce_sum(tf.nn.embedding_lookup(embedding, self.input_data), 2)

                print(embedding_lookup)
                # inputs = tf.split(1, args.seq_length, tf.nn.embedding_lookup(embedding, self.input_data))

                inputs = tf.split(1, args.seq_length, embedding_lookup)
                inputs = [tf.squeeze(input_, [1]) for input_ in inputs]
            self.embedding = embedding

        def loop(prev, _):
            prev = tf.matmul(prev, softmax_w) + softmax_b
            prev_symbol = tf.stop_gradient(tf.argmax(prev, 1))
            return tf.nn.embedding_lookup(embedding, prev_symbol)

        outputs, last_state = seq2seq.rnn_decoder(inputs, self.initial_state, cell,
                                                  loop_function=loop if infer else None, scope='rnnlm')
        output = tf.reshape(tf.concat(1, outputs), [-1, args.rnn_size])
        self.logits = tf.sigmoid(tf.matmul(output, softmax_w) + softmax_b)

        # Standard rnn algo, it doesnt work
        # def softmax_loss_function(logit, target):
        #     return nn_ops.softmax_cross_entropy_with_logits(logit, target)

        # loss = seq2seq.sequence_loss_by_example([self.probs],
        #                                         [tf.reshape(self.targets, [-1, args.vocab_size])],
        #                                         [tf.ones([args.batch_size * args.seq_length])],
        #                                         args.vocab_size,
        #                                         softmax_loss_function=softmax_loss_function)

        # self.cost = tf.reduce_sum(loss) / args.batch_size / args.seq_length

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

    def compute_accuracy(self, logit, target):
        sign_logit = tf.cast(tf.greater(logit, 0.5), tf.int32)
        int_target = tf.to_int32(tf.reshape(target, [-1, self.vocab_size]))
        return tf.contrib.metrics.accuracy(sign_logit, int_target)

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
        embedding = sess.run(self.embedding)
        for i, symbol in enumerate(chars):
            x, y = embedding[i][0], embedding[i][1]
            plt.scatter(x, y)
            plt.annotate(symbol, xy=(x, y), xytext=(5, 2),
                         textcoords='offset points', ha='right', va='bottom', size=4)
        plt.savefig("market2vec.png", dpi=600)
        # print(len(softmax_w))
        # print(softmax_w)
