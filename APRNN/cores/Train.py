from __future__ import print_function

import argparse
import datetime
import os
import time

import six
import tensorflow as tf

from cores.RNN import Model
from cores.Loader import Loader


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='../data/rubis_train',
                        help='data directory containing input.txt')
    parser.add_argument('--save_dir', type=str, default='../save',
                        help='directory to store checkpointed models')
    parser.add_argument('--rnn_size', type=int, default=10,
                        help='size of RNN hidden state')
    parser.add_argument('--num_layers', type=int, default=1,
                        help='number of layers in the RNN')
    parser.add_argument('--model', type=str, default='gru',
                        help='rnn, gru, or lstm')
    parser.add_argument('--batch_size', type=int, default=1000,
                        help='minibatch size')
    parser.add_argument('--seq_length', type=int, default=5,
                        help='RNN sequence length')
    parser.add_argument('--num_epochs', type=int, default=500,
                        help='number of epochs')
    parser.add_argument('--save_every', type=int, default=80,
                        help='save frequency')
    parser.add_argument('--grad_clip', type=float, default=5.,
                        help='clip gradients at this value')
    parser.add_argument('--learning_rate', type=float, default=0.4,
                        help='learning rate')
    parser.add_argument('--decay_rate', type=float, default=0.999,
                        help='decay rate for rmsprop')
    parser.add_argument('--init_from', type=str, default=None,
                        help="""continue training from saved model at this path. Path must contain files saved by previous training process:
                                'config.pkl'        : configuration;
                                'chars_vocab.pkl'   : vocabulary definitions;
                                'checkpoint'        : paths to model file(s) (created by tf).
                                                      Note: this file contains absolute paths,
                                                      be careful when moving files around;
                                'model.ckpt-*'      : file(s) with model definition (created by tf)
                            """)
    parser.add_argument('--feature_size', type=int, default=5, help='')
    parser.add_argument('--dropout_prob', type=float, default=0.8, help='')
    return parser.parse_args()


def main():
    args = get_arguments()
    train(args)


def load_best_model(args, sess):
    saver = tf.train.Saver(tf.global_variables())
    ckpt = tf.train.get_checkpoint_state(args.save_dir)
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)


