function render_process_thumbnail() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        PICARUS.postSlice('images', startRow, stopRow, {data: {action: 'io/thumbnail'},
                                                        success: _.partial(watchJob, {success: _.partial(updateJobStatus, $('#success'))}), fail: button_error})
    });
}