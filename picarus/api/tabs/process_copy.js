function render_process_copy() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    row_selector($('#rowPrefixDrop2'));
    $('#runButton').click(function () {
        button_running();
        var imageColumn = encode_id('data:image');
        var columnName = encode_id($('#columnName').val());
        var columnValue = $('#columnValue').val();
        var startRow = encode_id($('#startRow').val());
        var stopRow = encode_id($('#stopRow').val());
        var prefix = $('#rowPrefixDrop2 option:selected').val();
        var maxRows = Number($('#maxRows').val());
        function success(row, columns) {
            // Generate row key
            var cur_row = encode_id(prefix + random_bytes(10));
            cur_data = {};
            cur_data[imageColumn] = columns[imageColumn];
            if (columnName.length)
                cur_data[columnName] = base64.encode(columnValue);
            picarus_api_row("images", cur_row, "PATCH", {data: cur_data});
        }
        // Scan through rows, each one write back to the prefix
        picarus_api_data_scanner("images", startRow, stopRow, [imageColumn], {success: success, done: button_reset, fail: button_error, maxRows: maxRows, maxRowsIter: 5});
    });
}