def train(args):
    # data_loader = StockLoader(args.data_dir, args.batch_size, args.seq_length, kind='normal')
    data_loader = Loader(args.data_dir, args.batch_size, args.seq_length, kind='normal')

    args.vocab_size = data_loader.vocab_size
    ckpt = None

    # check compatibility if training is continued from previously saved model
    if args.init_from is not None:
        # check if all necessary files exist
        assert os.path.isdir(args.init_from), " %s must be a a path" % args.init_from
        assert os.path.isfile(
            os.path.join(args.init_from, "config.pkl")), "config.pkl file does not exist in path %s" % args.init_from
        assert os.path.isfile(os.path.join(args.init_from,
                                           "chars_vocab.pkl")), "chars_vocab.pkl.pkl file does not exist in path %s" \
                                                                % args.init_from
        ckpt = tf.train.get_checkpoint_state(args.init_from)
        assert ckpt, "No checkpoint found"
        assert ckpt.model_checkpoint_path, "No model path found in checkpoint"

        # open old config and check if models are compatible
        with open(os.path.join(args.init_from, 'config.pkl')) as f:
            saved_model_args = six.moves.cPickle.load(f)
        need_be_same = ["model", "rnn_size", "num_layers", "seq_length"]
        for checkme in need_be_same:
            assert vars(saved_model_args)[checkme] == vars(args)[
                checkme], "Command line argument and saved model disagree on '%s' " % checkme

        # open saved vocab/dict and check if vocabs/dicts are compatible
        with open(os.path.join(args.init_from, 'chars_vocab.pkl')) as f:
            saved_chars, saved_vocab = six.moves.cPickle.load(f)
        assert saved_chars == data_loader.chars, "Data and loaded model disagree on character set!"
        assert saved_vocab == data_loader.vocab, "Data and loaded model disagree on dictionary mappings!"

    with open(os.path.join(args.save_dir, 'config.pkl'), 'wb') as f:
        six.moves.cPickle.dump(args, f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'wb') as f:
        six.moves.cPickle.dump((data_loader.chars, data_loader.vocab), f)

    print('init model...', datetime.datetime.now())
    model = Model(args)
    print('model has built...', datetime.datetime.now())

    with tf.Session() as sess:


        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=100)
        # restore model
        if args.init_from is not None:
            saver.restore(sess, ckpt.model_checkpoint_path)

        print("Start training... num_batch: {0}".format(data_loader.num_batches))

        train_ratio = 1
        dev_ratio = 0
        train_index = int(data_loader.num_batches * train_ratio)
        dev_index = int(data_loader.num_batches * dev_ratio)
        # train_index = 4
        # dev_index = 1

        max_acc = 0
        down_time = 0
        learning_rate = args.learning_rate
        sess.run(tf.assign(model.lr, learning_rate))

        train_writer = tf.train.SummaryWriter('../save/summary/train', sess.graph)

        for e in range(args.num_epochs):
            learning_rate = args.learning_rate * (args.decay_rate ** e)
            sess.run(tf.assign(model.lr, learning_rate))

            for b in range(0, train_index):
                start = time.time()
                x, y = data_loader.x_batches[b], data_loader.y_batches[b]
                feed = {model.input_data: x, model.targets: y}

                summary, train_loss, state, _, accuracy = sess.run([model.merged, model.cost, model.final_state,
                                                           model.train_op, model.accuracy], feed)
                train_writer.add_summary(summary, e * train_index + b)
                end = time.time()
                print("{}/{} (epoch {}), train_loss = {:.3f}, accuracy = {:.3f}, time/batch = {:.3f}, learning rate = "
                      "{}".format(
                    e * train_index + b,
                    e,
                    args.num_epochs * train_index, train_loss, accuracy, end - start, learning_rate))

                # if (e * train_index + b) % args.save_every == 0 \
                #         or (e == args.num_epochs - 1 and b == data_loader.num_batches - 1):  # save for the last result
                #     accuracy = 0
                #     for dev_b in range(train_index, train_index + dev_index):
                #         x, y = data_loader.x_batches[dev_b], data_loader.y_batches[dev_b]
                #         feed = {model.input_data: x, model.targets: y}
                #         accuracies = sess.run([model.accuracy], feed)
                #         accuracy += sum(accuracies) / len(accuracies)
                #     accuracy /= dev_index
                #
                #     if accuracy > max_acc:
                #         down_time = 0
                #     else:
                #         down_time += 1
                #     if down_time == 6:
                #         down_time = 0
                #         print('[INFO] model reloads...', datetime.datetime.now())
                #         load_best_model(args, sess)
                #         learning_rate *= 0.5
                #         sess.run(tf.assign(model.lr, learning_rate))
                #
                #     print("[INFO] dev accuracy = {}, down time = {}".
                #           format(accuracy, down_time))
                #
                #     if accuracy > max_acc:
                #         max_acc = accuracy
                #         checkpoint_path = os.path.join(args.save_dir, 'model.ckpt')
                #         saver.save(sess, checkpoint_path, global_step=e * train_index + b)
                #         print("[INFO] model saved to {}, accuracy = {}".format(checkpoint_path, accuracy))
                #
                #     # for test data
                #     accuracy = 0
                #     for dev_b in range(train_index + dev_index, data_loader.num_batches):
                #         x, y = data_loader.x_batches[dev_b], data_loader.y_batches[dev_b]
                #         feed = {model.input_data: x, model.targets: y}
                #         accuracies = sess.run([model.accuracy], feed)
                #         accuracy += sum(accuracies) / len(accuracies)
                #     accuracy /= (data_loader.num_batches - train_index - dev_index)
                #     print("[INFO] test accuracy = {}".format(accuracy))

if __name__ == '__main__':
    main()
