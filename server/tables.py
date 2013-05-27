import base64
import jobs
import bottle
import json
import time
import uuid
import re
import picarus_takeout
import functools
import msgpack
from driver import PicarusManager
from parameters import PARAM_SCHEMAS_SERVE
from model_factories import FACTORIES

# These need to be set before using this module
thrift_lock = None
thrift_new = None
VERSION = None
JOBS = None


def dod_to_lod_b64(dod):
    # Converts from dod[row][column] to list of {row, col0_ub64:val0_b64, ...}
    # dod: dict of dicts
    # lod: list of dicts
    outs = []
    for row, columns in sorted(dod.items(), key=lambda x: x[0]):
        out = {'row': base64.b64encode(row)}
        out.update({base64.b64encode(x): base64.b64encode(y) if isinstance(y, str) else base64.b64encode(json.dumps(y)) for x, y in columns.items()})
        outs.append(out)
    return outs

PARAM_SCHEMAS_B64 = dod_to_lod_b64(PARAM_SCHEMAS_SERVE)


def encode_row(row, columns):
    out = {base64.b64encode(k): base64.b64encode(v) for k, v in columns.items()}
    out['row'] = base64.b64encode(row)
    return out


def key_to_model(manager, *args, **kw):
    try:
        return manager.key_to_model(*args, **kw)
    except IndexError:
        bottle.abort(404)


def _takeout_model_link_from_key(manager, key):
    print('Manager key[%r]' % key)
    model_binary, columns = key_to_model(manager, key, 'link')
    model = msgpack.loads(model_binary)
    if not isinstance(model, dict):
        bottle.abort(400)
    return model


def _takeout_model_chain_from_key(manager, key):
    if key == 'data:image':
        return []
    columns = key_to_model(manager, key)
    if columns['input_type'] == 'raw_image':
        return [_takeout_model_link_from_key(manager, key)]
    return _takeout_model_chain_from_key(manager, columns['input']) + [_takeout_model_link_from_key(manager, key)]


def _takeout_input_model_link_from_key(manager, key):
    model_binary, columns = key_to_model(manager, key, 'link')
    model = msgpack.loads(model_binary)
    if not isinstance(model, dict):
        bottle.abort(400)
    return columns['input'], model


def _takeout_input_model_chain_from_key(manager, key):
    columns = key_to_model(manager, key)
    if columns['input_type'] == 'raw_image':
        return [_takeout_input_model_link_from_key(manager, key)]
    return _takeout_input_model_chain_from_key(manager, columns['input']) + [_takeout_input_model_link_from_key(manager, key)]


def _parse_params(params, schema):
    kw = {}
    schema_params = schema['params']
    prefix = 'param'

    def get_param(x, func=str, exception=False):
        try:
            return func(params[prefix + '-' + x])
        except (KeyError, ValueError):
            if exception:
                raise
            bottle.abort(400)
    for param_name, param in schema_params.items():
        if param['type'] == 'enum':
            param_value = get_param(param_name)
            if param_value not in param['values']:
                bottle.abort(400)
            kw[param_name] = param_value
        elif param['type'] == 'int':
            param_value = get_param(param_name, int)
            if not (param['min'] <= param_value < param['max']):
                bottle.abort(400)
            kw[param_name] = param_value
        elif param['type'] == 'float':
            param_value = get_param(param_name, float)
            if not (param['min'] <= param_value < param['max']):
                bottle.abort(400)
            kw[param_name] = param_value
        elif param['type'] == 'int_list':
            param_value = {}
            for x in range(param['max_size']):
                try:
                    try:
                        bin_value = get_param(param_name + ':' + str(x), int, True)
                    except ValueError:
                        bottle.abort(400)
                    if not (param['min'] <= bin_value < param['max']):
                        bottle.abort(400)
                    param_value[x] = bin_value
                except KeyError:
                    pass
            param_value = sorted(param_value.items())
            if not len(param_value) == param_value[-1][0] + 1:
                bottle.abort(400)
            param_value = [x[1] for x in param_value]
            kw[param_name] = param_value
        elif param['type'] == 'const':
            kw[param_name] = param['value']
        elif param['type'] == 'str':
            kw[param_name] = get_param(param_name)
        else:
            bottle.abort(400)
    return kw


