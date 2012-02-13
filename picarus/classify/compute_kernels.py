import hadoopy
import picarus._file_parse as file_parse
import os
import picarus._kernels as kernels
import numpy as np


class Mapper(object):

    def __init__(self):
        # |X| x |Y| : Each feature in X corresponds to a row and each feature in Y corresponds to a column
        self.rows_per_chunk = os.environ.get('ROWS_PER_CHUNK', 500)
        self.input_to_id_y = dict((y, x) for x, y in enumerate(sorted(file_parse.load(os.environ['LOCAL_LABELS_FN_Y'])['inputs'].keys())))
        self.input_to_id_x = None
        if 'LOCAL_LABELS_FN_X' in os.environ:
            self.input_to_id_x = dict((y, x) for x, y in enumerate(sorted(file_parse.load(os.environ['LOCAL_LABELS_FN_X'])['inputs'].keys())))
        if self.input_to_id_x is not None:
            self.num_chunks = int(np.ceil(len(self.input_to_id_x) / float(self.rows_per_chunk)))
        else:
            self.num_chunks = int(np.ceil(len(self.input_to_id_y) / float(self.rows_per_chunk)))

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
        if image_hash in self.input_to_id_y:
            col_num = self.input_to_id_y[image_hash]
            for chunk_num in range(self.num_chunks):
                yield chunk_num, ('y', col_num, feature)

        if self.input_to_id_x is not None and image_hash in self.input_to_id_x:
            row_num = self.input_to_id_x[image_hash]
            yield row_num / self.rows_per_chunk, ('x', row_num, feature)


class Reducer(object):

    def __init__(self):
        self.use_y_as_x = 'LOCAL_LABELS_FN_X' not in os.environ
        self.rows_per_chunk = os.environ.get('ROWS_PER_CHUNK', 500)

    def reduce(self, chunk_num, values):
        """

        Args:
            key: (see mapper)
            values: Iterator of values (see mapper)

        Yields:
            A tuple in the form of (key, value)
            key: 
            value: 
        """
        target_kernels = ['hik']
        x_values = []
        y_values = []
        for x, y, z in values:
            if 'x' == x:
                x_values.append((y, z))
            elif 'y' == x:
                y_values.append((y, z))
            else:
                raise ValueError(x)
        y_matrix = np.vstack([x[1] for x in sorted(y_values)])
        if self.use_y_as_x:
            for row_num in range(chunk_num * self.rows_per_chunk, min((chunk_num + 1) * self.rows_per_chunk, y_matrix.shape[0])):
                row_feature = y_matrix[row_num]
                x_values.append((row_num, row_feature))
        for row_num, row_feature in x_values:
            for kernel in target_kernels:
                yield (kernel, row_num), kernels.compute(kernel, row_feature.reshape((1, row_feature.size)), y_matrix).ravel()


if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
