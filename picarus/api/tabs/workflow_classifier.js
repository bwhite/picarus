function render_workflow_classifier() {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.collection.bind('sync', this.render);
            this.render();
        },
        render: function() {
            $('#params_preprocessor').html('');
            $('#params_feature').html('');
            $('#params_classifier').html('');
            model_create_selector($('#slices_select'), $('#params_preprocessor'), 'image_preprocessor', 'picarus.ImagePreprocessor');
            model_create_selector($('#slices_select'), $('#params_feature'), 'feature', 'bovw');
            model_create_selector($('#slices_select'), $('#params_classifier'), 'classifier', 'svmkernel');
        }
    });
    new AppView({collection: PARAMETERS, el: $('#params')});
}