function prefix_to_stop_row(prefix) {
    // TODO: need to fix wrap around if last char is "255"
    return prefix.slice(0, -1) + String.fromCharCode(prefix.slice(-1).charCodeAt(0) + 1);
}

function picarus_api(url, method, args) {
    /* args: data, email, auth, success, fail */
    if (typeof args == 'undefined' ) args = {};
    var success;
    if (args.hasOwnProperty('success')) success = function(msg, text_status, xhr) {args.success(xhr)};

    var data = new FormData();
    if (method === 'GET') {
        data = undefined;
        if (args.hasOwnProperty('data')) {
            data = data;
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

function encode_id(data) {
    return base64.encode(data).replace(/\+/g , '-').replace(/\//g , '_');
}

function decode_id(data) {
    return base64.decode(data.replace(/\-/g , '+').replace(/\_/g , '/'));
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
    var column_suffix = _.map(columns, function (value) {return ['column', value]});
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
            function next_call() {
                var dd = _.pairs({maxRows: String(params.maxRowsIter), excludeStart: "1"}).concat(column_suffix);
                var url = "/a1/slice/" + table + "/" + _.last(data).row + "/" + stopRow + '?' + param_encode(dd);
                picarus_api(url, "GET", {success: map_success});
            }
            // This allows for pagination instead of immediately requesting the next chunk
            if (typeof params.resume == "undefined") {
                next_call();
            } else {
                params.resume(next_call);
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
    var maxRowsIter = 1;
    if (typeof params == "undefined") {
        params = {};
    }
    // TODO: Can't increase maxRowsIter until done is called after the very last element returns
    if (typeof params.maxRowsIter != "undefined") {
        maxRowsIter = params.maxRowsIter;
    }
    if (!rows.length) {
        if (typeof params.done != "undefined") {
            params.done();
        }
        return;
    }
    _.each(rows.slice(0, maxRowsIter), function (row, n) {
        var del_params = {};
        if (n == 0) {
            del_params.success = function () {picarus_api_delete_rows(rows.slice(maxRowsIter), params)};
        }
        picarus_api_row('images', row, "DELETE", del_params);
    });
}
