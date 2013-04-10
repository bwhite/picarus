function render_data_projects() {
    rows = new PicarusRows([], {'table': 'projects'});
    rows_dropdown(rows, {el: $('#prefixTable'), text: function (x) {return x.pescaperow()}});
    slices_selector();
    $('#modifyProjectButton').click(function () {
        var row = $('#prefixTable option:selected').val();
        var data = {};
        var slices = slices_selector_get(true);
        var value = _.map(slices, function (x) {return x[0] + '/' + x[1]}).join(',');
        data[$('#projectName').val()] = value;
        rows.get(row).psave(data, {patch: true});
    });
    var tableColumn = {header: "Table", getFormatted: function() {
        return _.escape(base64.decode(this.get('row')));
    }};
    new RowsView({collection: rows, el: $('#prefixes'), extraColumns: [tableColumn], deleteValues: true});
    rows.fetch();
}