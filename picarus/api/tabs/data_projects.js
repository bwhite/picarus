function render_data_projects() {
    prefixes_selector();
    $('#modifyProjectButton').click(function () {
        var row = $('#globalDataTableDrop option:selected').val();
        var data = {};
        var value = slices_selector_get(true).join(',');
        var project = $('#projectName').val();
        if (project === '')
            return;
        data[project] = value;
        PROJECTS.get(row).save(data, {patch: true});
    });
    var tableColumn = {header: "Table", getFormatted: function() {
        return this.escape('row');
    }};
    new RowsView({collection: PROJECTS, el: $('#prefixes'), extraColumns: [tableColumn], deleteValues: true});
}