def _get_input(params, key):
    # TODO: Verify that model keys exist
    return params['input-' + key]


def _create_model_from_params(manager, email, path, params):
    try:
        schema = PARAM_SCHEMAS_SERVE[path]
        model_params = _parse_params(params, schema)
        model_link = {'name': schema['name'], 'kw': model_params}
        input = _get_input(params, schema['input_type'])
        model_chain = _takeout_model_chain_from_key(manager, input) + [model_link]
        row = manager.input_model_param_to_key(input=input, model_link=model_link, model_chain=model_chain, input_type=schema['input_type'],
                                               output_type=schema['output_type'], email=email, name=manager.model_to_name(model_link))
        return {'row': base64.b64encode(row)}
    except ValueError:
        raise
        bottle.abort(500)


def _create_model_from_factory(email, db, path, create_model, params, start_stop_rows, table, job_row):
    schema = PARAM_SCHEMAS_SERVE[path]
    model_params = _parse_params(params, schema)
    inputs = {x: _get_input(params, x) for x in schema['input_types']}
    db.create_model_job(create_model, model_params, inputs, schema, start_stop_rows, table, email, job_row)
    return {'row': base64.b64encode(job_row), 'table': 'jobs'}


class BaseTableSmall(object):
    """Base class for tables that easily fit in memory"""

    def __init__(self):
        super(BaseTableSmall, self).__init__()

    def get_table(self, columns):
        bottle.response.headers["Content-type"] = "application/json"
        columns = set(columns)
        full_table = self._get_table()
        if columns:
            columns.add('row')
            return json.dumps([{y: x[y] for y in columns.intersection(x)} for x in full_table])
        else:
            return json.dumps(full_table)

    def _get_row(self, row, unused_columns):
        # TODO: Remove unused_columns
        row_ub64 = base64.b64encode(row)
        for x in self._get_table():
            if x['row'] == row_ub64:
                x = dict(x)  # Ensures we aren't deleting anything
                del x['row']
                return x
        bottle.abort(404)

    def get_row(self, row, columns):
        columns_ub64 = set(map(base64.b64encode, columns))
        column_values_b64 = self._get_row(row, columns)
        if columns_ub64:
            columns_ub64 = set(columns_ub64).intersection(column_values_b64)
            return {x: column_values_b64[x] for x in columns_ub64}
        else:
            return column_values_b64


class ParametersTable(BaseTableSmall):

    def __init__(self):
        super(ParametersTable, self).__init__()
        self._params = dod_to_lod_b64(PARAM_SCHEMAS_SERVE)

    def _get_table(self):
        return self._params


class UsageTable(BaseTableSmall):

    def __init__(self, _auth_user):
        super(UsageTable, self).__init__()
        self._table = dod_to_lod_b64(_auth_user.usage())

    def _get_table(self):
        return self._table


class RedisUsersTable(BaseTableSmall):

    def __init__(self, _auth_user, table, set_column, del_column):
        super(RedisUsersTable, self).__init__()
        self._auth_user = _auth_user
        self._table = table
        self._set_column = set_column
        self._del_column = del_column

    def _get_table(self):
        return dod_to_lod_b64(self._table)

    def patch_row(self, row, params, files):
        if files:
            bottle.abort(403)  # Files not allowed
        for x, y in params.items():
            new_column = base64.b64decode(x)
            new_value = base64.b64decode(y)
            self._row_column_value_validator(row, new_column, new_value)
            try:
                self._set_column[row](new_column, new_value)
            except KeyError:
                bottle.abort(403)
        return {}

    def delete_column(self, row, column):
        try:
            self._del_column[row](column)
        except KeyError:
            bottle.abort(403)
        return {}


