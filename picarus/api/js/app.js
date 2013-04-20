function login_get(func) {
    var otp = $('#otp');
    var apiKey = $('#apiKey');
    var modal = $('#authModal');
    var emailKeys = $('#emailKeys');
    PICARUS = new PicarusClient();
    emailKeys.click(function () {
        var email = $('#email').val();
        var loginKey = $('#loginKey').val();
        PICARUS.authEmailAPIKey(email, loginKey);
    });
    if (typeof EMAIL_AUTH === 'undefined') {
        function get_auth() {
            function success(response) {
                $.ajaxSetup({'beforeSend': function (xhr) {
                    xhr.setRequestHeader("Authorization", "Basic " + base64.encode(email + ":" + response.apiKey));
                }});
                use_api(response.apiKey);
            }
            function fail() {
                $('#secondFactorAuth').addClass('error');
            }
            var otp_val = otp.val();
            var email = $('#email').val();
            var loginKey = $('#loginKey').val();
            $.ajaxSetup({'beforeSend': function (xhr) {
                xhr.setRequestHeader("Authorization", "Basic " + base64.encode(email + ":" + loginKey));
            }});
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
            $.ajaxSetup({'beforeSend': function (xhr) {
                xhr.setRequestHeader("Authorization", "Basic " + base64.encode(email + ":" + apiKey));
            }});
            PICARUS.getRow('users', email, {success: success, fail: fail});
        }
        function use_api(apiKey) {
            var email = $('#email').val();
            var loginKey = $('#loginKey').val();
            $('#secondFactorAuth').removeClass('error');
            $.cookie('email', email, {secure: true});
            $.cookie('loginKey', loginKey, {secure: true});
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
    PICARUS.getRow('images', row, {success: success, data: {columns: imageColumn}});
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

function button_reset() {
    $('#runButton').button('reset');
}

function button_error() {
    $('#runButton').button('error');
}

function model_dropdown(args) {
    var columns_model = ['meta:'];
    var models = new PicarusRows([], {'table': 'models', columns: columns_model});
    if (typeof args.change === 'undefined') {
        args.change = function () {};
    }
    var AppView = Backbone.View.extend({
        el: $('#container'),
        initialize: function() {
            _.bindAll(this, 'render');
            _.bindAll(this, 'renderDrop');
            this.$el.bind('reset', this.renderDrop);
            this.$el.bind('change', this.renderDrop);
            this.collection.bind('reset', this.render);
            this.collection.bind('change', this.render);
        },
        renderDrop: args.change,
        modelFilter: args.modelFilter,
        render: function() {
            n = this.$el;
            this.$el.empty();
            var select_template = "{{#models}}<option value='{{row}}'>{{{text}}}</option>{{/models}};" // text is escaped already
            var models_filt = _.map(models.filter(this.modelFilter), function (data) {return {row: encode_id(data.get('row')), text: data.escape('meta:tags') + ' ' + data.escape('meta:name')}});
            models_filt.sort(function (x, y) {return Number(x.text > y.text) - Number(x.text < y.text)});
            this.$el.append(Mustache.render(select_template, {models: models_filt}));
            this.renderDrop();
        }
    });
    av = new AppView({collection: models, el: args.el});
    models.fetch();
    return models;
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
            _.bindAll(this, 'renderDrop');
            this.$el.bind('reset', this.renderDrop);
            this.$el.bind('change', this.renderDrop);
            this.collection.bind('reset', this.render);
            this.collection.bind('change', this.render);
        },
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
    rows.fetch();
}


function project_selector(projectsDrop) {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.model.bind('reset', this.render);
            this.model.bind('change', this.render);
        },
        render: function() {
            this.$el.empty();
            var projects = _.keys(JSON.parse(this.model.get('image_projects')));
            projects.sort(function (x, y) {return Number(x > y) - Number(x < y)});
            var select_template = "{{#projects}}<option value='{{.}}'>{{.}}</option>{{/projects}};"
            this.$el.append(Mustache.render(select_template, {projects: projects}));
            this.renderDrop();
        }
    });
    var auth = login_get(function (email_auth) {
        user = new PicarusRow({row: email_auth.email}, {'table': 'users'});
        new AppView({model: user, el: projectsDrop});
        user.fetch();
    });
}

function row_selector(prefixDrop, startRow, stopRow) {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.model.bind('reset', this.render);
            this.model.bind('change', this.render);
        },
        events: {'change': 'renderDrop'},
        renderDrop: function () {
            var prefix = prefixDrop.children().filter('option:selected').val();
            if (typeof startRow !== 'undefined')
                startRow.val(prefix);
            // TODO: Assumes that prefix is not empty and that the last character is not 0xff (it would overflow)
            if (typeof stopRow !== 'undefined')
                stopRow.val(prefix_to_stop_row(prefix));
        },
        render: function() {
            this.$el.empty();
            // TODO: Check permissions and accept perissions as argument
            var prefixes = _.keys(JSON.parse(this.model.get('image_prefixes')));
            prefixes.sort(function (x, y) {return Number(x > y) - Number(x < y)});
            var select_template = "{{#prefixes}}<option value='{{.}}'>{{.}}</option>{{/prefixes}};"
            this.$el.append(Mustache.render(select_template, {prefixes: prefixes}));
            this.renderDrop();
        }
    });
    var auth = login_get(function (email_auth) {
        user = new PicarusRow({row: email_auth.email}, {'table': 'users'});
        new AppView({model: user, el: prefixDrop});
        user.fetch();
    });
}

