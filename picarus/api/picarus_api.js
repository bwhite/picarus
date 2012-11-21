function picarus_api(url, method, args) {
    /* args: data, image, email, auth, success, fail, before_send */
    if (typeof args == 'undefined' ) args = {};
    var success;
    if (args.hasOwnProperty('success')) success = function(msg, text_status, xhr) {args.success(xhr)};
    var data = new FormData();
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
    var request = $.ajax({
        type: method,
        url: url,
        contentType: false,
        processData: false,
        cache: false,
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
    $.cookie("email", email, {expires : 30, secure: true});
    $.cookie("auth", auth, {expires : 30, secure: true});
}

function load_cookie(email_input, auth_input) {
    /* Return {email, auth} object, if provided set email/auth inputs (e.g., textboxes) */
    var email_auth = {email: $.cookie("email"), auth: $.cookie("auth")};
    email_input.val(email_auth.email);
    auth_input.val(email_auth.auth);
    return email_auth;
}
