function render_visualize_exif() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var max_size = Number($('#maxSize').val());
        var exif_column = 'meta:exif';
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        images = new PicarusRows([], {'table': 'images'});
        function done() {
            $('#results').html('');
            if (!images.length)
                return;
            // TODO: Change to use RowsView
            var AppView = Backbone.View.extend({
                initialize: function() {
                    _.bindAll(this, 'render');
                    this.collection.bind('reset', this.render);
                    this.collection.bind('change', this.render);
                    this.collection.bind('add', this.render);
                },
                render: function() {
                    var cur_images = this.collection.filter(function (x) {return x.get(exif_column) != '{}' && !_.isUndefined(x.get(exif_column))});
                    columns = _.uniq(_.flatten(_.map(cur_images, function (x) {
                        return _.keys(JSON.parse(x.get(exif_column)));
                    }))).concat(['row']);
                    picarus_table = new Backbone.Table({
                        collection: this.collection,
                        columns: _.map(columns, function (v) {
                            if (v === "row")
                                return [v, v];
                            return {header: v, getFormatted: function() {
                                var cur_exif = JSON.parse(this.get(exif_column));
                                var out = cur_exif[v];
                                if (typeof out !== 'undefined') {
                                    if (!_.isString(out))
                                        return _.escape(JSON.stringify(out));
                                    out = base64.decode(out);
                                    if (typeof out.length <= max_size)
                                        return _.escape(out);
                                    else
                                        return '<span style="color:red">' + _.escape(out.slice(0, max_size)) + '</span>'
                                }
                            }};
                        })
                    });
                    this.$el.html(picarus_table.render().el);
                }
            });
            av = new AppView({collection: images, el: $('#results')});
            av.render();
        }
        function success(row, columns) {
            columns.row = row;
            if (columns[exif_column] != '{}')
                images.add(columns);
        }
        var params = {success: success, maxRows: 1000, done: done, columns: [exif_column]};
        PICARUS.scanner("images", startRow, stopRow, params)
    });
}