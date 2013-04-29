function render_annotate_batch() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        var imageColumn = 'thum:image_150sq';
        var entityColumn = 'meta:class';
        var numTasks = Number($('#num_tasks').val());
        var query = $('#query').val();
        function success(response) {
            ANNOTATIONS.fetch();
            $('#results').append($('<a>').attr('href', '/a1/annotate/' + response.task + '/index.html').text('Worker').attr('target', '_blank'));
        }
        PICARUS.postSlice('images', startRow, stopRow, {success: success, data: {action: 'io/annotate/image/query_batch', imageColumn: imageColumn, query: query, instructions: $('#instructions').val(), numTasks: numTasks, mode: "amt"}});
    });
}