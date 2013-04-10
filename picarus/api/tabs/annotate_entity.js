function render_annotate_entity() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        var startRow = encode_id($('#startRow').val());
        var stopRow = encode_id($('#stopRow').val());
        var imageColumn = encode_id('thum:image_150sq');
        var numTasks = Number($('#num_tasks').val());
        var entityColumn = encode_id($('#entity').val());
        function success(xhr) {
            response = JSON.parse(xhr.responseText);
            $('#results').append($('<a>').attr('href', '/a1/annotate/' + response.task + '/index.html').text('Worker').attr('target', '_blank'));
        }
        picarus_api("/a1/slice/images/" + startRow + '/' + stopRow, "POST", {success: success, data: {action: 'io/annotate/image/entity', imageColumn: imageColumn, entityColumn: entityColumn, instructions: $('#instructions').val(), numTasks: numTasks, mode: "amt"}});
    });
}