function login_get(func) {
    var otp = $('#otp');
    var apiKey = $('#apiKey');
    var modal = $('#authModal');
    var emailKeys = $('#emailKeys');
    emailKeys.click(function () {
        var email = $('#email').val();
        var loginKey = $('#loginKey').val();
        PICARUS.setAuth(email, loginKey);
        PICARUS.authEmailAPIKey();
    });
    if (typeof EMAIL_AUTH === 'undefined') {
        function get_auth() {
            function success(response) {
                PICARUS.setAuth(email, response.apiKey);
                use_api(response.apiKey);
            }
            function fail() {
                $('#secondFactorAuth').addClass('error');
            }
            var otp_val = otp.val();
            var email = $('#email').val();
            var loginKey = $('#loginKey').val();
            PICARUS.setAuth(email, loginKey);
            PICARUS.authYubikey(otp_val, {success: success, fail: fail});
        }
        function get_api() {
            var email = $('#email').val();
            var apiKey = $('#apiKey').val();
            function success() {
                use_api(apiKey);
            }
            function fail() {
                $('#secondFactorAuth').addClass('error');
            }
            $('#secondFactorAuth').addClass('info');
            $('#secondFactorAuth').removeClass('error');
            PICARUS.setAuth(email, apiKey);
            PICARUS.getTable('prefixes', {success: success, fail: fail});
        }
        function use_api(apiKey) {
            var email = $('#email').val();
            var loginKey = $('#loginKey').val();
            $('#secondFactorAuth').removeClass('error');
            // NOTE: Removed secure attribute since this
            // information isn't strictly secret (can only be used to send you an email an hour)
            // This makes using a demo http version much nicer, to add back use {secure: true} below
            $.cookie('email', email);
            $.cookie('loginKey', loginKey);
            EMAIL_AUTH = {auth: apiKey, email: email};
            $('#otp').unbind();
            $('#apiKey').unbind('keypress');
            func(EMAIL_AUTH);
            modal.modal('hide');
        }
        function enable_inputs() {
            var email = $('#email').val();
            var loginKey = $('#loginKey').val();
            if (email.length && loginKey.length) {
                otp.removeAttr("disabled");
                apiKey.removeAttr("disabled");
                emailKeys.removeAttr("disabled");
            }
        }
        $('#email').val($.cookie('email'));
        $('#loginKey').val($.cookie('loginKey'));
        enable_inputs();
        $('#email').keypress(enable_inputs);
        $('#email').on('paste', function () {_.defer(enable_inputs)});
        $('#loginKey').keypress(enable_inputs);
        $('#loginKey').on('paste', function () {_.defer(enable_inputs)});
        otp.keypress(_.debounce(get_auth, 100));
        otp.on('paste', function () {_.defer(get_auth)});
        apiKey.keypress(_.debounce(get_api, 100));
        apiKey.on('paste', function () {_.defer(get_api)});
        modal.modal('show');
        modal.off('shown');
        modal.on('shown', function () {otp.focus()});
    } else {
        func(EMAIL_AUTH);
    }
}

function google_visualization_load(callback) {
    google.load("visualization", "1", {packages:["corechart"], callback: callback});
}

function add_hint(el, text) {
    el.wrap($('<span>').attr('class', 'hint hint--bottom').attr('data-hint', text));
}
function random_bytes(num) {
    return _.map(_.range(10), function () {
        return String.fromCharCode(_.random(255));
    }).join('');
}

function imageThumbnail(row, id) {
    var imageColumn = 'thum:image_150sq';
    function success(columns) {
        $('#' + id).attr('src', 'data:image/jpeg;base64,' + base64.encode(columns[imageColumn])).attr('title', row)
    }
    PICARUS.getRow('images', row, {success: success, data: {columns: [imageColumn]}});
}

function button_confirm_click(button, fun) {
    button.unbind();
    button.click(function (data) {
        var button = $(data.target);
        button.unbind();
        button.addClass('btn-danger');
        button.click(fun);
    });
}
function button_confirm_click_reset(button) {
    button.removeClass('btn-danger');
    button.unbind();
}