class PrefixesTable(RedisUsersTable):

    def __init__(self, _auth_user):
        table = {}
        set_column = {}
        del_column = {}
        for x in _auth_user._tables:
            table[x] = _auth_user.prefixes(x)
            set_column[x] = functools.partial(_auth_user.add_prefix, x)
            del_column[x] = functools.partial(_auth_user.remove_prefix, x)
        super(PrefixesTable, self).__init__(_auth_user, table, set_column, del_column)

    def _row_column_value_validator(self, row, new_column, new_value):
        if new_value not in ('r', 'rw'):
            bottle.abort(403)
        for cur_prefix, cur_permissions in self._table[row].items():
            if new_column.startswith(cur_prefix) and cur_permissions.startswith(new_value):
                return
        bottle.abort(403)  # No valid prefix lets the user do this


class ProjectsTable(RedisUsersTable):
    def __init__(self, _auth_user):
        table = {}
        set_column = {}
        del_column = {}
        for x in _auth_user._tables:
            table[x] = _auth_user.projects(x)
            set_column[x] = functools.partial(_auth_user.add_project, x)
            del_column[x] = functools.partial(_auth_user.remove_project, x)
        super(ProjectsTable, self).__init__(_auth_user, table, set_column, del_column)

    def _row_column_value_validator(self, row, new_column, new_value):
        # TODO: Add checks
        return


class JobsTable(BaseTableSmall):

    def __init__(self, _auth_user):
        super(JobsTable, self).__init__()
        self.owner = _auth_user.email
        self._auth_user = _auth_user

    def _get_table(self):
        try:
            cur_table = JOBS.get_tasks(self.owner)
        except jobs.UnauthorizedException:
            bottle.abort(401)
        return dod_to_lod_b64(cur_table)

    def delete_row(self, row):
        JOBS.delete_task(row, self.owner)
        return {}

    def post_row(self, row, params, files):
        if files:
            bottle.abort(400)
        params = {k: base64.b64decode(v) for k, v in params.items()}
        action = params['action']
        manager = JOBS.get_annotation_manager_check(row, self.owner)
        if action == 'io/annotation/sync':
            manager.sync()
            return {}
        elif action == 'io/annotation/priority':
            data_row = params['row']
            priority = int(params['priority'])
            manager.row_increment_priority(data_row, priority)
            return {}
        else:
            bottle.abort(400)

    def post_table(self, params, files):
        if files:
            bottle.abort(400)
        params = {base64.b64decode(k): base64.b64decode(v) for k, v in params.items()}
        path = params['path']
        start_stop_rows = parse_slices()
        if path in ('annotation/images/class',):
            data_table = get_table(self._auth_user, path.split('/')[1])
            for start_row, stop_row in start_stop_rows:
                data_table._slice_validate(start_row, stop_row, 'r')
            # We never need to decode these, they just need to be
            # random strings that can be in a url
            secret = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2]
            p = {}
            image_column = params['imageColumn']
            ub64 = base64.urlsafe_b64encode
            if path == 'annotation/images/class':
                class_column = params['classColumn']
                assert class_column.startswith('meta:')
                suffix = '/'.join(ub64(x) + '/' + ub64(y) for x, y in start_stop_rows)
                data = 'hbase://localhost:9090/images/%s?class=%s&image=%s' % (suffix,
                                                                               ub64(class_column), ub64(image_column))
                p['type'] = 'image_class'
                try:
                    p['class_descriptions'] = params['classDescriptions']
                except KeyError:
                    pass
                try:
                    p['class_thumbnails'] = params['classThumbnails']
                except KeyError:
                    pass
            else:
                bottle.abort(400)
            if 'instructions' in params:
                p['instructions'] = params['instructions']
            p['num_tasks'] = int(params['numTasks'])
            assert 0 < p['num_tasks']
            assert params['mode'] in ('standalone', 'amt')
            p['mode'] = params['mode']
            task = JOBS.add_task('annotation', self.owner, params=p, secret_params={'secret': secret, 'data': data})
            JOBS.get_annotation_manager(task, sync=True)
            return {'row': base64.b64encode(task)}
        else:
            bottle.abort(400)


