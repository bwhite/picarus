import hadoopy_hbase
import logging
import time
import tempfile
import zlib
import os
import random
import cPickle as pickle
import base64
import hashlib
import subprocess
import msgpack

logging.basicConfig(level=logging.DEBUG)

output_hdfs = 'picarus_temp/%f/' % time.time()


def get_version(module_name):
    prev_dir = os.path.abspath('.')
    try:
        module_dir = __import__(module_name).__path__[0]
    except ImportError:
        raise ValueError('Module [%s] could not be imported!' % module_name)
    except AttributeError:
        raise ValueError('Module [%s] directory could not be found!' % module_name)
    try:
        os.chdir(module_dir)
        return subprocess.Popen('git log -1 --pretty=format:%H'.split(), stdout=subprocess.PIPE).communicate()[0]
    finally:
        os.chdir(prev_dir)


def _tempfile(data, suffix=''):
    fp = tempfile.NamedTemporaryFile(suffix=suffix)
    fp.write(data)
    fp.flush()
    return fp


def model_tofile(model):
    if isinstance(model, dict) or isinstance(model, list):
        return _tempfile(zlib.compress(msgpack.dumps(model)), suffix='.msgpack.gz')
    else:
        return _tempfile(zlib.compress(pickle.dumps(model)), suffix='.pkl.gz')


