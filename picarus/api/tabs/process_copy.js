function render_process_copy() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    row_selector($('#rowPrefixDrop2'));
    $('#runButton').click(function () {
        button_running();
        var imageColumn = 'data:image';
        var columnName = $('#columnName').val();
        var columnValue = $('#columnValue').val();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        var prefix = $('#rowPrefixDrop2 option:selected').val();
        var maxRows = Number($('#maxRows').val());
        function success(row, columns) {
            // Generate row key
            var cur_row = prefix + random_bytes(10);
            cur_data = {};
            cur_data[imageColumn] = columns[imageColumn];
            if (columnName.length)
                cur_data[columnName] = columnValue;
            PICARUS.patchRow("images", cur_row, {data: cur_data});
        }
        // Scan through rows, each one write back to the prefix
        PICARUS.scanner("images", startRow, stopRow, {success: success, done: button_reset, fail: button_error, maxRows: maxRows, maxRowsIter: 5, columns: [imageColumn]});
    });
}