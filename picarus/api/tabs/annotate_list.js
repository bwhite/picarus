function render_annotate_list() {
    results = new Picarus2Rows([], {'table': 'annotations'});
    var workerColumn = {header: "Worker", getFormatted: function() {
        return Mustache.render("<a href='/a1/annotate/{{task}}/index.html' target='_blank'>Worker</a>", {task: this.escape('task')});
    }};
    function postRender() {
    }
    new RowsView({collection: results, el: $('#annotations'), extraColumns: [workerColumn], postRender: postRender, deleteRows: true});
    results.fetch();
}