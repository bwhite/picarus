function render_data_projects() {
    slices_selector();
    $('#modifyProjectButton').click(function () {
        var row = $('#globalDataTableDrop option:selected').val();
        var data = {};
        var slices = slices_selector_get(true);
        var value = _.map(slices, function (x) {return x[0] + ',' + x[1]}).join(';');
        data[$('#projectName').val()] = value;
        PROJECTS.get(row).save(data, {patch: true});
    });
    var tableColumn = {header: "Table", getFormatted: function() {
        return this.escape('row');
    }};
    new RowsView({collection: PROJECTS, el: $('#prefixes'), extraColumns: [tableColumn], deleteValues: true});
}