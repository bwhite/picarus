function render_jobs_annotationQA() {
    slices_selector();
    $('#runButton').click(function () {
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var imageColumn = 'data:image';
        var numTasks = Number($('#num_tasks').val());
        var questionColumn = $('#question').val();
        var latitudeColumn = $('#latitude').val();
        var longitudeColumn = $('#longitude').val();
        var mode = $('#modeSelect').val();
        $('#results').html('');
        function success(response) {
            JOBS.fetch();
            $('#results').append($('<a>').attr('href', '/v0/annotation/' + response.row + '/index.html').text('Worker').attr('target', '_blank'));
        }
        PICARUS.postTable('jobs', {success: success, data: {path: 'annotation/images/qa', slices: slices_selector_get().join(';'), imageColumn: imageColumn, latitudeColumn: latitudeColumn,
                                                            longitudeColumn: longitudeColumn, questionColumn: questionColumn, instructions: $('#instructions').val(), numTasks: numTasks, mode: mode}});
    });
}