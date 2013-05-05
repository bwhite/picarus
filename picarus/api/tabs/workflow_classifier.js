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
            var preprocessors = PARAMETERS.filter(function (x) {
                return _.contains(['preprocessor'], x.get('name'));
            });
            var features = PARAMETERS.filter(function (x) {
                return _.contains(['bovw', 'picarus.GISTImageFeature', 'picarus.HistogramImageFeature'], x.get('name'));
            });
            var classifiers = PARAMETERS.filter(function (x) {
                return _.contains(['svmlinear', 'svmkernel'], x.get('name'));
            });
            var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};" // text is escaped already
            $('#preprocess_select').html(Mustache.render(select_template, {models: _.pluck(preprocessors, 'name')}));
            $('#feature_select').html(Mustache.render(select_template, {models: _.pluck(features, 'name')}));
            $('#classifier_select').html(Mustache.render(select_template, {models: _.pluck(classifiers, 'name')}));
            slices_selector();
            this.renderPreprocessor();
            this.renderFeature();
            this.renderClassifier();
        }
    });
    new AppView({collection: PARAMETERS, el: $('#params')});
}