function slices_selector() {
    var prefixDrop = $('#slicesSelectorPrefixDrop'), startRow = $('#slicesSelectorStartRow'), stopRow = $('#slicesSelectorStopRow');
    var addButton = $('#slicesSelectorAddButton'), clearButton = $('#slicesSelectorClearButton'), slicesText = $('#slicesSelectorSlices');
    if (!prefixDrop.size())  // Skip if not visible
        return;
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.model.bind('reset', this.render);
            this.model.bind('change', this.render);
        },
        events: {'change': 'renderDrop'},
        renderDrop: function () {
            var prefix = decode_id(prefixDrop.children().filter('option:selected').val());
            if (typeof startRow !== 'undefined')
                startRow.val(prefix);
            // TODO: Assumes that prefix is not empty and that the last character is not 0xff (it would overflow)
            if (typeof stopRow !== 'undefined')
                stopRow.val(prefix_to_stop_row(prefix));
        },
        render: function() {
            this.$el.empty();
            // TODO: Check permissions and accept perissions as argument
            var prefixes = _.keys(JSON.parse(this.model.get('image_prefixes')));
            prefixes.sort(function (x, y) {return Number(x > y) - Number(x < y)});
            var select_template = "{{#prefixes}}<option value='{{value}}'>{{text}}</option>{{/prefixes}};"
            var prefixes_render = _.map(prefixes, function (x) {return {value: encode_id(x), text: x}});
            this.$el.append(Mustache.render(select_template, {prefixes: prefixes_render}));
            this.renderDrop();
        }
    });
    addButton.click(function () {
        slicesText.append($('<option>').text(_.escape(startRow.val()) + '/' + _.escape(stopRow.val())).attr('value', encode_id(unescape(startRow.val())) + '/' + encode_id(unescape(stopRow.val()))));
    });
    clearButton.click(function () {
        slicesText.html('');
    });
    var auth = login_get(function (email_auth) {
        user = new PicarusRow({row: email_auth.email}, {'table': 'users'});
        new AppView({model: user, el: prefixDrop});
        user.fetch();
    });
}

function slices_selector_get(split) {
    var out = _.map($('#slicesSelectorSlices').children(), function (x) {return $(x).attr('value')});
    if (split)
        return _.map(out, function (x) {
            return x.split('/');
        });
    return out;
}

function app_main() {
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
            var success = function (x) {return options.success(model, x, options)};
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
            var success = function (x) {return options.success(model, x, options)};
            var params = {success: success};
            if (_.has(options, 'attrs'))
                params.data = options.attrs;
            if (method == 'read') {
                if (_.has(this, 'columns'))
                    params.columns = this.columns;
                params.success = function (lod) {
                    lod = _.map(lod, function (v) {
                        v[1].row = v[0];
                        return v[1];
                    });
                    success(lod);
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
            _.bindAll(this, 'render');
            this.collection.bind('reset', this.render);
            this.collection.bind('change', this.render);
            this.collection.bind('remove', this.render);
            this.collection.bind('destroy', this.render);
            this.extraColumns = [];
            this.postRender = function () {};
            this.deleteValues = false;
            this.deleteRows = false;
            if (!_.isUndefined(options.postRender))
                this.postRender = options.postRender;
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
        },
        render: function() {
            
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
                collection: this.collection,
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

    PicarusImage = Backbone.Model.extend({
        idAttribute: "row",
        defaults : {
        }
    });
    // TODO: We may want to add a few REST calls, not sure yet
    PicarusImages = Backbone.Collection.extend({
        model : PicarusImage,
        url : "/a1/users/images"
    });

    $.ajaxSetup({
        'beforeSend': function (xhr) {
            login_get(function (email_auth) {
                xhr.setRequestHeader("Authorization", "Basic " + base64.encode(email_auth.email + ":" + email_auth.auth));
            });
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
                                                                                              filter: document.getElementById('bpl_filter').innerHTML,
                                                                                              prefixSelect: document.getElementById('bpl_prefix_select').innerHTML,
                                                                                              runButton: document.getElementById('bpl_run_button').innerHTML})];
        })),
        render:function(route){
            //Simply sets the content as appropriate
            this.$el.html(this.content[route]);
            // Post-process the DOM for Picarus specific helpers
            wrap_hints();
            custom_checkbox_and_radio();
            // Handles post render javascript calls if available
            if (route === "")
                route = 'data/user';
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
            var drop_template = _.template("<li <%=active%>><a href='#'><%=prev_key%></a><ul><% _.each(vals, function(data) { %> <li class='<%=data[2]%>'><a href='#<%=data[0]%>'><%=data[1]%></a></li> <% }); %></ul></li>");
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
        }
    });
    
    //Every time a Router is instantiated, the route is added
    //to a global Backbone.history object. Thus, this is just a
    //nice way of defining possible application states
    new (Backbone.Router.extend({
        routes: _.object(_.map(all_view, function (val) {
            return [val, val];
        }).concat([['*path', 'data/user']]))
    }));
    
    //Attach Backbone Views to existing HTML elements
    new NavBar({el:document.getElementById('nav-item-container')});
    new Content({el:document.getElementById('container')});
    
    //Start the app by setting kicking off the history behaviour.
    //We will get a routing event with the initial URL fragment
    Backbone.history.start();
    window.onbeforeunload = function() {return "Leaving Picarus..."};
}