class PicarusManager(object):

    def __init__(self, thrift=None):
        self.image_orig_column = 'data:image'
        self.image_column = 'data:image_320'
        self.images_table = 'images'
        self.models_table = 'models'
        self.hb = thrift if thrift is not None else hadoopy_hbase.connect()
        self.max_cell_size = 1024 * 1024  # 1MB
        # Feature Hasher settings
        self.hb = hadoopy_hbase.connect()
        # Feature Classifier settings
        self.feature_classifier_row = self.images_table
        # Index Settings
        self.class_column = 'meta:class_2'
        self.indoor_class_column = 'meta:class_0'
        self.num_mappers = 6

        # Model columns
        self.model_link_chunks_column = 'meta:model_link_chunks'
        self.model_chain_chunks_column = 'meta:model_chain_chunks'
        self.model_link_column = 'data:model_link'
        self.model_chain_column = 'data:model_chain'
        self.input_column = 'meta:input'
        self.model_link_sha1_column = 'meta:model_link_sha1'
        self.model_chain_sha1_column = 'meta:model_chain_sha1'
        self.model_link_size_column = 'meta:model_link_size'
        self.model_chain_size_column = 'meta:model_chain_size'
        self.input_type_column = 'meta:input_type'
        self.output_type_column = 'meta:output_type'
        self.model_link_type_column = 'meta:model_link_type'
        self.model_chain_type_column = 'meta:model_chain_type'
        self.creation_time_column = 'meta:creation_time'
        self.notes_column = 'meta:notes'
        self.name_column = 'meta:name'
        self.tags_column = 'meta:tags'
        self.factory_info_column = 'meta:factory_info'

    def output_type_to_prefix(self, output_type):
        # Only using data:, meta:, thum: feat:, pred:, hash: the others are deprecated
        return {'feature': 'feat:', 'feature2d_binary': 'feat:', 'binary_prediction': 'pred:', 'image_detections': 'pred:',
                'processed_image': 'data:', 'binary_class_confidence': 'pred:', 'mask_feature' : 'feat:', 'distance_image_rows': 'pred:',
                'multi_class_distance': 'pred:', 'hash': 'hash:', 'multi_feature': 'feat:'}[output_type]

    def input_model_param_to_key(self, input, model_link, model_chain, input_type, output_type, email, name, notes='', tags='', factory_info=None):
        assert isinstance(input, str)
        check_model = lambda x: isinstance(x, dict) and set(['name', 'kw']) == set(x.keys())
        dumps = lambda x: msgpack.dumps(x)
        prefix = self.output_type_to_prefix(output_type)
        model_key = prefix + os.urandom(16)
        cols = []

        def save_model(model_str, model_column, model_chunks_column, model_sha1_column, model_size_column):
            cols.append(hadoopy_hbase.Mutation(column=model_sha1_column, value=hashlib.sha1(model_str).hexdigest()))
            cols.append(hadoopy_hbase.Mutation(column=model_size_column, value=str(len(model_str))))
            chunk_count = 0
            while model_str:
                self.hb.mutateRow(self.models_table, model_key, [hadoopy_hbase.Mutation(column=model_column + '-%d' % chunk_count, value=model_str[:self.max_cell_size])])
                model_str = model_str[self.max_cell_size:]
                chunk_count += 1
            cols.append(hadoopy_hbase.Mutation(column=model_chunks_column, value=str(chunk_count)))
        try:
            # Save the models ASAP chunk by chunk to reduce memory usage
            if check_model(model_link) and all(map(check_model, model_chain)):
                model_chain_type = model_link_type = 'msgpack'
                save_model(dumps(model_link), self.model_link_column, self.model_link_chunks_column, self.model_link_sha1_column, self.model_link_size_column)
                save_model(dumps(model_chain), self.model_chain_column, self.model_chain_chunks_column, self.model_chain_sha1_column, self.model_chain_size_column)
            else:
                raise ValueError('Model must be a dict!')
            cols += [hadoopy_hbase.Mutation(column=self.input_column, value=input),
                     hadoopy_hbase.Mutation(column=self.input_type_column, value=input_type),
                     hadoopy_hbase.Mutation(column=self.output_type_column, value=output_type),
                     hadoopy_hbase.Mutation(column=self.model_link_type_column, value=model_link_type),
                     hadoopy_hbase.Mutation(column=self.model_chain_type_column, value=model_chain_type),
                     hadoopy_hbase.Mutation(column=self.creation_time_column, value=str(time.time())),
                     hadoopy_hbase.Mutation(column=self.notes_column, value=notes),
                     hadoopy_hbase.Mutation(column=self.name_column, value=name),
                     hadoopy_hbase.Mutation(column=self.tags_column, value=tags),
                     hadoopy_hbase.Mutation(column='user:' + email, value='rw')]
            if factory_info is not None:
                cols.append(hadoopy_hbase.Mutation(column=self.factory_info_column, value=factory_info))
            self.hb.mutateRow(self.models_table, model_key, cols)
            return model_key
        except:
            print('Deleting model [%r] due to exception' % model_key)
            self.hb.deleteAllRow(self.models_table, model_key)
            raise

    def key_to_model(self, key, model_type=None):
        columns = {x[5:]: y.value for x, y in self.hb.getRowWithColumns(self.models_table, key, ['meta:'])[0].columns.items()}
        if model_type is None:
            return columns
        if model_type == 'link':
            model_chunks_column = self.model_link_chunks_column[5:]
            model_column = self.model_link_column
        elif model_type == 'chain':
            model_chunks_column = self.model_chain_chunks_column[5:]
            model_column = self.model_chain_column
        else:
            raise ValueError
        model_chunks = int(columns[model_chunks_column])
        model_chunk_columns = [model_column + '-%d' % x for x in range(model_chunks)]
        chunks = [(int(x.split('-')[1]), y.value) for x, y in self.hb.getRowWithColumns(self.models_table, key, model_chunk_columns)[0].columns.items()]
        chunks.sort()
        return ''.join([x[1] for x in chunks]), columns

    def image_thumbnail(self, **kw):
        # Makes 150x150 thumbnails from the data:image column
        model = [{'name': 'picarus.ImagePreprocessor', 'kw': {'method': 'force_square', 'size': 150, 'compression': 'jpg'}}]
        self.takeout_chain_job(model, 'data:image', 'thum:image_150sq', **kw)

    def image_exif(self, **kw):
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode('meta:exif')}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/image_exif.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, columns=['data:image'], single_value=True,
                             cmdenvs=cmdenvs, check_script=False, make_executable=False, **kw)

    def takeout_chain_job(self, model, input_column, output_column, **kw):
        model_fp = model_tofile(model)
        cmdenvs = {'HBASE_TABLE': self.images_table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(output_column),
                   'MODEL_FN': os.path.basename(model_fp.name)}
        hadoopy_hbase.launch(self.images_table, output_hdfs + str(random.random()), 'hadoop/takeout_chain_job.py', libjars=['hadoopy_hbase.jar'],
                             num_mappers=self.num_mappers, files=[model_fp.name], columns=[input_column], single_value=True,
                             jobconfs={'mapred.task.timeout': '6000000'}, cmdenvs=cmdenvs, dummy_fp=model_fp, check_script=False, make_executable=False, **kw)

    def model_to_name(self, model):
        args = list(model.get('args', []))
        for x, y in sorted(model.get('kw', {}).items()):
            if isinstance(y, (dict, list, tuple, str)):
                if len(y) > 20:
                    y = '<...>'
                else:
                    y = repr(y)
            else:
                y = repr(y)
            if len(y) > 20:
                y = 'sha1:' + repr(hashlib.sha1(y).hexdigest()[:4])
            args.append('%s=%s' % (x, y))
        return model['name'] + '(%s)' % ', '.join(args)