function progressModal() {
    $('#progressModal').modal('show');
    function update(pct) {
        $('#progress').css('width', (100 * pct + '%'));
    }
    function done() {
        $('#progressModal').modal('hide');
    }
    return {done: done, update: update};
}

function alert_running() {
    $('#results').html('<div class="alert alert-info"><strong>Running!</strong> Job is running, please wait...</div>');
}

function alert_done() {
    $('#results').html('<div class="alert alert-success"><strong>Done!</strong> Job is done.</div>');
}

function alert_running_wrap(el) {
    return function () {
        el.html('<div class="alert alert-info"><strong>Running!</strong> Job is running, please wait...</div>');
    }
}

function alert_success_wrap(el) {
    return function () {
        el.html('<div class="alert alert-success"><strong>Done!</strong> Job is done.</div>');
    }
}

function alert_fail_wrap(el) {
    return function () {
        el.html('<div class="alert alert-error"><strong>Error!</strong> Job failed!</div>');
    }
}

function wrap_hints() {
    $('[hint]').each(function (x) {
        $(this).wrap($('<span>').attr('class', 'hint hint--bottom').attr('data-hint', $(this).attr('hint')));
    });
}

function button_running() {
    $('#runButton').button('loading');
}

function updateJobStatus($el, data, pollData) {
    if (!$.contains(document.documentElement, $el[0]))
        return;
    var goodRows = 0;
    var badRows = 0;
    var status = '';
    if (_.has(pollData, 'goodRows'))
        goodRows = Number(pollData.goodRows);
    if (_.has(pollData, 'badRows'))
        badRows = Number(pollData.badRows);
    if (_.has(pollData, 'status'))
        status = pollData.status;
    $el.html('');
    if (status || goodRows + badRows) {
        var pie = $('<span>', {'data-diameter': '60', 'class': 'pie', 'data-colours': '["green", "red"]'}).text(goodRows + ',' + badRows);
        $el.append(pie);
        pie.peity("pie");
        $el.append('Good[' + goodRows + '] Bad[' + badRows + '] Status[' + _.escape(status) + '] Row[' + _.escape(data.row) + ']');
    }
    if (pollData.status == 'completed' || pollData.status == 'failed')
        return;
}

function watchJob(options, data) {
    function pollJobsStatus() {
        PICARUS.getRow(data.table, data.row, {success: function (pollData) {
            JOBS.add(_.extend(pollData, {row: data.row}), {merge: true});
            if (!_.isUndefined(options.success))
                options.success(data, pollData);
            if (pollData.status != 'completed' && pollData.status != 'failed')
                _.delay(pollJobsStatus, 1000);
            if (pollData.status == 'completed' && !_.isUndefined(options.done))
                options.done();
        }, fail: function () {
            console.log('Poll Failed');
        }});
    }
    pollJobsStatus();
}

function button_reset() {
    $('#runButton').button('reset');
}

function button_error() {
    $('#runButton').button('error');
}

function decode_projects(x) {
    var projects = x.get('meta:projects');
    if (_.isUndefined(projects))
        return [];
    return _.map(projects.split(','), function (y) {return base64.decode(y)})
}

function model_dropdown(args) {
    var columns_model = ['meta:'];
    if (typeof args.change === 'undefined') {
        args.change = function () {};
    }
    var AppView = Backbone.View.extend({
        el: $('#container'),
        initialize: function() {
            _.bindAll(this, 'render');
            this.$projects = $('#globalProjectDrop');
            this.$projects.change(this.render);
            this.collection.bind('sync', this.render);
            this.render();
        },
        renderDrop: args.change,
        modelFilter: function (x) {
            var curProject = $('#globalProjectDrop').val();
            var modelProjects = decode_projects(x);
            if (curProject === '' || _.contains(modelProjects, curProject))
                return args.modelFilter(x);
            return false;
        },
        events: {'change': 'renderDrop'},
        render: function() {
            n = this.$el;
            this.$el.empty();
            var select_template = "{{#models}}<option value='{{row}}'>{{{text}}}</option>{{/models}};" // text is escaped already
            var models_filt = _.map(MODELS.filter(this.modelFilter), function (data) {return {row: encode_id(data.get('row')), text: data.escape('meta:tags') + ' ' + data.escape('meta:name')}});
            models_filt.sort(function (x, y) {return Number(x.text > y.text) - Number(x.text < y.text)});
            this.$el.append(Mustache.render(select_template, {models: models_filt}));
            this.renderDrop();
        }
    });
    av = new AppView({collection: MODELS, el: args.el});
    return MODELS;
}

