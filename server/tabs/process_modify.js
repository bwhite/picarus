function render_process_modify() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var columnName = unescape($('#columnName').val());
        var columnValue = unescape($('#columnValue').val());
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var data = {};
        data[columnName] = columnValue;
        PICARUS.patchSlice('images', startRow, stopRow, {success: button_reset, fail: button_error, data: data})
    });
}