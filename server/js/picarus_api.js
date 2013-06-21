function encode_id(data) {
    return base64.encode(data).replace(/\+/g , '-').replace(/\//g , '_');
}

function decode_id(data) {
    return base64.decode(data.replace(/\-/g , '+').replace(/\_/g , '/'));
}

function PicarusClient(args) {
    this.version = 'v0';

    this.setAuth = function (email, key) {
        $.ajaxSetup({'beforeSend': function (xhr) {
            xhr.setRequestHeader("Authorization", "Basic " + base64.encode(email + ":" + key));
        }});
    };

    if (_.isUndefined(args) || _.isUndefined(args.server))
        this.server = '';
    else
        this.server = args.server;

    if (!(_.isUndefined(args) || _.isUndefined(args.email) || _.isUndefined(args.apiKey)))
        this.setAuth(args.email, args.apiKey);

    this.get = function (path, data, success, fail) {
        path = [this.server, this.version].concat(_.map(path, encodeURIComponent)).join('/');
        return $.ajax(path, {data: data, success: success}).fail(fail);
    };

    this._ajax = function (path, data, success, fail, type) {
        path = [this.server, this.version].concat(_.map(path, encodeURIComponent)).join('/');
        var formData = new FormData();
        _.each(data, function (v, k) {
            formData.append(k, v);
        });
        return $.ajax(path, {type: type, data: formData, success: success, contentType: false, processData: false}).fail(fail);
    };
    
    this.post = function (path, data, success, fail) {
        return this._ajax(path, data, success, fail, 'POST');
    };

    this.patch = function (path, data, success, fail) {
        return this._ajax(path, data, success, fail, 'PATCH');
    };

    this.del = function (path, data, success, fail) {
        return this._ajax(path, data, success, fail, 'DELETE');
    };

    this.authEmailAPIKey = function (args) {
        args = this._argsDefaults(args);
        return this.post(["auth", "email"], {}, this._wrapNull(args.success), args.fail);
    };

    this.authYubikey = function (otp, args) {
        args = this._argsDefaults(args);
        return this.post(["auth", "yubikey"], {otp: otp}, this._wrapParseJSON(args.success), args.fail);
    };

    this.getTable = function (table, args) {
        //args: success, fail, columns
        args = this._argsDefaults(args);
        if (_.has(args, 'columns'))
            args.data.columns = _.map(args.columns, function(x) {return base64.encode(x)}).join(',');
        return this.get(['data', table], args.data, this._wrapDecodeLod(args.success), args.fail);
    };
    this.postTable = function (table, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        return this.post(['data', table], this.encdict(args.data), this._wrapDecodeValues(args.success), args.fail);
    };
    this.postRow = function (table, row, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        return this.post(['data', table, encode_id(row)], this.encvalues(args.data), this._wrapDecodeDict(args.success), args.fail);
    };
    this.deleteRow = function (table, row, args) {
        //args: success, fail
        args = this._argsDefaults(args);
        return this.del(['data', table, encode_id(row)], args.data, this._wrapNull(args.success), args.fail);
    };
    this.deleteColumn = function (table, row, column, args) {
        //args: success, fail
        args = this._argsDefaults(args);
        return this.del(['data', table, encode_id(row), encode_id(column)], args.data, this._wrapNull(args.success), args.fail);
    };
    this.postSlice = function (table, startRow, stopRow, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        return this.post(['slice', table, encode_id(startRow), encode_id(stopRow)], this.encvalues(args.data), this._wrapDecodeDict(args.success), args.fail);
    };

    this.patchRow = function (table, row, args) {
        //args: success, fail, data
        args = this._argsDefaults(args);
        return this.patch(['data', table, encode_id(row)], this.encdict(args.data), this._wrapDecodeValues(args.success), args.fail);
    };
    this.encdict = function (d) {
        // TODO: Add same logic as the python library for upgrading to file blobs
        return _.object(_.map(d, function (v, k) {
            if (!_.isObject(v)) // NOTE(brandyn): The reason is that files are "object" type
                v = base64.encode(v);
            return [base64.encode(k), v];
        }));
    };
    this.encvalues = function (d) {
        // TODO: Add same logic as the python library for upgrading to file blobs
        return _.object(_.map(d, function (v, k) {
            if (!_.isObject(v)) // NOTE(brandyn): The reason is that files are "object" type
                v = base64.encode(v);
            return [k, v];
        }));
    };
    this.getRow = function (table, row, args) {
        //args: success, fail, columns
        args = this._argsDefaults(args);
        if (_.has(args, 'columns'))
            args.data.columns = _.map(args.columns, function(x) {return base64.encode(x)}).join(',');
        return this.get(['data', table, encode_id(row)], args.data, this._wrapDecodeDict(args.success), args.fail);
    };
    this.getSlice = function (table, startRow, stopRow, args) {
        //args: success, fail, columns, data
        args = this._argsDefaults(args);
        if (_.has(args, 'columns'))
            args.data.columns = _.map(args.columns, function(x) {return base64.encode(x)}).join(',');
        return this.get(['slice', table, encode_id(startRow), encode_id(stopRow)], args.data, this._wrapDecodeLod(args.success), args.fail);
    };
    this.patchSlice = function (table, startRow, stopRow, args) {
        //args: success, fail, columns, data
        args = this._argsDefaults(args);
        return this.patch(['slice', table, encode_id(startRow), encode_id(stopRow)], this.encdict(args.data), this._wrapNull(args.success), args.fail);
    };
    this.deleteSlice = function (table, startRow, stopRow, args) {
        //args: success, fail, columns, data
        args = this._argsDefaults(args);
        return this.del(['slice', table, encode_id(startRow), encode_id(stopRow)], {}, this._wrapNull(args.success), args.fail);
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
        if (_.has(args, 'filter'))
            iterArgs.data.filter = args.filter;
        if (_.has(args, 'columns'))
            iterArgs.columns = args.columns;
        this.getSlice(table, startRow, stopRow, iterArgs);
    };
    this._argsDefaults = function (args) {
        if (_.isUndefined(args))
            args = {};
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
    this._wrapParseJSON = function(f) {
        return function(msg, text_status, xhr) {
            f(JSON.parse(xhr.responseText));
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
        this.postSlice('images', 'automated_tests:', 'automated_tests;', {data: {action: 'io/thumbnail'}, success: function (x) {console.log('Set debug_g'); debug_g=x}});
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
        this.postRow('images', base64.decode('c3VuMzk3OnRlc3QAC2nfc3VuX2F4dndzZHd5cW1waG5hcGIuanBn'), {data: {action: 'i/chain', model: base64.decode('ZmVhdDpRhhxwtznn3dTyAfPRMSdO')}, success: function (x) {console.log('Set debug_g'); debug_g=x}});
    };
}

function prefix_to_stop_row(prefix) {
    // TODO: need to fix wrap around if last char is "255"
    return prefix.slice(0, -1) + String.fromCharCode(prefix.slice(-1).charCodeAt(0) + 1);
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
        if (!rows.length)
            return;
        var row = rows.pop();
        if (_.isUndefined(row))
            return;
        action(row, s);
    }
    function workSuccess() { 
        success();
        work(workSuccess);
    }
    _.each(_.range(maxRowsIter), function () {
        work(workSuccess);
    });
}
