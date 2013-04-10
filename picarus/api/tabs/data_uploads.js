function render_data_uploads(email_auth) {
    function success_user(xhr) {
        response = JSON.parse(xhr.responseText);

    }
    var AppView = Backbone.View.extend({
        el: $('#container'),
        initialize: function() {
            _.bindAll(this, 'render');
            this.model.bind('reset', this.render);
            this.model.bind('change', this.render);
        },
        render: function() {
            var startRow = _.unescape(this.model.pescape('upload_row_prefix'));
            var imageColumn = encode_id('thum:image_150sq');
            function success(row, columns) {
                //$('#images').append(escape(decode_id(row)));
                //$('#images').append($('<br>'));
                $('#images').append($('<img>').attr('src', 'data:image/jpeg;base64,' + columns[imageColumn]).attr('width', '150px'));
                //$('#images').append($('<br>'));
            }
            picarus_api_data_scanner("images", encode_id(startRow), encode_id(prefix_to_stop_row(startRow)), [imageColumn], {success: success, maxRows: 24});
        }
    });
    var model = new PicarusUser({row: encode_id(email_auth.email)});
    new AppView({ model: model });
    model.fetch();
    //picarus_api("/a1/data/users/" + encode_id(email_auth.email), "GET", {success: success_user});
}