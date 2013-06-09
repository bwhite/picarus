function render_workflow_classifier() {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'render', 'renderFeature', 'renderBovw');
            this.collection.bind('sync', this.render);
            this.render();
        },
        events: {'change #preprocess_select': 'renderPreprocessor',
                 'change #feature_select': 'renderFeature',
                 'change #bovw_select': 'renderBovw',
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
                    rows.push([row, columns[gtColumn]]);
                }
                function add_model(row) {
                    var model = new PicarusRow({row: row}, {table: 'models', columns: ['meta:']});
                    MODELS.add(model);
                    model.fetch();
                }
                function num_positive(rows) {
                    var posClass = $('input[name="param-class_positive"]').val();
                    return _.reduce(rows, function (x, y) {
                        return x + Number(y[1] === posClass);
                    }, 0);
                }
                function scanner_done(data) {
                    var trainInd = Math.min(rows.length - 1, Math.round(trainFrac * rows.length));
                    var midRow = rows[trainInd][0];
                    if (trainInd) {
                        startMidStopRows.push([startRow, midRow, stopRow, trainInd, rows.length - trainInd,
                                               num_positive(rows.slice(0, trainInd)), num_positive(rows.slice(trainInd))]);
                        console.log('trainInd: ' + trainInd + ' rows: ' + rows.length);
                    }
                    slicesTodo -= 1;
                    if (!slicesTodo) {
                        console.log(startMidStopRows);
                        var slicesData = _.map(startMidStopRows, function (x) {
                            return {startRow: x[0], midRow: x[1], stopRow: x[2], trainPos: x[5], valPos: x[6], trainNeg: x[3] - x[5], valNeg: x[4] - x[6], thumbnail: '-', preprocessor: '-', feature: '-', classifier: '-'};
                        });
                        var progressTemplate = "<table><tr><th>trainStart</th><th>trainStop/valStart</th><th>valStop</th><th>TrainPos/Neg</th><th>ValPos/Neg</th><th>Thumb</th><th>Preproc</th><th>Feat</th><th>Classify</th></tr>{{#slices}}<tr><td>{{startRow}}</td><td>{{midRow}}</td><td>{{stopRow}}</td><td>{{trainPos}}/{{trainNeg}}</td><td>{{valPos}}/{{valNeg}}</td><td><span class='label {{thumbnailClass}}'>{{thumbnail}}</span></td><td><span class='label {{preprocessorClass}}'>{{preprocessor}}</span></td><td><span class='label {{featureClass}}'>{{feature}}</span></td><td><span class='label {{classifierClass}}'>{{classifier}}</span></td></tr>{{/slices}}</table>"
                        var modelsTemplate = "<table><tr><th>Name</th><th>Row (b64)</th></tr>{{#models}}<tr><td>{{name}}</td><td>{{rowb64}}</td></tr>{{/models}}</table>";
                        var modelsData = [{name: 'preprocessor'}, {name: 'feature'}, {name: 'classifier'}];
                        function r() {
                            $('#progressTable').html(Mustache.render(progressTemplate, {slices: slicesData}));
                            $('#modelsTable').html(Mustache.render(modelsTemplate, {models: modelsData}));
                        }
                        r();
                        function runThumbnails() {
                            _.each(slicesData, function (data) {
                                data.thumbnail = 'Running';
                                data.thumbnailClass = 'label-info';
                                r();
                                PICARUS.postSlice('images', data.startRow, data.stopRow, {data: {action: 'io/thumbnail'},
                                                                                          success: _.partial(watchJob, {done: function () {data.thumbnailClass = 'label-success';data.thumbnail = 'Done';r()}})});
                            });
                        }
                        runThumbnails();
                        
                        function runPreprocess(modelPreprocessor) {
                            var preprocessTodo = slicesData.length;
                            _.each(slicesData, function (data) {
                                data.preprocessor = 'Running';
                                data.preprocessorClass = 'label-info';
                                r();
                                PICARUS.postSlice('images', data.startRow, data.stopRow, {success:  _.partial(watchJob, {done: function () {
                                    preprocessTodo -= 1;
                                    if (!preprocessTodo) {
                                        data.preprocessor = 'Done';
                                        data.preprocessorClass = 'label-success';
                                        r();
                                        createFeature(modelPreprocessor);
                                    }
                                }}),
                                                                                          data: {action: 'io/link', model: modelPreprocessor}});
                            });
                        }
                        function runFeature(modelFeature) {
                            var featureTodo = slicesData.length;
                            _.each(slicesData, function (data) {
                                data.feature = 'Running';
                                data.featureClass = 'label-info';
                                r();
                                PICARUS.postSlice('images', data.startRow, data.stopRow, {success:  _.partial(watchJob, {done: function () {
                                    featureTodo -= 1;
                                    if (!featureTodo) {
                                        data.feature = 'Done';
                                        data.featureClass = 'label-success';
                                        r();
                                        createClassifier(modelFeature);
                                    }
                                }}),
                                                                                          data: {action: 'io/link', model: modelFeature}});
                            });
                        }
                        function runClassifier(modelClassifier) {
                            var classifierTodo = slicesData.length;
                            _.each(slicesData, function (data) {
                                data.classifier = 'Running';
                                data.classifierClass = 'label-info';
                                r();
                                PICARUS.postSlice('images', data.midRow, data.stopRow, {success:  _.partial(watchJob, {done: function () {
                                    classifierTodo -= 1;
                                    if (!classifierTodo) {
                                        data.classifier = 'Done';
                                        data.classifierClass = 'label-success';
                                        r();
                                        alert('Workflow done');
                                    }
                                }}),
                                                                                          data: {action: 'io/link', model: modelClassifier}});
                            });
                        }
                        function createPreprocessor() {
                            var params = model_create_selector_get($('#params_preprocessor'));
                            params.path = $('#preprocess_select').find(":selected").val();
                            params['input-raw_image'] = 'data:image';
                            PICARUS.postTable('models', {success: function (x) {add_model(x.row);modelsData[0].rowb64=base64.encode(x.row);r();runPreprocess(x.row)}, data: params});
                        }
                        function createFeature(modelPreprocessor) {
                            var params = model_create_selector_get($('#params_feature'));
                            params.path = $('#feature_select').find(":selected").val();
                            if (!params.path)
                                return;
                            params['input-processed_image'] = modelPreprocessor;

                            PICARUS.postTable('models', {success: function (x) {
                                add_model(x.row);
                                modelsData[1].rowb64 = base64.encode(x.row);
                                r();
                                if (PARAMETERS.get(params.path).get('output_type') === 'feature') {
                                    runFeature(x.row);
                                } else {
                                    this.createBovw(x.row);
                                }
                            }, data: params});
                        }
                        function createBovw(modelMaskFeature) {
                            var params = model_create_selector_get($('#params_bovw'));
                            params.path = $('#bovw_select').find(":selected").val();
                            params['input-mask_feature'] = modelMaskFeature;
                            params.table = 'images';
                            params.slices = _.map(startMidStopRows, function (x) {
                                return base64.encode(x[0]) + ',' + base64.encode(x[1]);
                            }).join(';');
                            PICARUS.postTable('models', {success: _.partial(watchJob, {done: function (x) {
                                add_model(x.modelRow);
                                modelsData[1].rowb64 += '  ' + base64.encode(x.modelRow);
                                r();
                                runFeature(x.modelRow);
                            }}), data: params});
                        }
                        function createClassifier(modelFeature) {
                            var params = model_create_selector_get($('#params_classifier'));
                            params.path = $('#classifier_select').find(":selected").val();
                            params['input-feature'] = modelFeature;
                            params['input-meta'] = gtColumn;
                            params.table = 'images';
                            params.slices = _.map(startMidStopRows, function (x) {
                                return base64.encode(x[0]) + ',' + base64.encode(x[1]);
                            }).join(';');
                            debug_params = params;
                            PICARUS.postTable('models', {success:  _.partial(watchJob, {done: function (x) {
                                add_model(x.modelRow);
                                modelsData[2].rowb64=base64.encode(x.modelRow);r();
                                runClassifier(x.modelRow);
                            }}), data: params});
                        }
                        createPreprocessor();
                    }
                }
                PICARUS.scanner('images', startRow, stopRow, {success: scanner_success, done: scanner_done, columns: [gtColumn]})
            });
        },
        renderPreprocessor: function () {
            $('#params_preprocessor').html('');
            var name = $('#preprocess_select').find(":selected").text();
            if (_.isUndefined(name))
                return;
            model_create_selector($('#slices_select'), $('#params_preprocessor'), 'image_preprocessor', name, true);
        },
        renderFeature: function () {
            $('#params_feature').html('');
            var name = $('#feature_select').find(":selected").text();
            var path = $('#feature_select').find(":selected").val();
            if (!path)
                return;
            model_create_selector($('#slices_select'), $('#params_feature'), 'feature', name, true);
            if (PARAMETERS.get(path).get('output_type') === 'mask_feature') {
                $('#bovwSection').css('display', '')
                this.renderBovw();
            } else {
                $('#bovwSection').css('display', 'none');
            }
        },
        renderBovw: function () {
            $('#params_bovw').html('');
            var name = $('#bovw_select').find(":selected").text();
            if (_.isUndefined(name))
                return;
            model_create_selector($('#slices_select'), $('#params_bovw'), 'feature', name, true);
        },
        renderClassifier: function () {
            $('#params_classifier').html('');
            var name = $('#classifier_select').find(":selected").text();
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
            var features = filterNames(['picarus.HOGImageMaskFeature', 'picarus.GISTImageFeature', 'picarus.HistogramImageFeature']);
            var bovws = filterNames(['bovw']);
            var classifiers = filterNames(['svmlinear', 'svmkernel']);
            var select_template = "{{#models}}<option value='{{row}}'>{{name}}</option>{{/models}};"
            $('#preprocess_select').html(Mustache.render(select_template, {models: preprocessors}));
            $('#feature_select').html(Mustache.render(select_template, {models: features}));
            $('#bovw_select').html(Mustache.render(select_template, {models: bovws}));
            $('#classifier_select').html(Mustache.render(select_template, {models: classifiers}));
            slices_selector();
            this.renderPreprocessor();
            this.renderFeature();
            this.renderClassifier();
        }
    });
    new AppView({collection: PARAMETERS, el: $('#params')});
}