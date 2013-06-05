function render_workflow_classifier() {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render');
            this.collection.bind('sync', this.render);
            this.render();
        },
        events: {'change #preprocess_select': 'renderPreprocessor',
                 'change #feature_select': 'renderFeature',
                 'change #classifier_select': 'renderClassifier',
                 'click #runButton': 'run'},
        run: function () {
            console.log('Click');
            var trainFrac = Number($('#trainFrac').val());
            var gtColumn = $('#gtColumn').val();
            var slices = slices_selector_get(true);
            var startMidStopRows = [];
            var slicesTodo = slices.length;
            console.log('TrainFrac: ' + trainFrac + ' GT Column: ' + gtColumn);
            _.each(slices, function (slice) {
                var startRow = base64.decode(slice[0]);
                var stopRow = base64.decode(slice[1]);
                var rows = [];
                function scanner_success(row, columns) {
                    rows.push(row);
                }
                function scanner_done(data) {
                    var trainInd = Math.min(rows.length - 1, Math.round(trainFrac * rows.length));
                    var midRow = rows[trainInd];
                    if (trainInd) {
                        startMidStopRows.push([startRow, midRow, stopRow]);
                        console.log('trainInd: ' + trainInd + ' rows: ' + rows.length);
                    }
                    slicesTodo -= 1;
                    if (!slicesTodo) {
                        console.log(startMidStopRows);
                        var slicesData = _.map(startMidStopRows, function (x) {
                            return {startRow: x[0], midRow: x[1], stopRow: x[2], thumbnail: '-', preprocessor: '-', feature: '-'};
                        });
                        var template = "<table><tr><th>trainStart</th><th>trainStop/valStart</th><th>valStop</th><th>Thumb</th><th>Preproc</th><th>Feat</th></tr>{{#slices}}<tr><td>{{startRow}}</td><td>{{midRow}}</td><td>{{stopRow}}</td><td>{{thumbnail}}</td><td>{{preprocessor}}</td><td>{{feature}}</td></tr>{{/slices}}</table>"
                        function r() {
                            $('#progressTable').html(Mustache.render(template, {slices: slicesData}));
                        }
                        r();
                        function runThumbnails() {
                            _.each(slicesData, function (data) {
                                PICARUS.postSlice('images', data.startRow, data.stopRow, {data: {action: 'io/thumbnail'},
                                                                                          success: _.partial(watchJob, {done: function () {data.thumbnail = 'Done';r()}})});
                            });
                        }
                        runThumbnails();
                        
                        function runPreprocess(modelPreprocessor) {
                            _.each(slicesData, function (data) {
                                PICARUS.postSlice('images', data.startRow, data.stopRow, {success:  _.partial(watchJob, {done: function () {data.preprocessor = 'Done';r()}}),
                                                                                          data: {action: 'io/link', model: modelPreprocessor}});
                            });
                        }
                    }
                }
                PICARUS.scanner('images', startRow, stopRow, {success: scanner_success, done: scanner_done, columns: [gtColumn]})
            });
        },
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
            var names = PARAMETERS.map(function (x) {return {name: x.get('name'), row: x.get('row')}});
            function filterNames(whiteList) {
                return _.filter(names, function (x) {
                    return _.contains(whiteList, x.name);
                });
            }
            var preprocessors = filterNames(['picarus.ImagePreprocessor']);
            var features = filterNames(['bovw', 'picarus.GISTImageFeature', 'picarus.HistogramImageFeature']);
            var classifiers = filterNames(['svmlinear', 'svmkernel']);
            var select_template = "{{#models}}<option value='{{row}}'>{{name}}</option>{{/models}};"
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
}