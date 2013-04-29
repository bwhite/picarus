function render_annotate_entity() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        var imageColumn = 'thum:image_150sq';
        var numTasks = Number($('#num_tasks').val());
        var entityColumn = $('#entity').val();
        function success(response) {
            ANNOTATIONS.fetch();
            $('#results').append($('<a>').attr('href', '/a1/annotate/' + response.task + '/index.html').text('Worker').attr('target', '_blank'));
        }
        PICARUS.postSlice('images', startRow, stopRow, {success: success, data: {action: 'io/annotate/image/entity', imageColumn: imageColumn, entityColumn: entityColumn, instructions: $('#instructions').val(), numTasks: numTasks, mode: "amt"}});
    });
}