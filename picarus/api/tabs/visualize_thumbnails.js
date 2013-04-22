function render_visualize_thumbnails() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var imageColumn = 'thum:image_150sq';
        var getMoreData = undefined;
        var hasMoreData = false;
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        $('#results').html('');
        function success(row, columns) {
            c = columns;
            console.log(row);
            if (!_.has(columns, imageColumn))
                return;
            console.log(row);
            $('#results').append($('<img>').attr('src', 'data:image/jpeg;base64,' + base64.encode(columns[imageColumn])).attr('title', row))
        }
        function done() {
            hasMoreData = false;
        }
        function resume(callback) {
            console.log('Resuming');
            getMoreData = callback;
        }
        var params = {success: success, columns: [imageColumn], resume: resume};
        var filter = unescape($('#filter').val());
        if (filter.length > 0) {
            params.filter = filter;
        }
        PICARUS.scanner("images", startRow, stopRow, params)
        $('#results').infiniteScroll({threshold, onEnd: function () {
            console.log('No more results');
        }, onBotton: function (callback) {
            console.log('More data!');
            if (hasMoreData && !_.isUndefined(getMoreData)) {
                var more = getMoreData;
                getMoreData = undefined;
                more();
            }
            callback(hasMoreData);
        }});
    });
}