function render_workflow_classifier() {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.collection.bind('sync', this.render);
            this.render();
        },
        events: {'change #preprocess_select': 'renderPreprocessor',
                 'change #feature_select': 'renderFeature',
                 'change #classifier_select': 'renderClassifier'},
        renderPreprocessor: function () {
            $('#params_preprocessor').html('');
            var name = $('#preprocess_select').val();
            if (_.isUndefined(name))
                return;
            model_create_selector($('#slices_select'), $('#params_preprocessor'), 'image_preprocessor', name, true);
        },
        renderFeature: function () {
            $('#params_feature').html('');
            var name = $('#feature_select').val();
            if (_.isUndefined(name))
                return;
            model_create_selector($('#slices_select'), $('#params_feature'), 'feature', name, true);
        },
        renderClassifier: function () {
            $('#params_classifier').html('');
            var name = $('#classifier_select').val();
            if (_.isUndefined(name))
                return;
            model_create_selector($('#slices_select'), $('#params_classifier'), 'classifier', name, true);
        },
        render: function() {
            $('#slices_select').html('');
            $('#slices_select').append(document.getElementById('bpl_slices_select').innerHTML);
            // NOTE(brandyn): Factory parameters needs more specification of output_type
            // as we can't do this automatically without it, for now it is hardcoded
            var names = PARAMETERS.pluck('name');
            var preprocessors = _.intersection(names, ['picarus.ImagePreprocessor']);
            var features = _.intersection(names, ['bovw', 'picarus.GISTImageFeature', 'picarus.HistogramImageFeature']);
            var classifiers = _.intersection(names, ['svmlinear', 'svmkernel']);
            var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};" // text is escaped already
            $('#preprocess_select').html(Mustache.render(select_template, {models: preprocessors}));
            $('#feature_select').html(Mustache.render(select_template, {models: features}));
            $('#classifier_select').html(Mustache.render(select_template, {models: classifiers}));
            slices_selector();
            this.renderPreprocessor();
            this.renderFeature();
            this.renderClassifier();
        }
    });
    new AppView({collection: PARAMETERS, el: $('#params')});
    alert('This tab is still being developed, it is currently non-functional')
}