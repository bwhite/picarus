function render_models_create() {
    results = new PicarusRows([], {'table': 'parameters'});
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'renderKind');
            _.bindAll(this, 'renderName');
            this.collection.bind('reset', this.renderKind);
            this.collection.bind('change', this.renderKind);
            this.collection.bind('add', this.renderKind);
        },
        events: {'change #kind_select': 'renderName',
                 'change #name_select': 'renderParam'},
        renderParam: function () {
            $('#params').html('');
            $('#slices_select').html('');
            var model_kind = $('#kind_select option:selected').val();
            var name = $('#name_select option:selected').val();
            model = results.filter(function (x) {
                if (x.pescape('kind') == model_kind && x.pescape('name') == name)
                    return true;
            })[0];

            function add_param_selections(params, param_prefix) {
                _.each(params, function (value, key) {
                    var cur_el;
                    if (value.type == 'enum') {
                        var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};"
                        cur_el = $('<select>').attr('name', param_prefix + key).html(Mustache.render(select_template, {models: value.values}));
                    } else if (value.type == 'int') {
                        // TODO: Client-side data validation
                        cur_el = $('<input>').attr('name', param_prefix + key).attr('type', 'text').addClass('input-medium');
                    } else if (value.type == 'float') {
                        // TODO: Client-side data validation
                        cur_el = $('<input>').attr('name', param_prefix + key).attr('type', 'text').addClass('input-medium');
                    } else if (value.type == 'int_list') {
                        // Create as many input boxes as the min # of boxes
                        cur_el = $('<input>').attr('type', 'text').addClass('input-medium').val(value.min_size);
                        var box_func = function () {
                            $("[name^=" + param_prefix + key +  "]").remove();
                            _.each(_.range(Number(cur_el.val())), function (x) {
                                var cur_el_num = $('<input>').attr('name', param_prefix + key + ':' + x).attr('type', 'text').addClass('input-mini');
                                $('#params').append(cur_el_num);
                                add_hint(cur_el_num, key + ':' + x);
                            });
                        }
                        box_func();
                        cur_el.change(box_func);
                    } else if (value.type == 'str') {
                        // TODO: Client-side data validation
                        cur_el = $('<input>').attr('name', param_prefix + key).attr('type', 'text').addClass('input-medium');
                    }
                    if (typeof cur_el !== 'undefined') {
                        $('#params').append(cur_el);
                        add_hint(cur_el, key);
                    }
                });
            }
            add_param_selections(model.pescapejs('params'), 'param-');
            if (model.pescape('data') === 'slices') {
                $('#slices_select').append(document.getElementById('bpl_slices_select').innerHTML);
                slices_selector();
            }
            var inputs;
            if (model.pescape('type') == 'model')
                inputs = [model.pescape('input_type')];
            else
                inputs = model.pescapejs('input_types');
            _.each(inputs, function (value) {
                var cur_el;
                var cur_id = _.uniqueId('model_select_');          
                if (value === 'raw_image') {
                    $('#params').append($('<input>').attr('name', 'input-' + value).attr('type', 'hidden').val(encode_id('data:image')));
                } else if (value === 'meta') {
                    var cur_id = _.uniqueId('model_select_');
                    var el = $('<input>').attr('id', cur_id).attr('name', 'input-' +  value).attr('type', 'text').addClass('input-medium');
                    $('#params').append(el);
                    add_hint(el, 'Metadata column (e.g., meta:class)');
                } else {
                    $('#params').append($('<select>').attr('id', cur_id).attr('name', 'input-' + value).addClass('input-medium'));
                    model_dropdown({modelFilter: function (x) {return x.pescape('meta:output_type') === value},
                                    change: function() {},
                                    el: $('#' + cur_id)});
                }
            });
        },
        renderKind: function() {
            var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};"
            var models_filt = _.uniq(_.map(this.collection.models, function (data) {return data.pescape('kind')}));
            $('#kind_select').html(Mustache.render(select_template, {models: models_filt}));
            this.renderName();
        },
        renderName: function () {
            var model_kind = $('#kind_select option:selected').val();
            var cur_models = this.collection.filter(function (x) { return x.pescape('kind') == model_kind});
            var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};"
            var models_filt = _.map(cur_models, function (data) {return data.pescape('name')});
            $('#name_select').html(Mustache.render(select_template, {models: models_filt}));
            this.renderParam();
        }
    });
    av = new AppView({collection: results, el: $('#selects')});
    results.fetch();
    $('#runButton').click(function () {
        var params = _.object($('#params :input').map(function () {return [[$(this).attr('name'), $(this).val()]]}));
        if (!_.isUndefined(params['input-meta']))
            params['input-meta'] = encode_id(params['input-meta']);
        function success(xhr) {
            response = JSON.parse(xhr.responseText);
            $('#results').html(response.row);
        }
        var model_kind = $('#kind_select option:selected').val();
        var name = $('#name_select option:selected').val();
        var model = results.filter(function (x) {
            if (x.pescape('kind') == model_kind && x.pescape('name') == name)
                return true;
        })[0];
        var path = model.get('row');
        params.path = decode_id(path);
        if (model.pescape('type') === 'factory') {
            params.table = 'images';
            params.slices = slices_selector_get().join(',');
            p = params;
            picarus_api("/a1/data/models", "POST", {success: success, data: params});
        } else {
            picarus_api("/a1/data/models", "POST", {success: success, data: params});
        }
    });
}