class AnnotationDataTable(BaseTableSmall):

    def __init__(self, _auth_user, table, task):
        super(AnnotationDataTable, self).__init__()
        self.owner = _auth_user.email
        self.table = table
        self.task = task

    def _get_table(self):
        try:
            secret = JOBS.get_task_secret(self.task, self.owner)['secret']
        except jobs.UnauthorizedException:
            bottle.abort(401)
        if self.table == 'results':
            table = JOBS.get_annotation_manager(self.task).admin_results(secret)
        elif self.table == 'users':
            table = JOBS.get_annotation_manager(self.task).admin_users(secret)
        else:
            bottle.abort(500)
        return dod_to_lod_b64(table)


class HBaseTable(object):

    def __init__(self, _auth_user, table):
        self.owner = _auth_user.email
        self.table = table

    def patch_row(self, row, params, files):
        with thrift_lock() as thrift:
            self._row_validate(row, 'rw', thrift)
            mutations = {}
            for x, y in files.items():
                cur_column = base64.b64decode(x)
                self._column_write_validate(cur_column)
                v = y.file.read()
                thrift.mutate_row(self.table, row, {cur_column: v})
            for x, y in params.items():
                cur_column = base64.b64decode(x)
                self._column_write_validate(cur_column)
                mutations[cur_column] = base64.b64decode(y)
            if mutations:
                thrift.mutate_row(self.table, row, mutations)
        return {}

    def delete_row(self, row):
        with thrift_lock() as thrift:
            self._row_validate(row, 'rw', thrift)
            thrift.delete_row(self.table, row)
            return {}

    def delete_column(self, row, column):
        with thrift_lock() as thrift:
            self._row_validate(row, 'rw', thrift)
            thrift.delete_column(self.table, row, column)
            return {}

    def get_row(self, row, columns):
        with thrift_lock() as thrift:
            self._row_validate(row, 'r', thrift)
            result = thrift.get_row(self.table, row, columns)
        return {base64.b64encode(x): base64.b64encode(y)
                for x, y in result.items()}


