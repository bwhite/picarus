__all__ = ['api', 'modules']
from picarus import api, modules
from picarus_takeout import *
import base64
import urllib
import json
import cStringIO as StringIO


class PicarusClient(object):

    def __init__(self, email, api_key=None, login_key=None, server="https://api.picar.us"):
        self.email = email
        self.api_key = api_key
        self.login_key = login_key
        self.server = server
        self.version = 'a1'
        import requests
        self.requests = requests

    def _check_status(self, response):
        if response.status_code != 200:
            raise RuntimeError('picarus_api: returned [%d]' % (response.status_code))
        return json.loads(response.content)

    def _decode_lod(self, lod):
        row_columns = []
        for x in lod:
            row = self.dec(x['row'])
            columns = {self.dec(x): self.dec(y) for x, y in x.items() if x != 'row'}
            row_columns.append((row, columns))
        return row_columns

    def _decode_dict(self, d):
        return {self.dec(x): self.dec(y) for x, y in d.items()}

    def _split_data(self, data):
        data_out = {}
        files_out = {}
        if data is None:
            data = {}
        for k, v in data.items():
            if hasattr(v, 'read'):
                files_out[k] = v
            else:
                data_out[k] = v
        return {'data': data_out, 'files': files_out}

    # raw
    def get(self, path, data=None):
        path = '/'.join(map(urllib.quote_plus, path))
        r = self.requests.get('%s/%s/%s' % (self.server, self.version, path), auth=(self.email, self.api_key), params=data)
        return self._check_status(r)

    def post(self, path, data=None):
        path = '/'.join(map(urllib.quote_plus, path))
        r = self.requests.post('%s/%s/%s' % (self.server, self.version, path), auth=(self.email, self.api_key), **self._split_data(data))
        return self._check_status(r)

    def post_login(self, path, data=None):
        path = '/'.join(map(urllib.quote_plus, path))
        r = self.requests.post('%s/%s/%s' % (self.server, self.version, path), auth=(self.email, self.login_key), **self._split_data(data))
        return self._check_status(r)

    def delete(self, path, data=None):
        path = '/'.join(map(urllib.quote_plus, path))
        r = self.requests.delete('%s/%s/%s' % (self.server, self.version, path), auth=(self.email, self.api_key), data=data)
        return self._check_status(r)

    def patch(self, path, data=None):
        path = '/'.join(map(urllib.quote_plus, path))
        r = self.requests.patch('%s/%s/%s' % (self.server, self.version, path), auth=(self.email, self.api_key), **self._split_data(data))
        return self._check_status(r)

    def _encode_columns(self, columns):
        data = {}
        if columns is not None:
            data['columns'] = ','.join(map(self.enc, columns))
        return data

    # /auth/
    def auth_email_api_key(self):
        self.post_login(['auth', 'email'])

    # /data/:table

    def get_table(self, table, columns=None):
        return self._decode_lod(self.get(('data', table), data=self._encode_columns(columns)))

    def post_table(self, table, data=None):
        return self.decvalues(self.post(('data', table), data=self.encdict(data)))

    # /data/:table/:row

    def get_row(self, table, row, columns=None):
        return self.decdict(self.get(('data', table, self.encurl(row)), data=self._encode_columns(columns)))

    def post_row(self, table, row, data=None):
        if data and 'model' in data:
            data['model'] = base64.b64encode(data['model'])
        return self.decdict(self.post(('data', table, self.encurl(row)), data=data))

    def delete_row(self, table, row):
        return self.delete(('data', table, self.encurl(row)))

    def patch_row(self, table, row, data=None):
        return self.patch(('data', table, self.encurl(row)), data=self.encdict(data))

    # /slice/:table/:start_row/:stop_row

    def get_slice(self, table, start_row, stop_row, columns=None, data=None):
        column_data = self._encode_columns(columns)
        if data is not None:
            column_data.update(data)
        return self._decode_lod(self.get(('slice', table, self.encurl(start_row), self.encurl(stop_row)), data=column_data))

    def post_slice(self, table, start_row, stop_row, data=None):
        if data and 'model' in data:
            data['model'] = base64.b64encode(data['model'])
        return self.post(('slice', table, self.encurl(start_row), self.encurl(stop_row)), data=data)

    def patch_slice(self, table, start_row, stop_row, data=None):
        return self.patch(('slice', table, self.encurl(start_row), self.encurl(stop_row)), data=self.encdict(data))

    def scanner(self, table, start_row, stop_row, columns=None):
        max_rows_iter = 10000
        data = {}
        data['maxRows'] = max_rows_iter
        while True:
            row_columns = self.get_slice(table, start_row, stop_row, columns=columns, data=data)
            if not row_columns:
                break
            for row, columns in row_columns:
                yield row, columns
            start_row = row
            data['excludeStart'] = '1'

    def enc(self, x):
        return base64.b64encode(str(x))

    def dec(self, x):
        return base64.b64decode(str(x))

    def encurl(self, x):
        return base64.urlsafe_b64encode(str(x))

    def decurl(self, x):
        return base64.urlsafe_b64decode(str(x))

    def encdict(self, d):
        if d is None:
            return {}
        out = {}
        for k, v in d.items():
            k = self.enc(k)
            if isinstance(v, (str, unicode)):
                if len(v) > 1024 * 8:
                    out[k] = StringIO.StringIO(v)
                else:
                    out[k] = self.enc(v)
            else:
                out[k] = v
        return out

    def decdict(self, d):
        if d is None:
            return {}
        return {self.dec(x): self.dec(y) for x, y in d.items()}

    def enckeys(self, d):
        if d is None:
            return {}
        return {self.enc(x): y for x, y in d.items()}

    def decvalues(self, d):
        if d is None:
            return {}
        return {x: self.dec(y) for x, y in d.items()}
