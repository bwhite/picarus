function render_visualize_metadata() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
    $('#runButton').click(function () {
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var max_size = Number($('#maxSize').val());
        var metaCF = 'meta:';
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        button_confirm_click_reset($('#removeButton'));
        // Setup table
        images = new PicarusRows();
        function remove_rows() {
            // TODO: Since there is a maxRows setting, this won't remove all rows, just the ones we have available
            var rows = _.map(images.models, function (x) {return x.id});
            picarus_api_delete_rows(rows, progressModal());
        }
        function done() {
            $('#results').html('');
            if (!images.length)
                return;
            var AppView = Backbone.View.extend({
                initialize: function() {
                    _.bindAll(this, 'render');
                    this.collection.bind('reset', this.render);
                    this.collection.bind('change', this.render);
                    this.collection.bind('add', this.render);
                },
                render: function() {
                    var columns = _.uniq(_.flatten(_.map(this.collection.models, function (x) {
                        return _.keys(x.attributes);
                    })));
                    picarus_table = new Backbone.Table({
                        collection: this.collection,
                        columns: _.map(columns, function (v) {
                            if (v === "row")
                                return [v, v];
                            return {header: v, getFormatted: function() {
                                var out = this.get(v);
                                if (typeof out !== 'undefined') {
                                    if (out.length <= max_size)
                                        return out;
                                    else
                                        return '<span style="color:red">' + out.slice(0, max_size) + '</span>'
                                }
                            }};
                        })
                    });
                    this.$el.html(picarus_table.render().el);
                }
            });
            av = new AppView({collection: images, el: $('#results')});
            av.render();
            $('#removeButton').removeAttr('disabled');
            button_confirm_click($('#removeButton'), remove_rows);
        }
        function success(row, columns) {
            columns.row = row;
            images.add(columns);
        }
        var params = {success: success, maxRows: 1000, done: done, columns: [metaCF]};
        var filter = unescape($('#filter').val());
        if (filter.length > 0) {
            params.filter = filter;
        }
        PICARUS.scanner("images", startRow, stopRow, params)
    });
}