class DataHBaseTable(HBaseTable):

    def __init__(self, _auth_user, table):
        super(DataHBaseTable, self).__init__(_auth_user, table)
        self.prefixes = _auth_user.prefixes(table)
        self.upload_row_prefix = _auth_user.upload_row_prefix

    def _slice_validate(self, start_row, stop_row, permissions):
        prefixes = self.prefixes
        permissions = set(permissions)
        prefixes = [x for x, y in prefixes.items() if set(y).issuperset(permissions)]
        for prefix in prefixes:
            if prefix == '':
                return
            # NOTE: Prevents rollover, minor limitation on prefix is that it must not end in \xff
            assert prefix[-1] != '\xff'
            prefix_start_row = prefix
            prefix_stop_row = prefix[:-1] + chr(ord(prefix[-1]) + 1)
            if start_row and prefix_start_row <= start_row < prefix_stop_row and stop_row and prefix_start_row <= stop_row <= prefix_stop_row:
                return
        bottle.abort(401)

    def _row_validate(self, row, permissions, thrift=None):
        prefixes = self.prefixes
        permissions = set(permissions)
        prefixes = [x for x, y in prefixes.items() if set(y).issuperset(permissions)]
        for prefix in prefixes:
            if prefix == '':
                return
            # NOTE: Prevents rollover, minor limitation on prefix is that it must not end in \xff
            assert prefix[-1] != '\xff'
            prefix_start_row = prefix
            prefix_stop_row = prefix[:-1] + chr(ord(prefix[-1]) + 1)
            if row and prefix_start_row <= row < prefix_stop_row:
                return
        bottle.abort(401)

    def post_table(self, params, files):
        row = self.upload_row_prefix + '%.10d%s' % (2147483648 - int(time.time()), uuid.uuid4().bytes)
        self.patch_row(row, params, files)
        return {'row': base64.b64encode(row)}

    def _byte_count_rows(self, lod_rows, row_bytes=0, column_bytes=0):
        byte_count = 0
        for lod_row in lod_rows:
            byte_count += sum(len(x) + len(y) for x, y in lod_row.items())
            byte_count += row_bytes + column_bytes * len(lod_row)
        return byte_count

    def get_slice(self, start_row, stop_row, columns, params, files):
        self._slice_validate(start_row, stop_row, 'r')
        max_rows = min(10000, int(params.get('maxRows', 1)))
        print('MaxRows[%d]' % max_rows)
        max_bytes = min(5242880, int(params.get('maxBytes', 5242880)))
        exclude_start = bool(int(params.get('excludeStart', 0)))
        out = []
        per_call = 1
        max_byte_count = 0
        with thrift_lock() as thrift:
            scanner = thrift.scanner(self.table, per_call=per_call, columns=columns,
                                     start_row=start_row, stop_row=stop_row)
            cur_row = start_row
            byte_count = 0
            for row_num, (cur_row, cur_columns) in enumerate(scanner, 1):
                if exclude_start and row_num == 1:
                    continue
                out.append(encode_row(cur_row, cur_columns))
                cur_byte_count = self._byte_count_rows(out[-1:])
                byte_count += cur_byte_count
                # Compute the number of rows we should try to get by using the max sized row
                # that we have seen as an upper bound.
                max_byte_count = max(1, max(max_byte_count, cur_byte_count))
                per_call = max(1, min((max_bytes - byte_count) / max_byte_count, max_rows - len(out)))
                if len(out) >= max_rows or byte_count >= max_bytes:
                    break
        bottle.response.headers["Content-type"] = "application/json"
        return json.dumps(out)

    def patch_slice(self, start_row, stop_row, params, files):
        self._slice_validate(start_row, stop_row, 'w')
        # NOTE: Only parameters allowed, no "files" due to memory restrictions
        mutations = {}
        for x, y in params.items():
            mutations[base64.b64decode(x)] = base64.b64decode(y)
        if mutations:
            with thrift_lock() as thrift:
                for row, _ in thrift.scanner(self.table, start_row=start_row, stop_row=stop_row, keys_only=True):
                    thrift.mutate_row(self.table, row, mutations)
        return {}

    def delete_slice(self, start_row, stop_row):
        self._slice_validate(start_row, stop_row, 'w')
        # NOTE: This only fetches rows that have a column in data:image (it is a significant optimization)
        # NOTE: Only parameters allowed, no "files" due to memory restrictions
        with thrift_lock() as thrift:
            for row, _ in thrift.scanner(self.table, start_row=start_row, stop_row=stop_row, keys_only=True):
                thrift.delete_row(self.table, row)
        return {}


