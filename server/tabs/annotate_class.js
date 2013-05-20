function render_annotate_class() {
    slices_selector();
    $('#runButton').click(function () {
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        var imageColumn = 'thum:image_150sq';
        var numTasks = Number($('#num_tasks').val());
        var classColumn = $('#class').val();
        var mode = $('#modeSelect').val();
        function success(response) {
            ANNOTATIONS.fetch();
            $('#results').append($('<a>').attr('href', '/a1/annotate/' + response.task + '/index.html').text('Worker').attr('target', '_blank'));
        }
        PICARUS.postTable('annotations', {success: success, data: {path: 'images/class', slices: slices_selector_get().join(';'), imageColumn: imageColumn, classColumn: classColumn, instructions: $('#instructions').val(), numTasks: numTasks, mode: mode}});
    });
}