function rows_dropdown(rows, args) {
    if (_.isUndefined(args.change)) {
        args.change = function () {};
    }
    if (_.isUndefined(args.filter)) {
        args.filter = function () {return true};
    }
    if (_.isUndefined(args.text)) {
        args.text = function (x) {return x.escape('row')};
    }
    var AppView = Backbone.View.extend({
        el: $('#container'),
        initialize: function() {
            _.bindAll(this, 'render');
            this.collection.bind('sync', this.render);
            this.render();
        },
        events: {'change': 'renderDrop'},
        renderDrop: args.change,
        render: function() {
            n = this.$el;
            this.$el.empty();
            var select_template = "{{#models}}<option value='{{row}}'>{{text}}</option>{{/models}};"
            var models_filt = _.map(rows.filter(args.filter), function (data) {return {row: encode_id(data.get('row')), text: args.text(data)}});
            models_filt.sort(function (x, y) {return Number(x.text > y.text) - Number(x.text < y.text)});
            this.$el.append(Mustache.render(select_template, {models: models_filt}));
            this.renderDrop();
        }
    });
    av = new AppView({collection: rows, el: args.el});
}

function project_selector() {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.$projects = $('#globalProjectDrop');
            this.collection.bind('sync', this.render);
            this.render();
        },
        events: {'change': 'renderDrop'},
        renderDrop: function() {
            this.$projects.empty();
            var projects = this.collection.get(this.$el.val());
            if (_.isUndefined(projects))
                return;
            projects = [''].concat(_.keys(_.omit(projects.attributes, 'row')));
            var select_template = "{{#projects}}<option value='{{.}}'>{{.}}</option>{{/projects}};";
            this.$projects.append(Mustache.render(select_template, {projects: projects}));
            this.$projects.trigger('change');
        },
        render: function() {
            this.$el.empty();
            var tables = this.collection.pluck('row');
            if (!tables.length)
                return;
            var select_template = "{{#tables}}<option value='{{.}}'>{{.}}</option>{{/tables}};"
            this.$el.append(Mustache.render(select_template, {tables: tables}));
            this.$el.trigger('change');
            this.renderDrop();
        }
    });
    new AppView({collection: PROJECTS, el: $('#globalDataTableDrop')});
}

function row_selector(prefixDrop, args) {
    if (_.isUndefined(args))
        args = {};
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.collection.bind('sync', this.render);
            this.$tables = $('#globalDataTableDrop');
            this.$projects = $('#globalProjectDrop');
            this.$tables.change(this.render);  // TODO: Hack
            this.$projects.change(this.render);
            this.postRender = function () {};
            if (!_.isUndefined(args.postRender))
                this.postRender = args.postRender;
            this.render();
        },
        events: {'change': 'renderDrop'},
        renderDrop: function () {
            var prefix = prefixDrop.children().filter('option:selected').val();
            if (typeof args.startRow !== 'undefined')
                args.startRow.val(prefix);
            // TODO: Assumes that prefix is not empty and that the last character is not 0xff (it would overflow)
            if (typeof args.stopRow !== 'undefined')
                args.stopRow.val(prefix_to_stop_row(prefix));
        },
        render: function() {
            this.$el.empty();
            // TODO: Check permissions and accept perissions as argument
            var project = this.$projects.val();
            prefixes = this.collection.get(this.$tables.val());
            projects = PROJECTS.get(this.$tables.val());
            if (_.isUndefined(prefixes))
                return;
            var prefixes = _.keys(_.omit(prefixes.attributes, 'row'));
            if (!_.isUndefined(project) && project !== '') {
                var table_project = PROJECTS.get(this.$tables.val()).get(project);
                var table_prefixes = _.map(table_project.split(','), function (x) {
                    return base64.decode(x);
                });
                prefixes = _.intersection(prefixes, table_prefixes);
            }
            prefixes.sort(function (x, y) {return Number(x > y) - Number(x < y)});
            var select_template = "{{#prefixes}}<option value='{{.}}'>{{.}}</option>{{/prefixes}};"
            this.$el.append(Mustache.render(select_template, {prefixes: prefixes}));
            this.postRender();
            this.renderDrop();
        }
    });
    new AppView({collection: PREFIXES, el: prefixDrop});
}

