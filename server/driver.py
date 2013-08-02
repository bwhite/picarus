import logging
import time
import os
import hashlib
import msgpack

logging.basicConfig(level=logging.DEBUG)


class PicarusManager(object):

    def __init__(self, db):
        self.image_orig_column = 'data:image'
        self.image_column = 'data:image_320'
        self.images_table = 'images'
        self.models_table = 'models'
        self.db = db
        self.max_cell_size = 1024 * 1024  # 1MB
        # Feature Hasher settings
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
        cols = {}

        def save_model(model_str, model_column, model_chunks_column, model_sha1_column, model_size_column):
            cols[model_sha1_column] = hashlib.sha1(model_str).hexdigest()
            cols[model_size_column] = str(len(model_str))
            chunk_count = 0
            while model_str:
                self.db.mutate_row(self.models_table, model_key, {model_column + '-%d' % chunk_count: model_str[:self.max_cell_size]})
                model_str = model_str[self.max_cell_size:]
                chunk_count += 1
            cols[model_chunks_column] = str(chunk_count)
        try:
            # Save the models ASAP chunk by chunk to reduce memory usage
            if check_model(model_link) and all(map(check_model, model_chain)):
                model_chain_type = model_link_type = 'msgpack'
                save_model(dumps(model_link), self.model_link_column, self.model_link_chunks_column, self.model_link_sha1_column, self.model_link_size_column)
                save_model(dumps(model_chain), self.model_chain_column, self.model_chain_chunks_column, self.model_chain_sha1_column, self.model_chain_size_column)
            else:
                raise ValueError('Model must be a dict!')
            cols.update({self.input_column: input,
                         self.input_type_column: input_type,
                         self.output_type_column: output_type,
                         self.model_link_type_column: model_link_type,
                         self.model_chain_type_column: model_chain_type,
                         self.creation_time_column: str(time.time()),
                         self.notes_column: notes,
                         self.name_column: name,
                         self.tags_column: tags,
                         'user:' + email: 'rw'})
            if factory_info is not None:
                cols[self.factory_info_column] = factory_info
            self.db.mutate_row(self.models_table, model_key, cols)
            return model_key
        except:
            print('Deleting model [%r] due to exception' % model_key)
            self.db.delete_row(self.models_table, model_key)
            raise

    def key_to_model(self, key, model_type=None):
        columns = dict((x[5:], y) for x, y in self.db.get_row(self.models_table, key, ['meta:']).items())
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
        # Get the chunks one at a time to relieve memory pressure
        chunks = []
        for x in range(model_chunks):
            model_column_cur = model_column + '-%d' % x
            model_val = self.db.get_row(self.models_table, key, [model_column_cur])[model_column_cur]
            chunks.append((x, model_val))
        chunks.sort()
        return ''.join([x[1] for x in chunks]), columns

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
