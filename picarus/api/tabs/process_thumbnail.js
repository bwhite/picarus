function render_process_thumbnail() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        button_running();
        var startRow = encode_id($('#startRow').val());
        var stopRow = encode_id($('#stopRow').val());
        picarus_api("/a1/slice/images/" + startRow + '/' + stopRow, "POST", {success: button_reset, fail: button_error, data: {action: 'io/thumbnail'}});
    });
}