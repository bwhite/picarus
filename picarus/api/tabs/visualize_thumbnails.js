function render_visualize_thumbnails() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var imageColumn = 'thum:image_150sq';
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        $('#results').html('');
        function success(row, columns) {
            c = columns;
            if (!_.has(columns, imageColumn))
                return;
            $('#results').append($('<img>').attr('src', 'data:image/jpeg;base64,' + base64.encode(columns[imageColumn])).attr('title', row))
        }
        var params = {success: success, maxRows: 100, columns: [imageColumn]};
        var filter = unescape($('#filter').val());
        if (filter.length > 0) {
            params.filter = filter;
        }
        PICARUS.scanner("images", startRow, stopRow, params)
    });
}