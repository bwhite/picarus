import random
import time
import zlib
import tempfile
import msgpack
import pickle
import redis
from PIL.ExifTags import TAGS
from PIL import Image
import cStringIO as StringIO
import json
import picarus_takeout
import bottle
import base64
import hadoopy_hbase
import os
import re
import gipc


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


def hadoop_wait_till_started(launch_out):
    process = launch_out['process']
    stdout = process.stderr
    while process.poll() is None:
        if stdout.readline().find('Tracking URL:') != -1:
            break
    if process.poll() > 0:
        raise RuntimeError('Hadoop task could not start')


def job_runner(*args, **kw):
    with gipc.pipe() as (reader, writer):
        p = gipc.start_process(target=job_worker, args=args, kwargs=kw)
        reader.get()
        p.join()


def job_worker(db, method, method_args):
    getattr(db, method)(*method_args)


class BaseDB(object):

    def __init__(self, jobs, spawn):
        if hasattr(self, 'args'):
            self.args += [jobs, None]
        else:
            self.args = [jobs, None]
        self._jobs = jobs
        self._spawn = spawn
        super(BaseDB, self).__init__()

    def __reduce__(self):
        return (BaseDB, self.args)

    def _job(self, table, start_row, stop_row, input_column, output_column, func, job_row):
        good_rows = 0
        total_rows = 0
        for row, columns in self.scanner(table, start_row, stop_row, columns=[input_column]):
            total_rows += 1
            try:
                input_data = columns[input_column]
            except KeyError:
                continue
            try:
                output_data = func(input_data)
            except:
                # TODO: We need some way of reporting exceptions back
                continue
            if output_data is None:
                continue
            self.mutate_row(table, row, {output_column: output_data})
            good_rows += 1
            self._jobs.update_job(job_row, {'goodRows': good_rows, 'badRows': total_rows - good_rows, 'status': 'running'})
        self._jobs.update_job(job_row, {'goodRows': good_rows, 'badRows': total_rows - good_rows, 'status': 'completed'})

    def exif_job(self, start_row, stop_row, job_row):

        def func(input_data):
            image = Image.open(StringIO.StringIO(input_data))
            if not hasattr(image, '_getexif'):
                return json.dumps({})
            else:
                image_tags = image._getexif()
                if image_tags is None:
                    return json.dumps({})
                else:
                    return json.dumps({name: base64.b64encode(image_tags[id]) if isinstance(image_tags[id], str) else image_tags[id]
                                       for id, name in TAGS.items()
                                       if id in image_tags})
        self._job('images', start_row, stop_row, 'data:image', 'meta:exif', func, job_row)

    def takeout_chain_job(self, table, model, input_column, output_column, start_row, stop_row, job_row):
        model = picarus_takeout.ModelChain(msgpack.dumps(model))

        def func(input_data):
            return model.process_binary(input_data)
        self._job(table, start_row, stop_row, input_column, output_column, func, job_row)


class RedisDB(BaseDB):

    def __init__(self, server, port, db, *args, **kw):
        if hasattr(self, 'args'):
            self.args += [server, port, db]
        else:
            self.args = [server, port, db]
        self.__redis = redis.StrictRedis(host=server, port=port, db=db)
        # redis[table:row] -> data[table][row]
        super(RedisDB, self).__init__(*args, **kw)

    def __reduce__(self):
        return (RedisDB, self.args)

    def _get_columns(self, table, row, columns, keys_only=False):
        table_row = table + ':' + row
        keys = self.__redis.hkeys(table_row)
        cfs = set()
        cols = set()
        for c in columns:
            cur_cf, cur_col = c.split(':', 1)
            if cur_col:
                cols.add(c)
            else:
                cfs.add(cur_cf)
        out = {}
        for k in keys:
            if k in cols or k.split(':', 1)[0] in cfs:
                if keys_only:
                    out[k] = ''
                else:
                    d = self.__redis.hget(table_row, k)
                    if d is not None:
                        out[k] = d
        return out

    def mutate_row(self, table, row, mutations):
        self.__redis.hmset(table + ':' + row, mutations)

    def delete_row(self, table, row):
        self.__redis.delete(table + ':' + row)

    def delete_column(self, table, row, column):
        self.__redis.hdel(table + ':' + row, column)

    def get_row(self, table, row, columns=None, check=True, keys_only=False):
        if columns:
            result = self._get_columns(table, row, columns, keys_only=keys_only)
        else:
            if keys_only:
                result = {x: '' for x in self.__redis.hkeys(table + ':' + row)}
            else:
                result = self.__redis.hgetall(table + ':' + row)
        if check and not result:
            bottle.abort(404)
        return result

    def get_column(self, table, row, column):
        out = self.__redis.hget(table + ':' + row, column)
        if out is None:
            bottle.abort(404)
        return out

    def scanner(self, table, start_row=None, stop_row=None, columns=None, keys_only=False, per_call=1, column_filter=None):
        keep_row = lambda x: True
        if column_filter:
            filter_column = column_filter[0]
            if column_filter[1] == '=':
                keep_row = lambda x: filter_column in x and x[filter_column] == column_filter[2]
            elif column_filter[1] == '!=':
                keep_row = lambda x: filter_column in x and x[filter_column] != column_filter[2]
            elif column_filter[1] == 'startswith':
                keep_row = lambda x: filter_column in x and x[filter_column].startswith(column_filter[2])
            else:
                bottle.abort(400)  # Bad filter
        if start_row is not None and stop_row is not None:
            prefix = []
            for x, y in zip(start_row, stop_row):
                if x == y:
                    prefix.append(x)
                else:
                    break
            prefix = ''.join(prefix)
        else:
            prefix = ''
        table_start_row = table + ':' if start_row is None else '%s:%s' % (table, start_row)
        table_stop_row = None if stop_row is None else '%s:%s' % (table, stop_row)
        for row in self.__redis.keys('%s:%s*' % (table, prefix)):
            if row < table_start_row or (table_stop_row is not None and row >= table_stop_row):
                continue
            clean_row = row.split(':')[1]
            cur_row = self.get_row(table, clean_row, check=False, keys_only=keys_only)
            if not keep_row(cur_row):
                continue
            yield clean_row, cur_row


