function render_visualize_thumbnails() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        function uninstallScroll() {
            $(window).unbind("scroll");
            $(window).off('scroll.infinite resize.infinite');
        }
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var imageColumn = 'thum:image_150sq';
        var getMoreData = undefined;
        var hasMoreData = true;
        var gimmeMoreData = false; // 
        uninstallScroll();
        $('#results').html('');
        var $el = $('<div>');
        $('#results').append($el);
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        function success(row, columns) {
            c = columns;
            console.log(row);
            if (!_.has(columns, imageColumn))
                return;
            console.log(row);
            $el.append($('<img>').attr('src', 'data:image/jpeg;base64,' + base64.encode(columns[imageColumn])).attr('title', base64.encode(row)));
        }
        function done() {
            hasMoreData = false;
        }
        function resume(callback) {
            console.log('Got resume');
            if (gimmeMoreData) {
                gimmeMoreData = false;
                callback();
            } else
                getMoreData = callback;
        }
        var params = {success: success, columns: [imageColumn], resume: resume};
        $el.infiniteScroll({threshold: 1024, onEnd: function () {
            console.log('No more results');
        }, onBottom: function (callback) {
            if (!jQuery.contains(document.documentElement, $el[0])) {
                uninstallScroll();
                return;
            }
            console.log('More data!');
            if (hasMoreData)
                if (!_.isUndefined(getMoreData)) {
                    var more = getMoreData;
                    getMoreData = undefined;
                    more();
                } else {
                    gimmeMoreData = true;
                }
            callback(hasMoreData);
        }});
        PICARUS.scanner("images", startRow, stopRow, params);
    });
}