function slices_selector() {
    var prefixDrop = $('#slicesSelectorPrefixDrop'), startRow = $('#slicesSelectorStartRow'), stopRow = $('#slicesSelectorStopRow');
    var addButton = $('#slicesSelectorAddButton'), clearButton = $('#slicesSelectorClearButton'), slicesText = $('#slicesSelectorSlices');
    function clear() {
        slicesText.html('');
    }
    if (!prefixDrop.size())  // Skip if not visible
        return;
    row_selector(prefixDrop, {startRow: startRow, stopRow: stopRow, postRender: clear});
    addButton.click(function () {
        slicesText.append($('<option>').text(_.escape(startRow.val()) + '/' + _.escape(stopRow.val())).attr('value', base64.encode(unescape(startRow.val())) + ',' + base64.encode(unescape(stopRow.val()))));
    });
    clearButton.click(clear);
}

function model_create_selector($slicesSelect, $params, modelKind, name, hideInputs) {
    model = PARAMETERS.filter(function (x) {
        if (x.escape('kind') == modelKind && x.escape('name') == name)
            return true;
    })[0];
    if (_.isUndefined(model))
        return;
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
                        $params.append(cur_el_num);
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
                $params.append(cur_el);
                add_hint(cur_el, key);
            }
        });
    }
    add_param_selections(JSON.parse(model.get('params')), 'param-');
    if (model.escape('data') === 'slices') {
        if (!hideInputs) {
            $slicesSelect.append(document.getElementById('bpl_slices_select').innerHTML);
            slices_selector();
        }
    }
    if (!hideInputs) {
        var inputs;
        if (model.escape('type') == 'model')
            inputs = [model.escape('input_type')];
        else
            inputs = JSON.parse(model.get('input_types'));
        _.each(inputs, function (value) {
            var cur_el;
            var cur_id = _.uniqueId('model_select_');          
            if (value === 'raw_image') {
                $params.append($('<input>').attr('name', 'input-' + value).attr('type', 'hidden').val('data:image'));
            } else if (value === 'meta') {
                var cur_id = _.uniqueId('model_select_');
                var el = $('<input>').attr('id', cur_id).attr('name', 'input-' +  value).attr('type', 'text').addClass('input-medium');
                $params.append(el);
                add_hint(el, 'Metadata column (e.g., meta:class)');
            } else {
                $params.append($('<select>').attr('id', cur_id).attr('name', 'input-' + value).addClass('input-medium'));
                model_dropdown({modelFilter: function (x) {return x.escape('meta:output_type') === value},
                                change: function() {},
                                el: $('#' + cur_id)});
            }
        });
    }
}

function model_create_selector_get($params) {
    return _.object($params.find(':input[name]').map(function () {
        var k = $(this).attr('name');
        var v = $(this).val();
        if (_.isUndefined(k))
            return;
        if (k.slice(0, 5) === 'input' && k != 'input-meta' && k != 'input-raw_image')
            return [[k, decode_id(v)]];
        return [[k, v]];
    }));
}

function prefixes_selector() {
    var prefixDrop = $('#slicesSelectorPrefixDrop');
    var addButton = $('#slicesSelectorAddButton'), clearButton = $('#slicesSelectorClearButton'), slicesText = $('#slicesSelectorSlices');
    function clear() {
        slicesText.html('');
    }
    if (!prefixDrop.size())  // Skip if not visible
        return;
    row_selector(prefixDrop, {postRender: clear});
    addButton.click(function () {
        slicesText.append($('<option>').text(prefixDrop.children().filter('option:selected').val()).attr('value', base64.encode(prefixDrop.children().filter('option:selected').val())));
    });
    clearButton.click(clear);
}

