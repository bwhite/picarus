function render_visualize_thumbnails() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        var startRow = encode_id(unescape($('#startRow').val()));
        var stopRow = encode_id(unescape($('#stopRow').val()));
        var imageColumn = encode_id('thum:image_150sq');
        var metaCF = encode_id('meta:');
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        $('#results').html('');
        function success(row, columns) {
            c = columns;
            if (!_.has(columns, imageColumn))
                return;
            $('#results').append($('<img>').attr('src', 'data:image/jpeg;base64,' + columns[imageColumn]).attr('title', row))
            //$('#results').append($('<br>'));
        }
        var params = {success: success, maxRows: 100};
        var filter = unescape($('#filter').val());
        if (filter.length > 0) {
            params.filter = filter;
        }
        picarus_api_data_scanner("images", startRow, stopRow, [imageColumn, metaCF], params)
    });
}