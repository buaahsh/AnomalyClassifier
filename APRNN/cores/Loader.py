import os
from os.path import isfile, join
from os import listdir
# from six.moves import cPickle
import six
import numpy as np
import pandas


class Loader:
    def __init__(self, data_dir, batch_size, seq_length, encoding='utf-8', kind='normal'):
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.encoding = encoding

        input_files = os.path.join(data_dir, "raw")
        vocab_file = os.path.join(data_dir, "vocab.pkl")
        tensor_file = os.path.join(data_dir, "feature_data.npy")

        if not (os.path.exists(vocab_file) and os.path.exists(tensor_file)):
            print("reading text file")
            self.preprocess(input_files, vocab_file, tensor_file)
        else:
            print("loading preprocessed files")
            self.load_preprocessed(vocab_file, tensor_file)
        self.create_batches(kind)
        self.reset_batch_pointer()

    def preprocess(self, input_files, vocab_file, tensor_file):
        files = [f for f in listdir(input_files) if isfile(join(input_files, f))]
        self.chars = list(map(lambda s: s.split('.')[0], files))
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        with open(vocab_file, 'wb') as f:
            six.moves.cPickle.dump(self.chars, f)

        self.tensor = self.load_tensor(input_files)
        np.save(tensor_file, self.tensor)

    def load_tensor(self, input_files):
        tensor = []
        files = [f for f in listdir(input_files) if isfile(join(input_files, f))]
        for i, f in enumerate(files):
            print(f)
            data = pandas.read_csv(join(input_files, f))
            l = []
            l.append(data.Open.tolist())
            l.append(data.High.tolist())
            l.append(data.Low.tolist())
            l.append(data.Close.tolist())
            l.append(data.Volume.tolist())
            l = np.transpose(np.array(l))
            if i == 0:
                tensor = np.empty(shape=(l.shape[0], len(files), l.shape[1]))
            if l.shape[0] != tensor.shape[0]:
                continue
            tensor[:,i,:] = l
        return tensor
        # return tensor

    def load_preprocessed(self, vocab_file, tensor_file):
        with open(vocab_file, 'rb') as f:
            self.chars = six.moves.cPickle.load(f)
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        self.tensor = np.load(tensor_file)
        self.num_batches = int(self.tensor.size / (self.batch_size *
                                                   self.seq_length))

    def create_batches(self, kind):
        print("creating batches")
        if kind == 'normal':
            self.num_batches = int(self.tensor.shape[0] / (self.batch_size * self.seq_length))

            # When the data (tensor) is too small, let's give them a better error message
            if self.num_batches == 0:
                assert False, "Not enough data. Make seq_length and batch_size small."

            self.tensor = self.tensor[:self.num_batches * self.batch_size * self.seq_length]
            xdata = self.tensor
            ydata = np.copy(self.tensor)

            ydata[:-1] = xdata[1:]
            ydata[-1] = xdata[0]

            self.x_batches = np.split(xdata, self.num_batches, 0)
            self.x_batches = np.array([np.split(x, len(x) / self.seq_length, 0) for x in self.x_batches])
            self.y_batches = np.split(ydata, self.num_batches, 0)
            self.y_batches = np.array([np.split(x, len(x) / self.seq_length, 0) for x in self.y_batches])

        elif kind == 'more2one':
            # create movement label
            temp = np.copy(self.tensor[1:])
            temp_label = temp - self.tensor[:-1]

            # change value into movement
            # self.tensor = np.sign((np.sign(temp_label) + 1))
            # temp_label = np.sign((np.sign(temp_label[:,:,-2]) + 1))

            self.tensor = np.sign(temp_label) # input: -1 or 1
            temp_label = np.sign((np.sign(temp_label[:,:,-2]) + 1)) # output: 0 or 1

            self.num_batches = int((self.tensor.shape[0] - self.seq_length + 1) / self.batch_size)
            if self.num_batches == 0:
                assert False, "Not enough data. Make seq_length and batch_size small."

            if self.batch_size == 1:
                self.num_batches -= 1

            # real value
            # self.tensor = self.tensor[:self.num_batches * self.batch_size + self.seq_length - 1]
            # temp_label = temp_label[:self.num_batches * self.batch_size + self.seq_length - 1]
            #
            # xdata = np.copy(self.tensor)
            # ydata = np.copy(temp_label)
            # self.x_batches = np.split(self.__rolling_window(xdata, self.seq_length), self.num_batches, 0)
            # self.y_batches = np.split(ydata[self.seq_length - 1:], self.num_batches, 0)

            # movement
            self.tensor = self.tensor[:self.num_batches * self.batch_size + self.seq_length]
            temp_label = temp_label[:self.num_batches * self.batch_size + self.seq_length]

            xdata = np.copy(self.tensor)
            ydata = np.copy(temp_label)

            self.x_batches = np.split(self.__rolling_window(xdata[:-1], self.seq_length), self.num_batches, 0)
            self.y_batches = np.split(ydata[self.seq_length:], self.num_batches, 0)

            # #index as output
            # self.tensor = self.tensor[:self.num_batches * self.batch_size + self.seq_length]
            # xdata = np.copy(self.tensor)
            # ydata = self.load_index()
            # ydata = np.reshape(ydata, newshape=(ydata.shape[0], 1))
            # ydata = ydata[1:] - ydata[:-1]
            # ydata = np.sign((np.sign(ydata) + 1))
            # ydata = ydata[:self.num_batches * self.batch_size + self.seq_length]
            #
            # self.x_batches = np.split(self.__rolling_window(xdata[:-1], self.seq_length), self.num_batches, 0)
            # self.y_batches = np.split(ydata[self.seq_length:], self.num_batches, 0)

    def next_batch(self):
        x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
        self.pointer += 1
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0

    def load_index(self, file_path='../data/index/raw/^ndq.txt'):
        data = pandas.read_csv(file_path)
        return np.array(data.Close.tolist())

    def __rolling_window(self, a, window):
        # shape = [a.shape[0] - window + 1, window] + [a.shape[-1]]
        # strides = a.strides + (a.strides[-1],)
        # return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)
        r = []
        for i in range(window - 1, a.shape[0]):
            r.append(a[i - window + 1: i + 1])
        return np.array(r)

    def write_to_file(self, output_file):
        # create movement label
        temp = np.copy(self.tensor[1:])
        temp_label = temp - self.tensor[:-1]

        # change value into movement
        # self.tensor = np.sign((np.sign(temp_label) + 1))
        # temp_label = np.sign((np.sign(temp_label[:,:,-2]) + 1))

        self.tensor = np.sign(temp_label)
        temp_label = np.sign((np.sign(temp_label[:, :, -2]) + 1))

        self.num_batches = int((self.tensor.shape[0] - self.seq_length + 1) / self.batch_size)
        self.tensor = self.tensor[:self.num_batches * self.batch_size + self.seq_length]
        temp_label = temp_label[:self.num_batches * self.batch_size + self.seq_length]

        xdata = np.copy(self.tensor)
        ydata = np.copy(temp_label)

        # xdata = self.__rolling_window(xdata[:-1], self.seq_length)
        xdata = np.reshape(xdata, [-1, xdata.shape[-1]])
        ydata = np.reshape(ydata, [-1, 1])

        xdata = xdata[:-1]
        ydata = ydata[1:]

        all_data = np.zeros(shape=[xdata.shape[0], xdata.shape[1] + 1])
        all_data[:, :xdata.shape[1]] = xdata
        all_data[:, xdata.shape[1]:] = ydata
        np.savetxt(output_file, all_data, delimiter=',', fmt='%.3f')

if __name__ == "__main__":
    data_dir = '../data/stock_5m'
    batch_size = 50
    seq_length = 5
    data_loader = Loader(data_dir, batch_size, seq_length, kind='more2one')
    print(data_loader.chars)
    # data_loader.write_to_file('tensor_2.txt')
