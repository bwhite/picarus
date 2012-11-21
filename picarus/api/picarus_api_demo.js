function display_alert(message) {
    $('#alert_placeholder').html('<div class="alert"><a class="close" data-dismiss="alert">×</a><span>' + message + '</span></div>');
}
function clear_alert() {
    $('#alert_placeholder').html('');
}
function reset_state() {
    clear_alert();
    $('#texton_argmax').attr('src', '');
    $('#colors_argmax').attr('src', '');
    reset_bar();
    update_bar();
}

function b64_urlsafe(data) {
    return data.replace('+', '-').replace('/', '_');
}

function reset_bar() {
    progress_total = $('.result_box').length;
    progress_success = 0;
    progress_fail = 0;
}

function update_bar() {
    $('#pbar-success').css('width', String(100 * progress_success / progress_total) + "%");
    $('#pbar-danger').css('width', String(100 * progress_fail / progress_total) + "%");
}

function entry_func() {
    $('#demobutton').click(run_demo);
    var submit_func = function(event) {
        if(event.keyCode == 13) {
            $("#demobutton").click();
        }
    }
    load_cookie($('#demouser'), $('#demopass'));
    reset_state();
}

function picarus_api_test_demo(url, method, args) {
    function success(xhr) {
        progress_success += 1;
        update_bar();
        if (args.hasOwnProperty('success'))
            args.success(xhr)
    }
    function fail(xhr) {
        progress_fail += 1;
        update_bar();
        if (args.hasOwnProperty('fail'))
            args.fail(xhr)
    }
    picarus_api_test(url, method, _.extend({}, args, {success: success, fail: fail, email: $('#demouser').val(), auth: $('#demopass').val()}));
}