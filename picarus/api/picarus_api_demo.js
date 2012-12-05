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

function db_path(table, row, column) {
    row = b64_urlsafe(base64.encode(row));
    column = b64_urlsafe(base64.encode(column));
    return '/db/' + table + '/' + row + '/' + column;
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

function setup_video(auth, table, row_prefix, column) {
    video = document.getElementById('video');
    canvas = document.getElementById('videocanvas');
    var ctx = canvas.getContext('2d');
    var localMediaStream = null;
    var img = document.getElementById('videoimg');

    function snapshot() {
        if (localMediaStream) {
            canvas.height = video.videoHeight;
            canvas.width = video.videoWidth;
            ctx.drawImage(video, 0, 0);
            img.src = canvas.toDataURL('image/jpeg');
            raw_data = img.src;
            var row = row_prefix + (2147483648 - ((new Date).getTime() / 1000)).toFixed(0);
            picarus_api(db_path(table, row, column), "PUT", _.extend({data: {data: img.src.slice(22)}}, auth));
        }
    }
    global_snapshot = snapshot;

    function fallback(e) {
        video.src = 'fallbackvideo.webm';
    }

    function success(stream) {
        video.src = window.webkitURL.createObjectURL(stream);
        localMediaStream = stream;
    }

    if (!navigator.webkitGetUserMedia) {
        fallback();
    } else {
        navigator.webkitGetUserMedia({video: true}, success, fallback);
    }
}