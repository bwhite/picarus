function render_process_modify() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        button_running();
        var columnName = $('#columnName').val();
        var columnValue = $('#columnValue').val();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        var data = {};
        data[columnName] = columnValue;
        PICARUS.patchSlice('images', startRow, stopRow, {success: button_reset, fail: button_error, data: data})
    });
}