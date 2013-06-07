function render_process_delete() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        PICARUS.deleteSlice('images', startRow, stopRow, {success: button_reset, fail: button_error})
    });
}