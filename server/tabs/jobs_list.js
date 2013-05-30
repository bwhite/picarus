function render_jobs_list() {
    var workerColumn = {header: "Worker", getFormatted: function() {
        if (JOBS.get(this.get('row')).get('type') != 'annotation')
            return '';
        return Mustache.render("<a href='/v0/annotation/{{task}}/index.html' target='_blank'>Worker</a>", {task: this.escape('row')});
    }};
    var syncColumn = {header: "Sync", getFormatted: function() {
        if (JOBS.get(this.get('row')).get('type') != 'annotation')
            return '';
        return '<span style="font-size:5px"><a class="tasks-sync" row="' + encode_id(this.get('row')) + '">sync</a></span>';
    }};

    function postRender() {
        $('.tasks-sync').click(function (data) {
            var row = decode_id(data.target.getAttribute('row'));
            var model = JOBS.get(row);
            PICARUS.postRow('jobs', row, {data: {'action': 'io/annotation/sync'}});
        });
    }
    // TODO: Filter based on type == annotation
    new RowsView({collection: JOBS, el: $('#results'), extraColumns: [workerColumn, syncColumn], postRender: postRender, deleteRows: true});
    var $clearCompletedButton = $('#clearCompletedButton');
    button_confirm_click_reset($clearCompletedButton);
    button_confirm_click($clearCompletedButton, function () {
        _.map(JOBS.filter(function (x) {return x.get('status') == 'completed'}), function (x) {x.destroy({wait: true})});
        button_confirm_click_reset($clearCompletedButton);
    });
}