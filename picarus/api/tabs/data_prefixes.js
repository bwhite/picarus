function render_data_prefixes() {
    rows = new PicarusRows([], {'table': 'prefixes'});
    function prefixChange() {
        var row = $('#prefixTable option:selected').val();
        var prefix_drop $('#prefixDrop option:selected').val();
        if (_.isUndefined(row) || _.isUndefined(prefix_drop)) {
            $('#permissions').html('');
            return;
        }
        row = decode_id(row);
        var permissions = rows.get(row).get(decode_id(prefix_drop));
        ps = permissions;
        var perms = ['r'];
        if (permissions == 'rw')
            perms = ['rw', 'r'];
        var select_template = "{{#prefixes}}<option value='{{value}}'>{{text}}</option>{{/prefixes}};"
        $('#permissions').html(Mustache.render(select_template, {prefixes: _.map(perms, function (x) {return {text: x, value: encode_id(x)}})}));
    }
    function change() {
        var row = $('#prefixTable option:selected').val();
        if (_.isUndefined(row)) {
            $('#prefixDrop').html('');
            prefixChange();
            return;
        }
        row = decode_id(row);
        var prefixes = [];
        _.each(rows.get(row).attributes, function (val, key) {
            if (key == 'row') {
                return;
            }
            prefixes.push(key);
        });
        prefixes.sort();
        var select_template = "{{#prefixes}}<option value='{{value}}'>{{text}}</option>{{/prefixes}};"
        $('#prefixDrop').html(Mustache.render(select_template, {prefixes: _.map(prefixes, function (x) {return {text: x, value: encode_id(x)}})}));
        $('#prefixDrop').change(prefixChange); // TODO: Redo this in backbone
        prefixChange();
    }
    rows_dropdown(rows, {el: $('#prefixTable'), text: function (x) {return x.escape('row')}, change: change});
    $('#createButton').click(function () {
        var row = $('#prefixTable option:selected').val();
        if (_.isUndefined(row)) {
            return;
        }
        row = decode_id(row);
        var data = {}
        data[decode_id($('#prefixDrop option:selected').val()) + unescape($('#suffix').val())] = decode_id($('#permissions option:selected').val());
        rows.get(row).save(data, {patch: true});        
    });
    var tableColumn = {header: "Table", getFormatted: function() {
        return this.escape('row');
    }};
    new RowsView({collection: rows, el: $('#prefixes'), extraColumns: [tableColumn], deleteValues: true});
    rows.fetch();
}