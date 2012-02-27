import hadoopy
import picarus._file_parse as file_parse
import os
import picarus._kernels as kernels
import numpy as np


class Mapper(object):

    def __init__(self):
        # |X| x |Y| : Each feature in X corresponds to a row and each feature in Y corresponds to a column
        self.rows_per_chunk = int(os.environ.get('ROWS_PER_CHUNK', 500))
        self.cols_per_chunk = int(os.environ.get('COLS_PER_CHUNK', 500))
        self.input_to_id_x = dict((y, x) for x, y in enumerate(sorted(file_parse.load(os.environ['LOCAL_LABELS_FN_X'])['inputs'].keys())))
        self.input_to_id_y = dict((y, x) for x, y in enumerate(sorted(file_parse.load(os.environ['LOCAL_LABELS_FN_Y'])['inputs'].keys())))
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
                yield (row_chunk_num, col_chunk_num), ('y', col_num, feature)

        # Each X value needs to get send to each col (one row chunk for that col will get it)
        if image_hash in self.input_to_id_x:
            row_num = self.input_to_id_x[image_hash]
            row_chunk_num = row_num / self.rows_per_chunk
            for col_chunk_num in range(self.num_col_chunks):
                yield (row_chunk_num, col_chunk_num), ('x', row_num, feature)


class Reducer(object):

    def __init__(self):
        self.rows_per_chunk = int(os.environ.get('ROWS_PER_CHUNK', 500))
        self.cols_per_chunk = int(os.environ.get('COLS_PER_CHUNK', 500))

    def reduce(self, row_col_chunk_num, values):
        """

        Args:
            key: (see mapper)
            values: Iterator of values (see mapper)

        Yields:
            A tuple in the form of (key, value)
            key: 
            value: 
        """
        row_chunk_num, col_chunk_num = row_col_chunk_num
        target_kernels = ['hik', 'linear']
        x_values = []
        y_values = []
        for x, y, z in values:
            if 'x' == x:
                x_values.append((y, z))
            elif 'y' == x:
                y_values.append((y, z))
            else:
                raise ValueError(x)
        y_values = sorted(y_values)
        col_num = y_values[0][0]
        y_matrix = np.vstack([x[1] for x in y_values])
        print(y_matrix.shape)
        for row_num, row_feature in x_values:
            row_feature = row_feature.reshape((1, row_feature.size))
            for kernel in target_kernels:
                yield (kernel, row_num, col_num), kernels.compute(kernel, row_feature, y_matrix).ravel()


if __name__ == '__main__':
    hadoopy.run(Mapper, Reducer)
