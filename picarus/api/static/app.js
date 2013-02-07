function login_setup() {
    load_cookie($('#userEmail'), $('#userAuth'));
}

function login_get() {
    return {email: $('#userEmail').val(), auth: $('#userAuth').val()};
}

function model_dropdown(args) {
    models = new PicarusModels();
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
            var models_filt = _.map(models.filter(this.modelFilter), function (data) {return {row: data.get('row'), text: data.get('tags')}});
            this.$el.append(Mustache.render(select_template, {models: models_filt}));
            this.renderDrop();
        }
    });
    av = new AppView({collection: models, el: document.getElementById('model_select')});
    models.fetch();
}

function row_selector() {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.model.bind('reset', this.render);
            this.model.bind('change', this.render);
        },
        events: {'change': 'renderDrop'},
        renderDrop: function () {
            var prefix = $('#rowPrefixDrop option:selected').val();
            $('#startRow').val(prefix);
            // TODO: Assumes that prefix is not empty and that the last character is not 0xff (it would overflow)
            $('#stopRow').val(prefix_to_stop_row(prefix));
        },
        render: function() {
            this.$el.empty();
            var prefixes = _.keys(this.model.get('imagePrefixes')); // TODO: Check permissions and accept perissions as argument
            var select_template = "{{#prefixes}}<option value='{{.}}'>{{.}}</option>{{/prefixes}};"
            this.$el.append(Mustache.render(select_template, {prefixes: prefixes}));
            this.renderDrop();
        }
    });
    // TODO: Create standard way to get login, not using cookie
    var auth = load_cookie();
    user = new PicarusUser({email: auth.email});
    new AppView({model: user, el: $('#rowPrefixDrop')});
    user.fetch();
}

function app_main() {
    // Setup models
    PicarusModel = Backbone.Model.extend({
        idAttribute: "row",
        defaults : {
        },
 
        url : function() {
            return this.id ? '/a1/models/' + this.id : '/a1/models'; 
        } 
 
    });
    PicarusModels = Backbone.Collection.extend({
        model : PicarusModel,
        url : "/a1/models"
    });

    PicarusUser = Backbone.Model.extend({
        idAttribute: "email",
        defaults : {
        },
 
        url : function() {
            return this.id ? '/a1/users/' + this.id : '/a1/users'; 
        } 
 
    });
    PicarusUsers = Backbone.Collection.extend({
        model : PicarusUser,
        url : "/a1/users"
    });

    PicarusImage = Backbone.Model.extend({
        idAttribute: "row",
        defaults : {
        },
    });
    // TODO: We may want to add a few REST calls, not sure yet
    PicarusImages = Backbone.Collection.extend({
        model : PicarusImage
    });

    $.ajaxSetup({
        'beforeSend': function (xhr) {
            var args = load_cookie();
            xhr.setRequestHeader("Authorization", "Basic " + base64.encode(args.email + ":" + args.auth));
        }
    });

    // Based on: https://gist.github.com/2711454
    var all_view = _.map($('#tpls [id*=tpl]'), function (v) {
        if (v.id === 'tpl_home')
            return "";
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
                selector_id = "home"
            } else {
                selector_id = val.split('/').join('_');
            }
            return [val, _.template(document.getElementById(prefix + selector_id).innerHTML, {baseLogin: document.getElementById('bpl_login').innerHTML,
                                                                                              rowSelect: document.getElementById('bpl_row_select').innerHTML,
                                                                                              prefixSelect: document.getElementById('bpl_prefix_select').innerHTML})];
        })),
        render:function(route){
            //Simply sets the content as appropriate
            this.$el.html(this.content[route]);
            // Handles post render javascript calls if available
            if (route === "")
                route = 'home';
            var func_name = 'render_' + route.split('/').join('_');
            if (window.hasOwnProperty(func_name))
                window[func_name]();
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
                name = "home"
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
            var drop_template = _.template("<li class='dropdown <%=active%>'><a href='#' data-toggle='dropdown' class='dropdown-toggle'><%=prev_key%> <b class='caret'></b></a><ul class='dropdown-menu'><% _.each(vals, function(data) { %> <li class='<%=data[2]%>'><a href='#<%=data[0]%>' data-toggle='tab'><%=data[1]%></a></li> <% }); %></ul></li>");
            var prev_els = [];
            var prev_key = undefined;
            var route_key = route.split('/', 2)[0]
            function flush_dropdown(el) {
                el.append(drop_template({prev_key: capFirst(prev_key), vals: prev_els, active: route_key === prev_key ? 'active' : ''}));
            }
            for (var key in this.titles) {
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
                    prev_els.push([key, name, route === key ? 'active' : '']);
                } else {
                    this.$el.append(template({url:'#' + key,visible:this.titles[key],active:route === key ? 'active' : ''}));
                }
            }
            if (typeof prev_key != 'undefined') {
                flush_dropdown(this.$el);
            }
            $('.dropdown-toggle').dropdown();
        }
    });
    
    //Every time a Router is instantiated, the route is added
    //to a global Backbone.history object. Thus, this is just a
    //nice way of defining possible application states
    new (Backbone.Router.extend({
        routes: _.object(_.map(all_view, function (val) {
            return [val, val];
        }).concat([['*path', '']]))
    }));
    
    //Attach Backbone Views to existing HTML elements
    new NavBar({el:document.getElementById('nav-item-container')});
    new Content({el:document.getElementById('container')});
    
    //Start the app by setting kicking off the history behaviour.
    //We will get a routing event with the initial URL fragment
    Backbone.history.start();
}