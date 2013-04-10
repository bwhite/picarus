function render_data_prefixes() {
    rows = new PicarusRows([], {'table': 'prefixes'});
    function prefixChange() {
        var row = $('#prefixTable option:selected').val();
        var permissions = rows.get(row).pescape($('#prefixDrop option:selected').val());
        ps = permissions;
        var perms = ['r'];
        if (permissions == 'rw')
            perms = ['rw', 'r'];
        var select_template = "{{#prefixes}}<option value='{{.}}'>{{.}}</option>{{/prefixes}};"
        $('#permissions').html(Mustache.render(select_template, {prefixes: perms}));
    }
    function change() {
        var row = $('#prefixTable option:selected').val();
        var prefixes = [];
        _.each(rows.get(row).attributes, function (val, key) {
            if (key == 'row')
                return;
            prefixes.push(decode_id(key));
        });
        prefixes.sort();
        var select_template = "{{#prefixes}}<option value='{{.}}'>{{.}}</option>{{/prefixes}};"
        $('#prefixDrop').html(Mustache.render(select_template, {prefixes: prefixes}));
        $('#prefixDrop').change(prefixChange); // TODO: Redo this in backbone
        prefixChange();
    }
    rows_dropdown(rows, {el: $('#prefixTable'), text: function (x) {return x.pescaperow()}, change: change});
    $('#createButton').click(function () {
        var row = $('#prefixTable option:selected').val();
        var data = {}
        data[$('#prefixDrop option:selected').val() + $('#suffix').val()] = $('#permissions option:selected').val(); 
        rows.get(row).psave(data, {patch: true});        
    });
    var tableColumn = {header: "Table", getFormatted: function() {
        return _.escape(base64.decode(this.get('row')));
    }};
    new RowsView({collection: rows, el: $('#prefixes'), extraColumns: [tableColumn], deleteValues: true});
    rows.fetch();
}