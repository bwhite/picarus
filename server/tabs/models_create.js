function render_models_create() {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'renderKind');
            _.bindAll(this, 'renderName');
            this.collection.bind('reset', this.renderKind);
            this.collection.bind('change', this.renderKind);
            this.collection.bind('add', this.renderKind);
            this.renderKind();
        },
        events: {'change #kind_select': 'renderName',
                 'change #name_select': 'renderParam'},
        renderParam: function () {
            $('#params').html('');
            $('#slices_select').html('');
            var model_kind = $('#kind_select option:selected').val();
            var name = $('#name_select option:selected').val();
            model_create_selector($('#slices_select'), $('#params'), model_kind, name);
        },
        renderKind: function() {
            var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};"
            var models_filt = _.uniq(_.map(this.collection.models, function (data) {return data.escape('kind')}));
            if (!models_filt.length)
                return;
            $('#kind_select').html(Mustache.render(select_template, {models: models_filt}));
            this.renderName();
        },
        renderName: function () {
            var model_kind = $('#kind_select option:selected').val();
            var cur_models = this.collection.filter(function (x) { return x.escape('kind') == model_kind});
            var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};"
            var models_filt = _.map(cur_models, function (data) {return data.escape('name')});
            $('#name_select').html(Mustache.render(select_template, {models: models_filt}));
            this.renderParam();
        }
    });
    av = new AppView({collection: PARAMETERS, el: $('#selects')});
    $('#runButton').click(function () {
        var params = model_create_selector_get($('#params'));
        function success(response) {
            var row = response.row;
            if (_.isUndefined(row))
                row = response.modelRow;
            var model = new PicarusRow({row: row}, {table: 'models', columns: ['meta:']});
            MODELS.add(model);
            model.fetch();
            $('#results').html(response.row);
            button_reset();
        }
        var model_kind = $('#kind_select option:selected').val();
        var name = $('#name_select option:selected').val();
        var model = PARAMETERS.filter(function (x) {
            if (x.escape('kind') == model_kind && x.escape('name') == name)
                return true;
        })[0];
        var path = model.get('row');
        params.path = path;
        if (model.escape('type') === 'factory') {
            params.table = 'images';
            params.slices = slices_selector_get().join(';');
            p = params;
            PICARUS.postTable('models', {success: _.partial(watchJob, {success: _.partial(updateJobStatus, $('#results')), done: success}), data: params});
        } else {
            PICARUS.postTable('models', {success: success, data: params});
        }
    });
}