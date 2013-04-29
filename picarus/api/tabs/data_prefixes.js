function render_data_prefixes() {
    function prefixChange() {
        var row = $('#globalDataTableDrop option:selected').val();
        var prefix_drop = $('#prefixDrop option:selected').val();
        if (_.isUndefined(row) || _.isUndefined(prefix_drop)) {
            $('#permissions').html('');
            return;
        }
        var permissions = PREFIXES.get(row).get(decode_id(prefix_drop));
        ps = permissions;
        var perms = ['r'];
        if (permissions == 'rw')
            perms = ['rw', 'r'];
        var select_template = "{{#prefixes}}<option value='{{value}}'>{{text}}</option>{{/prefixes}};"
        $('#permissions').html(Mustache.render(select_template, {prefixes: _.map(perms, function (x) {return {text: x, value: encode_id(x)}})}));
    }
    function change() {
        var row = $('#globalDataTableDrop option:selected').val();
        if (_.isUndefined(row)) {
            $('#prefixDrop').html('');
            prefixChange();
            return;
        }
        var prefixes = [];
        var table_prefixes = PREFIXES.get(row);
        if (_.isUndefined(table_prefixes)) {
            $('#prefixDrop').html('');
            prefixChange();
            return;
        }
        _.each(table_prefixes.attributes, function (val, key) {
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
    $('#globalDataTableDrop').change(change);
    $('#createButton').click(function () {
        var row = $('#globalDataTableDrop option:selected').val();
        if (_.isUndefined(row)) {
            return;
        }
        var data = {};
        data[decode_id($('#prefixDrop option:selected').val()) + unescape($('#suffix').val())] = decode_id($('#permissions option:selected').val());
        PREFIXES.get(row).save(data, {patch: true});
    });
    new RowsView({collection: PREFIXES, el: $('#prefixes'), deleteValues: true, postRender: change});
}