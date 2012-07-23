import hadoopy
import picarus._file_parse as file_parse
import os
import picarus._kernels as kernels
import numpy as np
import time
import json
import collections


def _tuple_to_key(key):
    return u'\t'.join(map(str, key))


def _key_to_tuple(key):
    return key.split('\t')

class Mapper(object):

    def __init__(self):
        # |X| x |Y| : Each feature in X corresponds to a row and each feature in Y corresponds to a column
        self.rows_per_chunk = int(os.environ.get('ROWS_PER_CHUNK', 500))
        self.cols_per_chunk = int(os.environ.get('COLS_PER_CHUNK', 500))
        self.input_to_id_x = dict((y, x) for x, y in enumerate(sorted(file_parse.load(os.environ['LOCAL_LABELS_FN_X']))))
        self.input_to_id_y = dict((y, x) for x, y in enumerate(sorted(file_parse.load(os.environ['LOCAL_LABELS_FN_Y']))))
        self.num_row_chunks = int(np.ceil(len(self.input_to_id_x) / float(self.rows_per_chunk)))
        self.num_col_chunks = int(np.ceil(len(self.input_to_id_y) / float(self.cols_per_chunk)))
        print('Row Chunks[%d] Col Chunks[%d]' % (self.num_row_chunks, self.num_col_chunks))

    def map(self, image_hash, feature):
        """

        Args:
            image_hash: Unique image string
            feature: Numpy image feature

        Yields:
            A tuple in the form of (classifier_name, label_value)
            classifier_name: String representing the classifier
            label_value: (label, feature) where label is an int
        """
        # Each Y value needs to get send to each row (one column chunk for that row will get it)
        if image_hash in self.input_to_id_y:
            col_num = self.input_to_id_y[image_hash]
            col_chunk_num = col_num / self.cols_per_chunk
            for row_chunk_num in range(self.num_row_chunks):
                yield _tuple_to_key((col_chunk_num, row_chunk_num, 0)), (col_num, feature)

        # Each X value needs to get send to each col (one row chunk for that col will get it)
        if image_hash in self.input_to_id_x:
            row_num = self.input_to_id_x[image_hash]
            row_chunk_num = row_num / self.rows_per_chunk
            for col_chunk_num in range(self.num_col_chunks):
                yield _tuple_to_key((col_chunk_num, row_chunk_num, 1)), (row_num, feature)


class Reducer(object):

    def __init__(self):
        self.rows_per_chunk = int(os.environ.get('ROWS_PER_CHUNK', 500))
        self.cols_per_chunk = int(os.environ.get('COLS_PER_CHUNK', 500))
        self._total_time = collections.defaultdict(lambda: 0)
        self._num_dims = 0
        self._num_vecs = collections.defaultdict(lambda: 0)
        self._prev_col_chunk_num = None
        self.col_num = None
        self.y_matrix = None

    def reduce(self, col_row_chunk_num, values):
        """

        Args:
            key: (see mapper)
            values: Iterator of values (see mapper)

        Yields:
            A tuple in the form of (key, value)
            key: 
            value: 
        """
        print(col_row_chunk_num)
        col_chunk_num, row_chunk_num, vec = map(int, _key_to_tuple(col_row_chunk_num))
        if self._prev_col_chunk_num is None:
            self.reset(col_chunk_num)
        if col_chunk_num != self._prev_col_chunk_num:
            self.reset(col_chunk_num)
        if vec == 0:
            y_values = list(values)
            y_values = sorted(y_values)
            self.col_num = y_values[0][0]
            y_values = [x[1] for x in y_values]
            self.y_matrix = np.vstack(y_values)
            del y_values
            print(self.y_matrix.shape)
            self._num_dims = self.y_matrix.shape[1]
        else:
            unnormalized_target_kernels = []  # 'linear'
            normalized_target_kernels = ['hik']
            if 0:
                # Unnormalized
                for row_num, row_feature in values:
                    row_feature = row_feature.reshape((1, row_feature.size))
                    for kernel in unnormalized_target_kernels:
                        st = time.time()
                        k = kernels.compute(kernel, row_feature, self.y_matrix).ravel()
                        self._total_time[kernel] += time.time() - st
                        self._num_vecs[kernel] += self.y_matrix.shape[0]
                        yield (kernel, row_num, self.col_num), k
            else:
                # Normalized
                self.y_matrix = (self.y_matrix.T / np.sum(self.y_matrix, 1)).T
                for row_num, row_feature in values:
                    row_feature = row_feature.reshape((1, row_feature.size)) / np.sum(row_feature)
                    for kernel in normalized_target_kernels:
                        st = time.time()
                        k = kernels.compute(kernel, row_feature, self.y_matrix).ravel()
                        self._total_time[kernel] += time.time() - st
                        self._num_vecs[kernel] += self.y_matrix.shape[0]
                        yield (kernel, row_num, self.col_num), k

    def reset(self, col_chunk_num):
        self._prev_col_chunk_num = col_chunk_num
        self.col_num = None
        self.y_matrix = None

    def close(self):
        if self._num_vecs:
            print(json.dumps({'total_time': dict(self._total_time),
                              'num_vecs': dict(self._num_vecs),
                              'num_dims': self._num_dims}))


if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
