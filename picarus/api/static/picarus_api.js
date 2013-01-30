function picarus_api(url, method, args) {
    /* args: data, image, email, auth, success, fail, before_send */
    if (typeof args == 'undefined' ) args = {};
    var success;
    if (args.hasOwnProperty('success')) success = function(msg, text_status, xhr) {args.success(xhr)};

    var data = new FormData();
    if (method == 'GET') {
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
        if (args.hasOwnProperty('image')) {
            jQuery.each(args.image.files, function(i, file) {
                data.append('image', file);
            });
        }
    }
    var request = $.ajax({
        type: method,
        url: url,
        contentType: false,
        processData: false, // needed for POSTing of binary data
        beforeSend: function(xhr) {
            if (args.hasOwnProperty('email') && args.hasOwnProperty('auth'))
                xhr.setRequestHeader("Authorization", "Basic " + base64.encode(args.email + ":" + args.auth));
            if (args.hasOwnProperty('before_send')) args.before_send(xhr);
        },
        data: data,
        success: success
    });
    if (args.hasOwnProperty('fail')) request.fail(function(xhr, text_status) {args.fail(xhr)});
}

function picarus_api_test(url, method, args) {
    /* args: data, image, email, auth, div, success, fail */
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


/* Handle email/auth cookies */
function store_cookie(email, auth) {
    $.cookie("email", email, {secure: true});
    $.cookie("auth", auth, {secure: true});
}

function load_cookie(email_input, auth_input) {
    /* Return {email, auth} object, if provided set email/auth inputs (e.g., textboxes) */
    var email_auth = {email: $.cookie("email"), auth: $.cookie("auth")};
    if (typeof email_input != 'undefined' ) {
        email_input.val(email_auth.email);
    }
    if (typeof auth_input != 'undefined' ) {
        auth_input.val(email_auth.auth);
    }
    return email_auth;
}


function picarus_api_data_scanner(auth, table, startRow, stopRow, columns, success, done, max_rows, max_rows_iter) {
    if (typeof max_rows == "undefined") {
        max_rows = Infinity;
    }
    if (typeof max_rows_iter == "undefined") {
        max_rows_iter = 101;
    }
    function param_encode(dd) {
        return _.map(dd, function (v) {
            return v.join('=');
        }).join('&');
    }
    function b64_urlsafe(data) {
        return base64.encode(data).replace(/\+/g , '-').replace(/\//g , '_');
    }
    var column_suffix = _.map(columns, function (value) {return ['column', encodeURIComponent(value)]});
    var lastRow = undefined;
    var successRows = 0;
    function map_success(xhr) {
        response = JSON.parse(xhr.responseText);  // {data: {row_key_b64: col_val_b64}}
        var data = _.map(response.data, function (value) {
            return [base64.decode(value[0]), _.object(_.map(value[1], function (v, k) {return [base64.decode(k), base64.decode(v)]}))];
        });
        var isdone = true;
        max_rows -= data.length;
        if (response.hasOwnProperty("cursor") && max_rows > 0) {
            console.log('next');
            var dd = _.pairs({maxRows: String(Math.min(max_rows, max_rows_iter)), excludeStart: "1", cursor: response.cursor}).concat(column_suffix);
            var url = "/a1/rows/" + b64_urlsafe(table) + "/" + b64_urlsafe(_.last(data)[0]) + "/" + b64_urlsafe(stopRow) + "?" + param_encode(dd);
            console.log(url);
            picarus_api(url, "GET", _.extend({success: map_success}, auth));
            isdone = false;
        } else if (max_rows < 0) {
            // Truncates any excess rows we may have gotten
            data = data.slice(0, max_rows);
        }
        _.each(data, function (v) {
            lastRow = v[0];
            success(v[0], v[1]);
        });
        successRows += data.length;
        console.log(successRows);
        console.log(max_rows);
        if (isdone && typeof done != "undefined") {
            console.log('Done');
            done(lastRow, successRows);
        }
    }
    var dd = _.pairs({maxRows: String(Math.min(max_rows, max_rows_iter))}).concat(column_suffix);
    //picarus_api("/a1/rows/" + b64_urlsafe(table) +  "/" + b64_urlsafe(startRow) + "/" + b64_urlsafe(stopRow) + "?" + param_encode(dd), "GET", _.extend({success: map_success}, auth));
    var dd = _.object(_.pairs({maxRows: String(Math.min(max_rows, max_rows_iter))}).concat(column_suffix));
    picarus_api("/a1/rows/" + b64_urlsafe(table) +  "/" + b64_urlsafe(startRow) + "/" + b64_urlsafe(stopRow), "GET", _.extend({success: map_success, data: dd}, auth));
}