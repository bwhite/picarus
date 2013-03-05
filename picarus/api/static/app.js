function login_get(func) {
    var otp = $('#otp');
    var apiKey = $('#apiKey');
    var modal = $('#authModal');
    var emailKeys = $('#emailKeys');
    emailKeys.click(function () {
        var email = $('#email').val();
        var loginKey = $('#loginKey').val();
        picarus_api("/a1/auth/email", "POST", {email: email, auth: loginKey});
    });
    if (typeof EMAIL_AUTH === 'undefined') {
        function get_auth() {
            function success(xhr) {
                use_api(JSON.parse(xhr.responseText).apiKey);
            }
            function fail() {
                $('#secondFactorAuth').addClass('error');
            }
            var otp_val = otp.val();
            var email = $('#email').val();
            var loginKey = $('#loginKey').val();
            picarus_api("/a1/auth/yubikey", "POST", {data: {otp: otp_val}, success: success, email: email, auth: loginKey, fail: fail});
        }
        function get_api() {
            var email = $('#email').val();
            var apiKey = $('#apiKey').val();
            function success(xhr) {
                use_api(apiKey);
            }
            function fail() {
                $('#secondFactorAuth').addClass('error');
            }
            $('#secondFactorAuth').addClass('info');
            $('#secondFactorAuth').removeClass('error');
            picarus_api("/a1/users/" + encodeURIComponent(email), "GET", {success: success, email: email, auth: apiKey, fail: fail});
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

function model_dropdown(args) {
    var models = new PicarusModels();
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
            var select_template = "{{#models}}<option value='{{row}}'>{{text}}</option>{{/models}};"
            var models_filt = _.map(models.filter(this.modelFilter), function (data) {return {row: data.escape('row'), text: data.pescape('data:tags')}});
            this.$el.append(Mustache.render(select_template, {models: models_filt}));
            this.renderDrop();
        }
    });
    av = new AppView({collection: models, el: args.el});
    models.fetch();
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
            var prefixes = _.keys(this.model.pescapejs('image_prefixes'));
            var select_template = "{{#prefixes}}<option value='{{.}}'>{{.}}</option>{{/prefixes}};"
            this.$el.append(Mustache.render(select_template, {prefixes: prefixes}));
            this.renderDrop();
        }
    });
    var auth = login_get(function (email_auth) {
        user = new PicarusUser({row: encode_id(email_auth.email)});
        new AppView({model: user, el: prefixDrop});
        user.fetch();
    });
}

function app_main() {
    // Setup models
    function param_encode(dd) {
        return _.map(dd, function (v) {
            return v.join('=');
        }).join('&');
    }
    var modelParams = ['data:input', 'data:versions', 'data:prefix', 'data:creation_time', 'data:param', 'data:notes', 'data:name', 'data:tags'];
    modelParams = '?' + param_encode(_.map(modelParams, function (x) {
        return ['column', encode_id(x)];
    }));
    PicarusModel = Backbone.Model.extend({
        idAttribute: "row",
        defaults : {
        },
        url : function() {
            return this.id ? '/a1/data/models/' + this.id : '/a1/data/models' + modelParams; 
        },
        pescape: function (x) {
            return _.escape(base64.decode(this.escape(encode_id(x))));
        },
        pescapejs: function (x) {
            return JSON.parse(base64.decode(this.escape(encode_id(x))));
        },
        psave: function (attributes, options) {
            return this.save(object_ub64_b64_enc(attributes), options);
        }
    });
    PicarusModels = Backbone.Collection.extend({
        model : PicarusModel,
        url : function() {
            return '/a1/data/models' + modelParams; 
        }
    });

    PicarusParamModel = Backbone.Model.extend({
        idAttribute: "row",
        pescape: function (x) {
            return _.escape(base64.decode(this.escape(encode_id(x))));
        },
        pescapejs: function (x) {
            console.log(base64.decode(this.escape(encode_id(x))));
            return JSON.parse(base64.decode(this.escape(encode_id(x))));
        }
    });
    PicarusParamModels = Backbone.Collection.extend({
        model : PicarusParamModel,
        url : "/a1/data/parameters"
    });

    PicarusUser = Backbone.Model.extend({
        idAttribute: "row",
        defaults : {
        },
 
        url : function() {
            return this.id ? '/a1/data/users/' + this.id  : '/a1/data/users'; 
        },
        pescape: function (x) {
            return _.escape(base64.decode(this.escape(encode_id(x))));
        },
        pescapejs: function (x) {
            console.log(base64.decode(this.escape(encode_id(x))));
            return JSON.parse(base64.decode(this.escape(encode_id(x))));
        }
    });
    PicarusUsers = Backbone.Collection.extend({
        model : PicarusUser,
        url : "/a1/data/users"
    });

    PicarusImage = Backbone.Model.extend({
        idAttribute: "row",
        defaults : {
        },
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
                                                                                              filter: document.getElementById('bpl_filter').innerHTML,
                                                                                              prefixSelect: document.getElementById('bpl_prefix_select').innerHTML})];
        })),
        render:function(route){
            //Simply sets the content as appropriate
            this.$el.html(this.content[route]);
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