function render_process_modify() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        button_running();
        var columnName = encode_id($('#columnName').val());
        var columnValue = base64.encode($('#columnValue').val());
        var startRow = encode_id($('#startRow').val());
        var stopRow = encode_id($('#stopRow').val());
        var data = {};
        data[columnName] = columnValue;
        picarus_api("/a1/slice/images/" + startRow + '/' + stopRow, "PATCH", {success: button_reset, fail: button_error, data: data});
    });
}