class HBaseDB(BaseDB):

    def __init__(self, server, port, *args, **kw):
        if hasattr(self, 'args'):
            self.args += [server, port]
        else:
            self.args = [server, port]
        self.__thrift = hadoopy_hbase.connect(server, port)
        self.num_mappers = 6
        super(HBaseDB, self).__init__(*args, **kw)

    def __reduce__(self):
        return (HBaseDB, self.args)

    def mutate_row(self, table, row, mutations):
        mutations = [hadoopy_hbase.Mutation(column=x, value=y) for x, y in mutations.items()]
        self.__thrift.mutateRow(table, row, mutations)

    def delete_row(self, table, row):
        self.__thrift.deleteAllRow(table, row)

    def delete_column(self, table, row, column):
        self.__thrift.mutateRow(table, row, [hadoopy_hbase.Mutation(column=column, isDelete=True)])

    def get_row(self, table, row, columns=None):
        if columns:
            result = self.__thrift.getRowWithColumns(table, row, columns)
        else:
            result = self.__thrift.getRow(table, row)
        if not result:
            bottle.abort(404)
        return {x: y.value for x, y in result[0].columns.items()}

    def get_column(self, table, row, column):
        try:
            return self.__thrift.get(table, row, column)[0].value
        except IndexError:
            bottle.abort(404)

    def scanner(self, table, start_row=None, stop_row=None, columns=None, keys_only=False, per_call=1, column_filter=None):
        filts = ['KeyOnlyFilter()'] if keys_only else []
        if column_filter:
            sanitary = lambda x: re.search("^[a-zA-Z0-9@\.:]+$", x)
            filter_family, filter_column = column_filter[0].split(':')
            if column_filter[1] == '=':
                filter_relation = '='
                filter_value = 'binary:' + column_filter[2]
            elif column_filter[1] == '!=':
                filter_relation = '!='
                filter_value = 'binary:' + column_filter[2]
            elif column_filter[1] == 'startswith':
                filter_relation = '='
                filter_value = 'binaryprefix:' + column_filter[2]
            else:
                bottle.abort(400)  # Bad filter
            if any(not sanitary(x) for x in [filter_family, filter_column, filter_value]):
                bottle.abort(400)
            filts.append("SingleColumnValueFilter ('%s', '%s', %s, '%s', true, true)" % (filter_family, filter_column, filter_relation, filter_value))
        filt = ' AND '.join(filts)
        if not filt:
            filt = None
        return hadoopy_hbase.scanner(self.__thrift, table, columns=columns,
                                     start_row=start_row, stop_row=stop_row, filter=filt, per_call=per_call)


class HBaseDBHadoop(HBaseDB):

    def __init__(self, *args, **kw):
        super(HBaseDBHadoop, self).__init__(*args, **kw)

    def __reduce__(self):
        return (HBaseDBHadoop, self.args)

    def exif_job(self, start_row, stop_row, job_row):
        cmdenvs = {'HBASE_TABLE': 'images',
                   'HBASE_OUTPUT_COLUMN': base64.b64encode('meta:exif')}
        output_hdfs = 'picarus_temp/%f/' % time.time()
        hadoop_wait_till_started(hadoopy_hbase.launch('images', output_hdfs + str(random.random()), 'hadoop/image_exif.py', libjars=['hadoopy_hbase.jar'],
                                                      num_mappers=self.num_mappers, columns=['data:image'], single_value=True,
                                                      jobconfs={'mapred.task.timeout': '6000000', 'picarus.job.row': job_row}, cmdenvs=cmdenvs, check_script=False,
                                                      make_executable=False, start_row=start_row, stop_row=stop_row, name=job_row, wait=False))

    def takeout_chain_job(self, table, model, input_column, output_column, start_row, stop_row, job_row):
        output_hdfs = 'picarus_temp/%f/' % time.time()
        model_fp = model_tofile(model)
        cmdenvs = {'HBASE_TABLE': table,
                   'HBASE_OUTPUT_COLUMN': base64.b64encode(output_column),
                   'MODEL_FN': os.path.basename(model_fp.name)}
        hadoop_wait_till_started(hadoopy_hbase.launch(table, output_hdfs + str(random.random()), 'hadoop/takeout_chain_job.py', libjars=['hadoopy_hbase.jar'],
                                                      num_mappers=self.num_mappers, files=[model_fp.name], columns=[input_column], single_value=True,
                                                      jobconfs={'mapred.task.timeout': '6000000', 'picarus.job.row': job_row}, cmdenvs=cmdenvs, dummy_fp=model_fp,
                                                      check_script=False, make_executable=False,
                                                      start_row=start_row, stop_row=stop_row, name=job_row, wait=False))
