function render_annotate_batch() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        var startRow = encode_id($('#startRow').val());
        var stopRow = encode_id($('#stopRow').val());
        var imageColumn = encode_id('thum:image_150sq');
        var entityColumn = encode_id('meta:class');
        var numTasks = Number($('#num_tasks').val());
        var query = $('#query').val();
        function success(xhr) {
            response = JSON.parse(xhr.responseText);
            $('#results').append($('<a>').attr('href', '/a1/annotate/' + response.task + '/index.html').text('Worker').attr('target', '_blank'));
        }
        picarus_api("/a1/slice/images/" + startRow + '/' + stopRow, "POST", {success: success, data: {action: 'io/annotate/image/query_batch', imageColumn: imageColumn, query: query, instructions: $('#instructions').val(), numTasks: numTasks, mode: "amt"}});
    });
}