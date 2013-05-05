function render_workflow_classifier() {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.collection.bind('sync', this.render);
            this.render();
        },
        render: function() {
            $('#slices_select').html('');
            $('#slices_select').append(document.getElementById('bpl_slices_select').innerHTML);
            slices_selector();
            $('#params_preprocessor').html('');
            $('#params_feature').html('');
            $('#params_classifier').html('');
            model_create_selector($('#slices_select'), $('#params_preprocessor'), 'image_preprocessor', 'picarus.ImagePreprocessor', true);
            model_create_selector($('#slices_select'), $('#params_feature'), 'feature', 'bovw', true);
            model_create_selector($('#slices_select'), $('#params_classifier'), 'classifier', 'svmkernel', true);
        }
    });
    new AppView({collection: PARAMETERS, el: $('#params')});
}