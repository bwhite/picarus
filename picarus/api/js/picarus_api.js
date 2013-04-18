function encode_id(data) {
    return base64.encode(data).replace(/\+/g , '-').replace(/\//g , '_');
}

function decode_id(data) {
    return base64.decode(data.replace(/\-/g , '+').replace(/\_/g , '/'));
}

function PicarusClient(email, apiKey, server) {
    if (_.isUndefined(server))
        server = 'https://api.picar.us';
    this.email = email;
    this.apiKey = apiKey;
    this.server = server;
    this.version = 'a1';

    this.get = function (path, data, success, fail) {
        path = [this.server, this.version].concat(_.map(path, encodeURIComponent)).join('/');
        $.ajax(path, {data: data, success: success}).fail(fail);
    };

    this._ajax = function (path, data, success, fail, type) {
        path = [this.server, this.version].concat(_.map(path, encodeURIComponent)).join('/');
        var formData = new FormData();
        _.each(data, function (v, k) {
            formData.append(k, v);
        });
        $.ajax(path, {type: type, data: formData, success: success, contentType: false, processData: false}).fail(fail);
    };
    
    this.post = function (path, data, success, fail) {
        this._ajax(path, data, success, fail, 'POST');
    };

    this.patch = function (path, data, success, fail) {
        this._ajax(path, data, success, fail, 'PATCH');
    };

    this.del = function (path, data, success, fail) {
        this._ajax(path, data, success, fail, 'DELETE');
    };

    this.getTable = function (table, args) {
        //args: success, fail, columns
        args = this._argsDefaults(args);
        if (_.has(args, 'columns'))
            args.data.columns = _.map(args.columns, function(x) {return base64.encode(x)}).join(',');
        this.get(['data', table], args.data, this._wrapDecodeLod(args.success), args.fail);
    };
    this.postTable = function (table, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        this.post(['data', table], this.encdict(args.data), this._wrapDecodeValues(args.success), args.fail);
    };
    this.postRow = function (table, row, action, model, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        args.data.action = action;
        args.data.model = base64.encode(model);
        this.post(['data', table, encode_id(row)], args.data, this._wrapDecodeDict(args.success), args.fail);
    };
    this.deleteRow = function (table, row, args) {
        //args: success, fail
        args = this._argsDefaults(args);
        drow = row;
        this.del(['data', table, encode_id(row)], args.data, this._wrapNull(args.success), args.fail);
    };
    this.postSlice = function (table, startRow, stopRow, action, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        args.data.action = action;
        this.post(['slice', table, encode_id(startRow), encode_id(stopRow)], args.data, this._wrapNull(args.success), args.fail);
    };

    this.patchRow = function (table, row, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        this.patch(['data', table, encode_id(row)], this.encdict(args.data), this._wrapDecodeValues(args.success), args.fail);
    };
    this.encdict = function (d) {
        return _.object(_.map(d, function (v, k) {
            if (!_.isObject(v)) // NOTE(brandyn): The reason is that files are "object" type
                v = base64.encode(v);
            return [base64.encode(k), v];
        }));
    };
    this.getRow = function (table, row, args) {
        //args: success, fail, columns
        args = this._argsDefaults(args);
        if (_.has(args, 'columns'))
            args.data.columns = _.map(args.columns, function(x) {return base64.encode(x)}).join(',');
        this.get(['data', table, encode_id(row)], args.data, this._wrapDecodeDict(args.success), args.fail);
    };
    this.getSlice = function (table, startRow, stopRow, args) {
        //args: success, fail, columns, data
        args = this._argsDefaults(args);
        if (_.has(args, 'columns'))
            args.data.columns = _.map(args.columns, function(x) {return base64.encode(x)}).join(',');
        this.get(['slice', table, encode_id(startRow), encode_id(stopRow)], args.data, this._wrapDecodeLod(args.success), args.fail);
    };
    this.scanner = function (table, startRow, stopRow, args) {
        // args: success, fail, done, maxRows, maxRowsIter, filter, resume
        args = this._argsDefaults(args);
        if (_.isUndefined(args.maxRows)) {
            args.maxRows = Infinity;
        }
        if (_.isUndefined(args.maxRowsIter)) {
            args.maxRowsIter = Math.min(10000, args.maxRows);
        }
        if (_.isUndefined(args.maxBytes)) {
            args.maxBytes = 1048576;
        }
        var lastRow = undefined;
        var numRows = 0;
        if (!_.isUndefined(args.filter)) {
            iterArgs.data.filter = args.filter;
        }
        function innerSuccess(data) {
            debug_data = data;
            var isdone = true;
            args.maxRows -= data.length;
            if (args.maxRows < 0) {
                // Truncates any excess rows we may have gotten
                data = data.slice(0, args.maxRows);
            }
            if (numRows == 0 && data.length && !_.isUndefined(args.first)) {
                var firstRow = _.first(data);
                args.first(firstRow[0], firstRow[1]);
            }
            _.each(data, function (v) {
                lastRow = v[0];
                args.success(v[0], v[1]);
            });
            numRows += data.length;
            console.log(numRows);
            // If there is more data left to get, and we want more data
            // It's possible that this will make 1 extra call at the end that returns nothing,
            // but there are several trade-offs and that is the simplest implementation that doesn't
            // encode extra parameters, modify status codes (nonstandard), output fixed rows only, etc.
            if (data.length && args.maxRows > 0) {
                isdone = false;
                console.log('Not Done');
                function nextCall() {
                    iterArgs.data.excludeStart = 1;
                    this.getSlice(table, _.last(data)[0], stopRow, iterArgs);
                }
                nextCall = _.bind(nextCall, this);
                // This allows for pagination instead of immediately requesting the next chunk
                if (_.isUndefined(args.resume))
                    nextCall();
                else
                    args.resume(nextCall);
            }
            if (isdone && !_.isUndefined(args.done))
                args.done({lastRow: lastRow, numRows: numRows});
        }
        var iterArgs = {data: {maxRows: args.maxRowsIter}, success: _.bind(innerSuccess, this), fail: args.fail};
        if (_.has(args, 'columns'))
            iterArgs.columns = args.columns;
        this.getSlice(table, startRow, stopRow, iterArgs);
    };
    this._argsDefaults = function (args) {
        args = _.clone(args);
        if (!_.has(args, 'success'))
            args.success = function () {};
        if (!_.has(args, 'fail'))
            args.fail = function () {};
        if (!_.has(args, 'data'))
            args.data = {};
        return args;
    };
    this._wrapDecodeLod = function(f) {
        return function(msg, text_status, xhr) {
            f(_.map(JSON.parse(xhr.responseText), function (x) {
                var row = base64.decode(x.row);
                var columns = _.object(_.map(_.omit(x, 'row'), function (v, k) {
                    return [base64.decode(k), base64.decode(v)];
                }));
                return [row, columns];
            }));
        };
    };
    this._wrapNull = function(f) {
        return function(msg, text_status, xhr) {
            f();
        };
    };
    this._wrapDecodeDict = function(f) {
        return function(msg, text_status, xhr) {
            f(_.object(_.map(JSON.parse(xhr.responseText), function (v, k) {
                    return [base64.decode(k), base64.decode(v)];
            })));
        };
    };
    this._wrapDecodeValues = function(f) {
        return function(msg, text_status, xhr) {
            f(_.object(_.map(JSON.parse(xhr.responseText), function (v, k) {
                    return [k, base64.decode(v)];
            })));
        };
    };
    this.test = function () {
        this.getTable('parameters', {success: function (x) {console.log('Set debug_a'); debug_a=x}});
        this.getTable('models', {success: function (x) {console.log('Set debug_b'); debug_b=x}, columns: ['meta:']});
        this.getSlice('images', 'sun397:', 'sun397;', {success: function (x) {console.log('Set debug_c'); debug_c=x}, columns: ['meta:']});
        this.scanner('images', 'sun397:', 'sun397;', {columns: ['meta:'], maxRows: 10, success: function (x) {console.log('Set debug_i'); debug_i=x}})
        this.postSlice('images', 'automated_tests:', 'automated_tests;', 'io/thumbnail', {success: function (x) {console.log('Set debug_g'); debug_g=x}});
        function test_patchRow(row) {
            this.patchRow('images', row, {success: function (x) {console.log('Set debug_f'); debug_f=x;test_getRow(row)}, data: {'meta:class_0': 'test_data2'}});
        }
        function test_deleteRow(row) {
            this.deleteRow('images', row, {success: function (x) {console.log('Set debug_h'); debug_h=x}});
        }
        function test_getRow(row) {
            this.getRow('images', row, {success: function (x) {console.log('Set debug_d'); debug_d=x;test_deleteRow(row)}, columns: ['meta:']});
        }
        test_getRow = _.bind(test_getRow, this);
        test_deleteRow = _.bind(test_deleteRow, this);
        test_patchRow = _.bind(test_patchRow, this);
        this.postTable('images', {success: function (x) {console.log('Set debug_e');debug_e=x;test_patchRow(x.row);}, data: {'meta:class': 'test_data'}});
        this.postRow('images', base64.decode('c3VuMzk3OnRlc3QAC2nfc3VuX2F4dndzZHd5cW1waG5hcGIuanBn'), 'i/chain', base64.decode('ZmVhdDpRhhxwtznn3dTyAfPRMSdO'), {success: function (x) {console.log('Set debug_g'); debug_g=x}});
    };
}
/*

class PicarusClient(object):

    def __init__(self, email, api_key, server="https://api.picar.us"):
        self.email = email
        self.api_key = api_key
        self.server = server
        self.version = 'a1'

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

    # raw

    def get(self, path, data=None):
        path = '/'.join(map(urllib.quote_plus, path))
        r = requests.get('%s/%s/%s' % (self.server, self.version, path), auth=(self.email, self.api_key), params=data)
        return self._check_status(r)

    def post(self, path, data=None, files=None):
        path = '/'.join(map(urllib.quote_plus, path))
        r = requests.post('%s/%s/%s' % (self.server, self.version, path), auth=(self.email, self.api_key), data=data, files=files)
        return self._check_status(r)

    def delete(self, path, data=None):
        path = '/'.join(map(urllib.quote_plus, path))
        r = requests.delete('%s/%s/%s' % (self.server, self.version, path), auth=(self.email, self.api_key), data=data)
        return self._check_status(r)

    def patch(self, path, data=None, files=None):
        path = '/'.join(map(urllib.quote_plus, path))
        r = requests.patch('%s/%s/%s' % (self.server, self.version, path), auth=(self.email, self.api_key), data=data, files=files)
        return self._check_status(r)

    def _encode_columns(self, columns):
        data = {}
        if columns is not None:
            data['columns'] = ','.join(map(self.enc, columns))
        return data

    # /data/:table

    def getTable(self, table, columns=None):
        return self._decode_lod(self.get(('data', table), data=self._encode_columns(columns)))

    def postTable(self, table, data=None, files=None):
        return self.decvalues(self.post(('data', table), data=self.encdict(data), files=self.enckeys(files)))

    # /data/:table/:row

    def getRow(self, table, row, columns=None):
        return self.decdict(self.get(('data', table, self.enc(row)), data=self._encode_columns(columns)))

    def postRow(self, table, row, data=None, files=None):
        return self.post(('data', table, self.enc(row)), data=data, files=files)

    def deleteRow(self, table, row):
        return self.delete(('data', table, self.enc(row)))

    def patchRow(self, table, row, data=None, files=None):
        return self.patch(('data', table, self.enc(row)), data=self.encdict(data), files=self.enckeys(files))

    # /slice/:table/:start_row/:stop_row

    def getSlice(self, table, start_row, stop_row, columns=None, data=None):
        column_data = self._encode_columns(columns)
        if data is not None:
            column_data.update(data)
        return self._decode_lod(self.get(('slice', table, self.enc(start_row), self.enc(stop_row)), data=column_data))

    def postSlice(self, table, start_row, stop_row, action, data=None):
        if data is None:
            data = {}
        data['action'] = action
        return self.post(('slice', table, self.enc(start_row), self.enc(stop_row)), data=data)

    def patch_slice(self, table, start_row, stop_row, data=None):
        return self.patch(('slice', table, self.enc(start_row), self.enc(stop_row)), data=self.encdict(data))

    def scanner(self, table, start_row, stop_row, columns=None):
        max_rows_iter = 10000
        data = {}
        data['maxRows'] = max_rows_iter
        while True:
            row_columns = self.getSlice(table, start_row, stop_row, columns=columns, data=data)
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

    def encdict(self, d):
        return {self.enc(x): self.enc(y) for x, y in d.items()}

    def decdict(self, d):
        return {self.dec(x): self.dec(y) for x, y in d.items()}

    def enckeys(self, d):
        return {self.enc(x): y for x, y in d.items()}

    def decvalues(self, d):
        return {x: self.dec(y) for x, y in d.items()}

*/

function prefix_to_stop_row(prefix) {
    // TODO: need to fix wrap around if last char is "255"
    return prefix.slice(0, -1) + String.fromCharCode(prefix.slice(-1).charCodeAt(0) + 1);
}

function picarus_api(url, method, args) {
    /* args: data, email, auth, success, fail */
    if (typeof args == 'undefined' ) args = {};
    var success;
    if (args.hasOwnProperty('success')) success = function(msg, text_status, xhr) {args.success(xhr)};

    function param_encode(data) {
        return _.map(data, function (v, k) {
            return k + '=' + v;
        }).join('&');
    }

    var data = new FormData();
    if (method === 'GET') {
        data = undefined;
        if (args.hasOwnProperty('data')) {
            url += '?' + param_encode(args.data);
        }
    } else {
        if (args.hasOwnProperty('data')) {
            jQuery.each(args.data, function(k, v) {
                data.append(k, v);
            });
        }
    }
    var options = {
        type: method,
        url: url,
        contentType: false,
        processData: false, // needed for POSTing of binary data
        data: data,
        success: success
    }
        
    if (args.hasOwnProperty('email') && args.hasOwnProperty('auth')) {
        options.beforeSend = function(xhr) {
            xhr.setRequestHeader("Authorization", "Basic " + base64.encode(args.email + ":" + args.auth));
        };
    }
    var request = $.ajax(options);
    if (args.hasOwnProperty('fail')) request.fail(function(xhr, text_status) {args.fail(xhr)});
}

function picarus_api_row(table, row, method, args) {
    picarus_api("/a1/data/" + table + "/" + row, method, args);
}

function picarus_api_upload(table, args) {
    picarus_api("/a1/data/" + table, "POST", args);
}

function picarus_api_test(url, method, args) {
    /* args: data, email, auth, div, success, fail */
    if (typeof args == 'undefined' ) args = {};
    function clear_error() {
    }
    function report_result(xhr, label_type) {
        if (args.hasOwnProperty('div')) {
            args.div.html('<span class="label ' + label_type +'">' + xhr.status + '</span><p><pre>' + args.data  +  '</pre></p><p><pre>' + xhr.getAllResponseHeaders() + '</pre></p><p><pre>' + xhr.responseText + '</pre></p>');
        }
    }
    function before_send(xhr) {
        clear_error();
        if (args.hasOwnProperty('div')) {
            args.div.html('<span class="label warning">' + 'Running' + '</span>');
        }
    }
    function success(xhr) {
        report_result(xhr, "label-success");
        if (args.hasOwnProperty('success')) {
            args.success(xhr);
        }
    }
    function fail(xhr) {
        clear_error();
        report_result(xhr, "label-important");
        if (args.hasOwnProperty('fail')) {
            args.fail(xhr);
        }
    }
    picarus_api(url, method, _.extend({}, args, {success: success, fail: fail, before_send: before_send}));
}

function class_key(classes, div) {
    div.html('');
    cur_classes = classes;
    classes = _.map(classes, function (value, class_name) {
        value.name = class_name;
        return value;
    });
    classes = _.sortBy(classes, 'mask_num');
    _.each(classes, function (value) {
        div.append($('<span>', {style: 'color:rgb(' + value['color'][0] + ','+ value['color'][1] + ',' + value['color'][2] + ')'}).html('&#x25A0;'));
        div.append(' (' + value['mask_num'] + ') ' + value['name']);
        div.append('<br>');
    })
}

function picarus_api_data_scanner(table, startRow, stopRow, columns, params) {
    // params: success, done, maxRows, maxRowsIter, first, filter, resume
    if (typeof params.maxRows == "undefined") {
        params.maxRows = Infinity;
    }
    if (typeof params.maxRowsIter == "undefined") {
        params.maxRowsIter = Math.min(10000, params.maxRows);
    }
    if (typeof params.maxBytes == "undefined") {
        params.maxBytes = 1048576;
    }
    function param_encode(dd) {
        return _.map(dd, function (v) {
            return v.join('=');
        }).join('&');
    }
    // Removed encode_id(x) below, should add it back after refactor that exposes unencoded data only
    var column_suffix =  [['columns', _.map(columns, function (x) {return x}).join(',')]];
    var lastRow = undefined;
    var numRows = 0;
    if (typeof params.filter != "undefined") {
        column_suffix = column_suffix.concat([['filter', escape(params.filter)]]);
    }
    function map_success(xhr) {
        var data = JSON.parse(xhr.responseText);
        var isdone = true;
        params.maxRows -= data.length;
        if (params.maxRows < 0) {
            // Truncates any excess rows we may have gotten
            data = data.slice(0, params.maxRows);
        }
        if (numRows == 0 && data.length && typeof params.first != "undefined") {
            var firstRow = _.first(data);
            params.first(firstRow.row, _.omit(firstRow, 'row'));
        }
        if (typeof params.success != "undefined") {
            _.each(data, function (v) {
                lastRow = v.row;
                params.success(v.row, _.omit(v, 'row'));
            });
        }
        numRows += data.length;
        console.log(numRows);
        // If there is more data left to get, and we want more data
        // It's possible that this will make 1 extra call at the end that returns nothing,
        // but there are several trade-offs and that is the simplest implementation that doesn't
        // encode extra parameters, modify status codes (nonstandard), output fixed rows only, etc.
        if (data.length && params.maxRows > 0) {
            isdone = false;
            function nextCall() {
                var dd = _.pairs({maxRows: String(params.maxRowsIter), excludeStart: "1"}).concat(column_suffix);
                var url = "/a1/slice/" + table + "/" + _.last(data).row + "/" + stopRow + '?' + param_encode(dd);
                picarus_api(url, "GET", {success: map_success});
            }
            // This allows for pagination instead of immediately requesting the next chunk
            if (typeof params.resume == "undefined") {
                nextCall();
            } else {
                params.resume(nextCall);
            }
        }
        if (isdone && typeof params.done != "undefined") {
            params.done({lastRow: lastRow, numRows: numRows});
        }
    }
    var dd = _.pairs({maxRows: String(params.maxRowsIter)}).concat(column_suffix);
    picarus_api("/a1/slice/" + table +  "/" + startRow + "/" + stopRow + '?' + param_encode(dd), "GET", {success: map_success});
}


function picarus_api_delete_rows(rows, params) {
    function action(row, s) {
        PICARUS.deleteRow('images', row, {success: s})
    }
    picarus_api_row_action(rows, action, params);
}

function picarus_api_modify_rows(rows, column, value, params) {
    var data = {};
    data[column] = value;
    function action(row, s) {
        PICARUS.patchRow('images', row, {success: s, data: data})
    }
    picarus_api_row_action(rows, action, params);
}


function picarus_api_row_action(rows, action, params) {
    var maxRowsIter = 20;
    var rowsLeft = rows.length;
    var origRows = rows.length;
    if (_.isUndefined(params))
        params = {};
    if (!_.isUndefined(params.maxRowsIter))
        maxRowsIter = params.maxRowsIter;
    if (_.isUndefined(params.update))
        params.update = function () {};
    if (_.isUndefined(params.done))
        params.done = function () {};
    if (!rowsLeft)
        params.done();
    function success() {
        rowsLeft -= 1;
        params.update(1 - rowsLeft / origRows);
        if (!rowsLeft)
            params.done();
    }
    function work(s) {
        var row = rows.pop();
        if (_.isUndefined(row))
            return;
        action(row, s);
    }
    _.each(_.range(maxRowsIter), function () {
        work(function () { 
                 success();
                 while (rows.length)
                     work(success);
             });
    });
}
