function render_process_garbage() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        button_running();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        function success(xhr) {
            response = JSON.parse(xhr.responseText);
            button_reset();
            _.each(response.columns, function (x) {
                $('#results').append(x + '<br>');
            });
        }
        PICARUS.postSlice('images', startRow, stopRow, 'io/garbage', {success: button_reset, fail: button_error})
    });
}