function slices_selector_get(split) {
    var out = _.map($('#slicesSelectorSlices').children(), function (x) {return $(x).attr('value')});
    if (split)
        return _.map(out, function (x) {
            return x.split(',');
        });
    return out;
}

function prefixes_selector_get() {
    var out = _.map($('#slicesSelectorSlices').children(), function (x) {return $(x).attr('value')});
    return out;
}

function app_main() {
    PICARUS = new PicarusClient();
    // Setup models
    function param_encode(dd) {
        return _.map(dd, function (v) {
            return v.join('=');
        }).join('&');
    }
    PicarusRow = Backbone.Model.extend({
        idAttribute: "row",
        initialize: function(attributes, options) {
            if (!_.isUndefined(options)) {
                if (_.has(options, 'table'))
                    this.table = options.table;
                if (_.isArray(options.columns))
                    this.columns = options.columns;
            }
        },
        sync: function (method, model, options) {
            opt = options;
            console.log('row:' + method);
            mod = model;
            var table = model.get_table();
            var out;
            var success = options.success;
            var params = {success: success};
            params.data = model.attributes;
            if (_.has(options, 'attrs')) {
                params.data = options.attrs;
            }
            if (method == 'read') {
                if (_.has(this, 'columns'))
                    params.columns = this.columns;
                out = PICARUS.getRow(table, model.id, params);
            } else if (method == 'delete') {
                out = PICARUS.deleteRow(table, model.id, params);
            } else if (method == 'patch') {
                out = PICARUS.patchRow(table, model.id, params);
            } else if (method == 'create') {
                out = PICARUS.postTable(table, params);
            }
            debug_out = out;
            model.trigger('request', model, out, options);
            return out;
        },
        get_table: function () {
            var table = this.table;
            if (_.isUndefined(table))
                table = this.collection.table;
            return table;
        },
        unset: function (attr, options) {
            function s() {
                return this.set(attr, void 0, _.extend({}, options, {unset: true}));
            }
            s = _.bind(s, this);
            return PICARUS.deleteColumn(this.get_table(), this.id, attr, {success: s});
        }
    });
    PicarusRows = Backbone.Collection.extend({
        model : PicarusRow,
        initialize: function(models, options) {
            this.table = options.table;
            if (_.isArray(options.columns))
                this.columns = options.columns;
        },
        sync: function (method, model, options) {
            opt = options;
            console.log('rows:' + method);
            mod = model;
            var out;
            var params = {};
            var table = this.table;
            if (_.has(options, 'attrs'))
                params.data = options.attrs;
            if (method == 'read') {
                if (_.has(this, 'columns'))
                    params.columns = this.columns;
                params.success = function (lod) {
                    options.success(_.map(lod, function (v) {v[1].row = v[0]; return v[1]}));
                };
                out = PICARUS.getTable(this.table, params);
            }
            model.trigger('request', model, out, options);
            return out;
        }
    });


    function deleteValueFunc(row, column) {
        if (column == 'row')
            return '';
        return Mustache.render('<a class="value_delete" style="padding-left: 5px" row="{{row}}" column="{{column}}">Delete</a>', {row: encode_id(row), column: encode_id(column)});
    }
    function deleteRowFunc(row) {
        return Mustache.render('<button class="btn row_delete" type="submit" row="{{row}}"">Delete</button>', {row: encode_id(row)});
    }

    RowsView = Backbone.View.extend({
        initialize: function(options) {
            _.bindAll(this, 'render', 'renderWait');
            this.collection.bind('add', this.renderWait);
            this.collection.bind('sync', this.render);
            this.collection.bind('reset', this.render);
            this.collection.bind('change', this.renderWait);
            this.collection.bind('remove', this.renderWait);
            this.collection.bind('destroy', this.renderWait);
            this.extraColumns = [];
            this.postRender = function () {};
            this.filter = function (x) {return true};
            this.deleteValues = false;
            this.deleteRows = false;
            if (!_.isUndefined(options.postRender))
                this.postRender = options.postRender;
            if (!_.isUndefined(options.filter))
                this.filter = options.filter;
            if (!_.isUndefined(options.extraColumns))
                this.extraColumns = options.extraColumns;
            if (options.deleteRows) {
                this.deleteRows = true;
                function delete_row(data) {
                    var row = decode_id(data.target.getAttribute('row'));
                    this.collection.get(row).destroy({wait: true});
                }
                delete_row = _.bind(delete_row, this);
                this.postRender = _.compose(this.postRender, function () {
                    button_confirm_click($('.row_delete'), delete_row);
                });
                this.extraColumns.push({header: "Delete", getFormatted: function() { return deleteRowFunc(this.get('row'))}});
            }
            if (options.deleteValues) {
                this.deleteValues = true;
                function delete_value(data) {
                    var row = decode_id(data.target.getAttribute('row'));
                    var column = decode_id(data.target.getAttribute('column'));
                    this.collection.get(row).unset(column);
                }
                delete_value = _.bind(delete_value, this);
                this.postRender = _.compose(this.postRender, function () {
                    button_confirm_click($('.value_delete'), delete_value);
                });
            }
            if (options.columns)
                this.columns = options.columns;
            this.renderWait();
        },
        renderWait: _.debounce(function () {this.render()}, 5),
        render: function() {
            console.log('Rendering!');
            var columns = this.columns;
            if (_.isUndefined(columns))
                columns = _.uniq(_.flatten(_.map(this.collection.models, function (x) {
                    return _.keys(x.attributes);
                })));
            var deleteValueFuncLocal = function () {return ''};
            if (this.deleteValues)
                deleteValueFuncLocal = deleteValueFunc;
            var table_columns = _.map(columns, function (x) {
                if (x === 'row')
                    return {header: 'row', getFormatted: function() { return _.escape(this.get(x))}};
                outExtra = '';
                return {header: x, getFormatted: function() {
                    var val = this.get(x);
                    if (_.isUndefined(val))
                        return '';
                    return _.escape(val) + deleteValueFuncLocal(this.get('row'), x);
                }
                };
            }).concat(this.extraColumns);
            picarus_table = new Backbone.Table({
                collection: new PicarusRows(this.collection.filter(this.filter), {'table': 'models', columns: ['meta:']}),
                columns: table_columns
            });
            if (this.collection.length) {
                this.$el.html(picarus_table.render().el);
                this.postRender();
            } else {
                this.$el.html('<div class="alert alert-info">Table Empty</div>');
            }
        }
    });

    // Based on: https://gist.github.com/2711454
    var all_view = _.map($('#tpls [id*=tpl]'), function (v) {
        return v.id.slice(4).split('_').join('/')
    });

    function capFirst(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    //This is the Backbone controller that manages the content of the app
    var Content = Backbone.View.extend({
        initialize:function(options){
            Backbone.history.on('route',function(source, path){
                this.render(path);
            }, this);
        },
        //This object defines the content for each of the routes in the application
        content: _.object(_.map(all_view, function (val) {
            var selector_id;
            var prefix = 'tpl_';
            if (val === "") {
                selector_id = "data_user"
            } else {
                selector_id = val.split('/').join('_');
            }
            return [val, _.template(document.getElementById(prefix + selector_id).innerHTML, {baseLogin: document.getElementById('bpl_login').innerHTML,
                                                                                              rowSelect: document.getElementById('bpl_row_select').innerHTML,
                                                                                              slicesSelect: document.getElementById('bpl_slices_select').innerHTML,
                                                                                              prefixesSelect: document.getElementById('bpl_prefixes_select').innerHTML,
                                                                                              filter: document.getElementById('bpl_filter').innerHTML,
                                                                                              prefixSelect: document.getElementById('bpl_prefix_select').innerHTML,
                                                                                              runButton: document.getElementById('bpl_run_button').innerHTML})];
        })),
        render:function(route){
            //Simply sets the content as appropriate
            this.$el.html(this.content[route]);
            // Post-process the DOM for Picarus specific helpers
            wrap_hints();
            // Handles post render javascript calls if available
            if (route === "")
                route = 'models/list';
            var func_name = 'render_' + route.split('/').join('_');
            if (window.hasOwnProperty(func_name))
                login_get(window[func_name]);
        }
    });
    
    //This is the Backbone controller that manages the Nav Bar
    var NavBar = Backbone.View.extend({
        initialize:function(options){
            Backbone.history.on('route',function(source, path){
                this.render(path);
            }, this);
        },
        //This is a collection of possible routes and their accompanying
        //user-friendly titles
        titles: _.object(_.map(all_view, function (val) {
            var name;
            if (val === "") {
                name = "user";
            } else {
                name = _.last(val.split('/', 2));
            }
            return [val, capFirst(name)];
        })),
        events:{
            'click a':function(source) {
                var hrefRslt = source.target.getAttribute('href');
                Backbone.history.navigate(hrefRslt, {trigger:true});
                //Cancel the regular event handling so that we won't actual change URLs
                //We are letting Backbone handle routing
                return false;
            }
        },
        //Each time the routes change, we refresh the navigation (dropdown magic by Brandyn)
        render:function(route){
            this.$el.empty();
            var template = _.template("<li class='<%=active%>'><a href='<%=url%>'><%=visible%></a></li>");
            var drop_template = _.template("<li class='dropdown' <%=active%>><a href='#' class='dropdown-toggle' data-toggle='dropdown'><%=prev_key%></a><ul class='dropdown-menu'><% _.each(vals, function(data) { %> <li class='<%=data[2]%>'><a href='#<%=data[0]%>'><%=data[1]%></a></li> <% }); %></ul></li>");
            var prev_els = [];
            var prev_key = undefined;
            var route_key = route.split('/', 2)[0]
            function flush_dropdown(el) {
                el.append(drop_template({prev_key: capFirst(prev_key), vals: prev_els, active: route_key === prev_key ? "class='active'" : ''}));
            }
            for (var key in this.titles) {
                var active = route === key ? 'active' : '';
                var key_splits = key.split('/', 2);
                var name = this.titles[key];
                if (typeof prev_key != 'undefined' && (prev_key != key_splits[0] || key_splits.length < 2)) {
                    flush_dropdown(this.$el);
                    prev_key = undefined;
                    prev_els = [];
                }
                // If a part of a dropdown, add to list, else add directly
                if (key_splits.length >= 2) {
                    prev_key = key_splits[0];
                    prev_els.push([key, name, active]);
                } else {
                    this.$el.append(template({url:'#' + key,visible:this.titles[key],active:active}));
                }
            }
            if (typeof prev_key != 'undefined') {
                flush_dropdown(this.$el);
            }
            $('.dropdown-toggle').dropdown()
        }
    });
    
    //Every time a Router is instantiated, the route is added
    //to a global Backbone.history object. Thus, this is just a
    //nice way of defining possible application states
    new (Backbone.Router.extend({
        routes: _.object(_.map(all_view, function (val) {
            return [val, val];
        }).concat([['*path', 'models/list']]))
    }));
    
    //Attach Backbone Views to existing HTML elements
    new NavBar({el:document.getElementById('nav-item-container')});
    new Content({el:document.getElementById('container')});
    
    login_get(app_main_postauth);
}

function refresh_models() {
    _.each([PROJECTS, PREFIXES, JOBS, PARAMETERS, MODELS, USAGE], function (x) {x.fetch()});
}

function app_main_postauth(email_auth) {
    PROJECTS = new PicarusRows([], {'table': 'projects'});
    PREFIXES = new PicarusRows([], {'table': 'prefixes'});
    JOBS = new PicarusRows([], {'table': 'jobs'});
    PARAMETERS = new PicarusRows([], {'table': 'parameters'});
    USAGE = new PicarusRows([], {'table': 'usage'});
    MODELS = new PicarusRows([], {'table': 'models', columns: ['meta:']});
    refresh_models();
    project_selector();
    //Start the app by setting kicking off the history behaviour.
    //We will get a routing event with the initial URL fragment
    Backbone.history.start();
    window.onbeforeunload = function() {return "Leaving Picarus..."};
}