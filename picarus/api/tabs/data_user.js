function render_data_user() {
    users = new Picarus2Rows([], {'table': 'users'});
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.collection.bind('reset', this.render);
            this.collection.bind('change', this.render);
        },
        render: function() {
            var columns = _.uniq(_.flatten(_.map(this.collection.models, function (x) {
                return _.keys(x.attributes);
            })));
            picarus_table = new Backbone.Table({
                collection: this.collection,
                columns: _.map(columns, function (x) {
                    if (x === 'row')
                        return {header: 'email', getFormatted: function() {return this.escape(x)}};
                    return {header: x, getFormatted: function() {return this.escape(x)}};
                })
            });
            this.$el.html(picarus_table.render().el);
        }
    });
    new AppView({collection: users, el: $('#users')});
    login_get(function (email_auth) {
        var user = new Picarus2Row({row: email_auth.email});
        users.add(user);
        user.fetch();
        
    });
}