class ImagesHBaseTable(DataHBaseTable):

    def __init__(self, _auth_user):
        super(ImagesHBaseTable, self).__init__(_auth_user, 'images')

    def _column_write_validate(self, column):
        if column == 'data:image':
            return
        if column.startswith('meta:'):
            return
        bottle.abort(403)

    def post_row(self, row, params, files):
        if files:
            bottle.abort(400)
        params = {k: base64.b64decode(v) for k, v in params.items()}
        action = params['action']
        with thrift_lock() as thrift:
            manager = PicarusManager(db=thrift)
            print(params)
            model_key = params['model']
            print('ModelKey[%r]' % model_key)
            # TODO: Allow io/ so that we can write back to the image too
            if action == 'i/link':
                self._row_validate(row, 'r')
                # TODO: Get this directly from model
                chain_input, model_link = _takeout_input_model_link_from_key(manager, model_key)
                binary_input = thrift.get_column(self.table, row, chain_input)
                model = picarus_takeout.ModelChain(msgpack.dumps([model_link]))
                bottle.response.headers["Content-type"] = "application/json"
                return json.dumps({base64.b64encode(params['model']): base64.b64encode(model.process_binary(binary_input))})
            elif action == 'i/chain':
                self._row_validate(row, 'r')
                # TODO: Get this directly from model
                chain_inputs, model_chain = zip(*_takeout_input_model_chain_from_key(manager, model_key))
                binary_input = thrift.get_column(self.table, row, chain_inputs[0])
                model_chain = list(model_chain)
                model = picarus_takeout.ModelChain(msgpack.dumps(model_chain))
                bottle.response.headers["Content-type"] = "application/json"
                v = base64.b64encode(model.process_binary(binary_input))
                return json.dumps({base64.b64encode(params['model']): v})
            else:
                bottle.abort(400)

    def post_slice(self, start_row, stop_row, params, files):
        if files:
            bottle.abort(400)
        params = {k: base64.b64decode(v) for k, v in params.items()}
        action = params['action']
        with thrift_new() as thrift:
            manager = PicarusManager(db=thrift)
            if action == 'io/thumbnail':
                self._slice_validate(start_row, stop_row, 'rw')
                # Makes 150x150 thumbnails from the data:image column
                model = [{'name': 'picarus.ImagePreprocessor', 'kw': {'method': 'force_square', 'size': 150, 'compression': 'jpg'}}]
                job_row = JOBS.add_task('process', self.owner, {'startRow': base64.b64encode(start_row),
                                                                'stopRow': base64.b64encode(stop_row),
                                                                'table': self.table,
                                                                'action': action}, {})
                thrift.takeout_chain_job('images', model, 'data:image', 'thum:image_150sq', start_row=start_row, stop_row=stop_row, job_row=job_row)
                return {base64.b64encode(k): base64.b64encode(v) for k, v in {'row': job_row, 'table': 'jobs'}.items()}
            elif action == 'io/exif':
                self._slice_validate(start_row, stop_row, 'rw')
                job_row = JOBS.add_task('process', self.owner, {'startRow': base64.b64encode(start_row),
                                                                'stopRow': base64.b64encode(stop_row),
                                                                'table': self.table,
                                                                'action': action}, {})
                thrift.exif_job(start_row=start_row, stop_row=stop_row, job_row=job_row)
                return {base64.b64encode(k): base64.b64encode(v) for k, v in {'row': job_row, 'table': 'jobs'}.items()}
            elif action == 'io/link':
                self._slice_validate(start_row, stop_row, 'rw')
                model_key = params['model']
                chain_input, model_link = _takeout_input_model_link_from_key(manager, model_key)
                job_row = JOBS.add_task('process', self.owner, {'startRow': base64.b64encode(start_row),
                                                                'stopRow': base64.b64encode(stop_row),
                                                                'table': self.table,
                                                                'action': action}, {})
                thrift.takeout_chain_job('images', [model_link], chain_input, model_key, start_row=start_row, stop_row=stop_row, job_row=job_row)
                return {base64.b64encode(k): base64.b64encode(v) for k, v in {'row': job_row, 'table': 'jobs'}.items()}
            elif action == 'io/chain':
                self._slice_validate(start_row, stop_row, 'rw')
                model_key = params['model']
                chain_inputs, model_chain = zip(*_takeout_input_model_chain_from_key(manager, model_key))
                job_row = JOBS.add_task('process', self.owner, {'startRow': base64.b64encode(start_row),
                                                                'stopRow': base64.b64encode(stop_row),
                                                                'table': self.table,
                                                                'action': action}, {})
                thrift.takeout_chain_job('images', list(model_chain), chain_inputs[0], model_key, start_row=start_row, stop_row=stop_row, job_row=job_row)
                return {base64.b64encode(k): base64.b64encode(v) for k, v in {'row': job_row, 'table': 'jobs'}.items()}
            elif action == 'o/crawl/flickr':
                self._slice_validate(start_row, stop_row, 'w')

            else:
                bottle.abort(400)


