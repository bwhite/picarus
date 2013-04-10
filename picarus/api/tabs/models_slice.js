function render_models_slice() {
    model_dropdown({modelFilter: function (x) {return true},
                    el: $('#model_select')});
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        button_running();
        var startRow = encode_id(unescape($('#startRow').val()));
        var stopRow = encode_id(unescape($('#stopRow').val()));
        var action = 'io/link';
        if ($('#chainCheck').is(':checked'))
            action = 'io/chain';
        var data = {action: action, model: $('#model_select').find(":selected").val()};
        picarus_api("/a1/slice/images/" + startRow + '/' + stopRow, "POST", {success: button_reset, fail: button_error, data: data});
    });
}