function render_process_exif() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        button_running();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        PICARUS.postSlice('images', startRow, stopRow, {data: {action: 'io/exif'}, success: button_reset, fail: button_error})
    });
}