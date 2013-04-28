function render_data_projects() {
    rows_dropdown(PROJECTS, {el: $('#prefixTable'), text: function (x) {return x.escape('row')}});
    slices_selector();
    $('#modifyProjectButton').click(function () {
        var row = decode_id($('#prefixTable option:selected').val());
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