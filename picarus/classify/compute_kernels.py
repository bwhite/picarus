import hadoopy
import picarus._file_parse as file_parse
import os
import picarus._kernels as kernels
import numpy as np

ROWS_PER_CHUNK = 100


class Mapper(object):

    def __init__(self):
        # |Y| x |X| : Each feature in Y corresponds to a row and each feature in X corresponds to a column
        self.input_to_id_x = dict((y, x) for x, y in enumerate(sorted(file_parse.load(os.environ['LOCAL_LABELS_FN_X'])['inputs'].keys())))
        self.input_to_id_y = None
        if 'LOCAL_LABELS_FN_Y' in os.environ:
            self.input_to_id_y = dict((y, x) for x, y in enumerate(sorted(file_parse.load(os.environ['LOCAL_LABELS_FN_Y'])['inputs'].keys())))
        if self.input_to_id_y is not None:
            self.num_chunks = int(np.ceil(len(self.input_to_id_y) / float(ROWS_PER_CHUNK)))
        else:
            self.num_chunks = int(np.ceil(len(self.input_to_id_x) / float(ROWS_PER_CHUNK)))

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
        if image_hash in self.input_to_id_x:
            col_num = self.input_to_id_x[image_hash]
            for chunk_num in range(self.num_chunks):
                yield chunk_num, ('x', col_num, feature)

        if self.input_to_id_y is not None and image_hash in self.input_to_id_y:
            row_num = self.input_to_id_y[image_hash]
            yield row_num / ROWS_PER_CHUNK, ('y', row_num, feature)


class Reducer(object):

    def __init__(self):
        self.use_x_as_y = 'LOCAL_LABELS_FN_Y' not in os.environ

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
        x_matrix = np.vstack([x[1] for x in sorted(x_values)])
        if self.use_x_as_y:
            for row_num in range(chunk_num * ROWS_PER_CHUNK, min((chunk_num + 1) * ROWS_PER_CHUNK, x_matrix.shape[0])):
                row_feature = x_matrix[row_num]
                y_values.append((row_num, row_feature))
        for row_num, row_feature in y_values:
            for kernel in target_kernels:
                yield (kernel, row_num), kernels.compute(kernel, x_matrix, row_feature.reshape((1, row_feature.size)))


if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