def parse_slices():
    k = base64.b64encode('slices')
    if bottle.request.content_type == "application/json":
        out = bottle.request.json[k]
    else:
        if not bottle.request.params[k]:
            out = []
        else:
            out = base64.b64decode(bottle.request.params[k]).split(';')
    return [map(base64.b64decode, x.split(',')) for x in out]


class ModelsHBaseTable(HBaseTable):

    def __init__(self, _auth_user):
        super(ModelsHBaseTable, self).__init__(_auth_user, 'models')
        self._auth_user = _auth_user

    def _column_write_validate(self, column):
        if column in ('meta:notes', 'meta:tags'):
            return
        if column.startswith('user:'):
            return
        bottle.abort(403)

    def _row_validate(self, row, permissions, thrift):
        try:
            results = thrift.get_column(self.table, row, 'user:' + self.owner)
        except bottle.HTTPError:
            bottle.abort(403)
        if not results.startswith(permissions):
            bottle.abort(403)

    def get_table(self, columns):
        user_column = 'user:' + self.owner
        output_user = user_column in columns or not columns or 'user:' in columns
        outs = []
        if columns:
            columns = columns + [user_column]
        else:
            columns = None
        with thrift_lock() as thrift:
            for row, cols in thrift.scanner(self.table, columns=columns, column_filter=(user_column, 'startswith', 'r')):
                self._row_validate(row, 'r', thrift)
                if not output_user:
                    del cols[user_column]
                outs.append(encode_row(row, cols))
        bottle.response.headers["Content-type"] = "application/json"
        return json.dumps(outs)

    def post_table(self, params, files):
        if files:
            bottle.abort(400)
        params = {base64.b64decode(k): base64.b64decode(v) for k, v in params.items()}
        path = params['path']
        with thrift_lock() as thrift:
            manager = PicarusManager(db=thrift)
            if path.startswith('model/'):
                return _create_model_from_params(manager, self.owner, path, params)
            elif path.startswith('factory/'):
                table = params['table']
                start_stop_rows = parse_slices()
                data_table = get_table(self._auth_user, table)
                for start_row, stop_row in start_stop_rows:
                    data_table._slice_validate(start_row, stop_row, 'r')
                try:
                    slices = [base64.b64encode(start_row) + ',' + base64.b64encode(stop_row) for start_row, stop_row in start_stop_rows]
                    job_row = JOBS.add_task('model', self.owner, {'slices': ';'.join(slices),
                                                                  'table': self.table,
                                                                  'path': path}, {})
                    return _create_model_from_factory(manager, self.owner, path, FACTORIES[path], params, start_stop_rows, data_table.table, job_row)
                except KeyError:
                    bottle.abort(400)


def get_table(_auth_user, table):
    annotation_re = re.search('annotation\-(results|users)\-([a-zA-Z0-9_\-]+)', table)
    if annotation_re:
        return AnnotationDataTable(_auth_user, *annotation_re.groups())
    elif table == 'jobs':
        return JobsTable(_auth_user)
    elif table == 'images':
        return ImagesHBaseTable(_auth_user)
    elif table == 'models':
        return ModelsHBaseTable(_auth_user)
    elif table == 'usage':
        return UsageTable(_auth_user)
    elif table == 'prefixes':
        return PrefixesTable(_auth_user)
    elif table == 'projects':
        return ProjectsTable(_auth_user)
    elif table == 'parameters':
        return ParametersTable()
    else:
        bottle.abort(404)
