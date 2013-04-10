function render_process_garbage() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        button_running();
        var startRow = encode_id($('#startRow').val());
        var stopRow = encode_id($('#stopRow').val());
        function success(xhr) {
            response = JSON.parse(xhr.responseText);
            button_reset();
            _.each(response.columns, function (x) {
                $('#results').append(x + '<br>');
            });
        }
        picarus_api("/a1/slice/images/" + startRow + '/' + stopRow, "POST", {success: button_reset, fail: button_error, data: {action: 'io/garbage'}});
    });
}