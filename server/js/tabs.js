function render_data_prefixes() {
    function prefixChange() {
        var row = $('#globalDataTableDrop option:selected').val();
        var prefix_drop = $('#prefixDrop option:selected').val();
        if (_.isUndefined(row) || _.isUndefined(prefix_drop)) {
            $('#permissions').html('');
            return;
        }
        var permissions = PREFIXES.get(row).get(decode_id(prefix_drop));
        ps = permissions;
        var perms = ['r'];
        if (permissions == 'rw')
            perms = ['rw', 'r'];
        var select_template = "{{#prefixes}}<option value='{{value}}'>{{text}}</option>{{/prefixes}};"
        $('#permissions').html(Mustache.render(select_template, {prefixes: _.map(perms, function (x) {return {text: x, value: encode_id(x)}})}));
    }
    function change() {
        var row = $('#globalDataTableDrop option:selected').val();
        if (_.isUndefined(row)) {
            $('#prefixDrop').html('');
            prefixChange();
            return;
        }
        var prefixes = [];
        var table_prefixes = PREFIXES.get(row);
        if (_.isUndefined(table_prefixes)) {
            $('#prefixDrop').html('');
            prefixChange();
            return;
        }
        _.each(table_prefixes.attributes, function (val, key) {
            if (key == 'row') {
                return;
            }
            prefixes.push(key);
        });
        prefixes.sort();
        var select_template = "{{#prefixes}}<option value='{{value}}'>{{text}}</option>{{/prefixes}};"
        $('#prefixDrop').html(Mustache.render(select_template, {prefixes: _.map(prefixes, function (x) {return {text: x, value: encode_id(x)}})}));
        $('#prefixDrop').change(prefixChange); // TODO: Redo this in backbone
        prefixChange();
    }
    $('#globalDataTableDrop').change(change);
    $('#createButton').click(function () {
        var row = $('#globalDataTableDrop option:selected').val();
        if (_.isUndefined(row)) {
            return;
        }
        var data = {};
        data[decode_id($('#prefixDrop option:selected').val()) + unescape($('#suffix').val())] = decode_id($('#permissions option:selected').val());
        PREFIXES.get(row).save(data, {patch: true});
    });
    new RowsView({collection: PREFIXES, el: $('#prefixes'), deleteValues: true, postRender: change});
}
function render_data_projects() {
    prefixes_selector();
    $('#modifyProjectButton').click(function () {
        var row = $('#globalDataTableDrop option:selected').val();
        var data = {};
        var value = slices_selector_get(true).join(',');
        var project = $('#projectName').val();
        if (project === '')
            return;
        data[project] = value;
        PROJECTS.get(row).save(data, {patch: true});
    });
    var tableColumn = {header: "Table", getFormatted: function() {
        return this.escape('row');
    }};
    new RowsView({collection: PROJECTS, el: $('#prefixes'), extraColumns: [tableColumn], deleteValues: true});
}
function render_data_usage() {
    new RowsView({collection: USAGE, el: $('#usage')});
}
function render_models_list() {
    var columns = ['meta:name', 'meta:input_type', 'meta:output_type', 'row', 'meta:creation_time', 'meta:input',
                   'meta:model_link_size', 'meta:model_chain_size', 'meta:factory_info'];

    var takeoutColumn = {header: "Takeout", getFormatted: function() {
        return Mustache.render("<a class='takeout_link' row='{{row}}'>Link</a>/<a class='takeout_chain' row='{{row}}'>Chain</a>", {row: encode_id(this.get('row'))});
    }};
    var tagsColumn = {header: "Tags", className: "models-tags", getFormatted: function() { return this.escape('meta:tags') + '<a class="modal_link_tags" row="' + encode_id(this.get('row')) + '">edit</a>'}};
    var notesColumn = {header: "Notes", className: "models-notes", getFormatted: function() { return this.escape('meta:notes') + '<a class="modal_link_notes" row="' + encode_id(this.get('row')) + '">edit</a>'}};
    var projectsColumn = {header: "Projects", className: "models-projects", getFormatted: function() { return _.escape(decode_projects(this).join(',')) + '<a class="modal_link_projects" row="' + encode_id(this.get('row')) + '">edit</a>'}};
    var rowB64Column = {header: "RowB64", getFormatted: function() { return base64.encode(this.get('row'))}};
    function postRender() {
        function process_takeout(row, model_chunks_column, model_column, model_type) {
            function takeoutSuccess(response) {
                 chunks = _.map(response, function (v, k) {
                    return [Number(k.split('-')[1]), v];
                }).sort();
                 model = _.map(chunks, function (v, k) {
                    return v[1];
                }).join('');
                var curSha1 = Sha1.hash(model, false);
                var trueSha1 = MODELS.get(row).escape('meta:model_' + model_type + '_sha1');
                if (curSha1 === trueSha1) {
                    var modelByteArray = new Uint8Array(model.length);
                    for (var i = 0; i < model.length; i++) {
                        modelByteArray[i] = model.charCodeAt(i) & 0xff;
                    }
                    var blob = new Blob([modelByteArray]);
                    saveAs(blob, 'picarus-model-' + encode_id(row) + '.sha1-' +  trueSha1 + '.' + model_type + '.msgpack');
                } else {
                    alert("Model SHA1 doesn't match!");
                }
            }
            var num_chunks = Number(MODELS.get(row).escape(model_chunks_column));
            var columns =  _.map(_.range(num_chunks), function (x) {
                return model_column + '-' + x;
            });
            console.log(row)
            PICARUS.getRow('models', row, {columns: columns, success: takeoutSuccess})
        }
        $('.takeout_link').click(function (data) {
            process_takeout(decode_id($(data.target).attr('row')), 'meta:model_link_chunks', 'data:model_link', 'link');
        });
        $('.takeout_chain').click(function (data) {
            process_takeout(decode_id($(data.target).attr('row')), 'meta:model_chain_chunks', 'data:model_chain', 'chain');
        });

        function setup_modal(links, col) {
            links.click(function (data) {
                var row = decode_id(data.target.getAttribute('row'));
                var model = MODELS.get(row);
                $('#modal_content').val(model.escape(col));
                $('#save_button').unbind();
                $('#save_button').click(function () {
                    var attributes = {};
                    attributes[col] = $('#modal_content').val();
                    model.save(attributes, {patch: true});
                    $('#myModal').modal('hide');
                });
                $('#myModal').modal('show');
            })
        }
        function setup_modal_projects(links, col) {
            links.click(function (data) {
                var row = decode_id(data.target.getAttribute('row'));
                var model = MODELS.get(row);
                var dataTable = $('#globalDataTableDrop').val();
                var projectNames = _.keys(_.omit(PROJECTS.get(dataTable).attributes, 'row'));
                var selectedProjectsPrevious = [];
                if (!_.isUndefined(model.get('meta:projects'))) {
                    selectedProjectsPrevious = decode_projects(model);
                }
                projectNames = _.map(projectNames, function (x) {
                    if (_.contains(selectedProjectsPrevious, x))
                        return {name: x, selected: "selected='selected'"};
                    else
                        return {name: x, selected: ''};
                });
                // NOTE: This does the escaping inside the template
                var template = "<select class='multiselect' multiple='multiple' row='{{row}}'>{{#projects}}<option {{selected}}>{{name}}</option>{{/projects}}</select>";
                //selected="selected"
                //$('#modal_content_projects').val(model.escape(col)); // TODO: Determine which to click
                //_.map($('#modal_content_projects option:selected'), function (x) {return $(x).val()})
                $('#modal_content_projects').html(Mustache.render(template, {projects: projectNames}));
                $('.multiselect').multiselect();
                $('#save_button_projects').unbind();
                $('#save_button_projects').click(function () {
                    var attributes = {};
                    var selectedProjects = _.map($('#modal_content_projects option:selected'), function (x) {return base64.encode(_.unescape($(x).val()))}).join(',');
                    attributes['meta:projects'] = selectedProjects;
                    model.save(attributes, {patch: true});
                    $('#myModalProjects').modal('hide');
                });
                $('#myModalProjects').modal('show');
            })
        }
        setup_modal($('.modal_link_notes'), 'meta:notes');
        setup_modal($('.modal_link_tags'), 'meta:tags');
        setup_modal_projects($('.modal_link_projects'), 'meta:projects');
    }
    function filter(x) {
        var curProject = $('#globalProjectDrop').val();
        var modelProjects = decode_projects(x);
        return curProject === '' || _.contains(modelProjects, curProject);
    }
    new RowsView({collection: MODELS, el: $('#results'), extraColumns: [takeoutColumn, notesColumn, tagsColumn, projectsColumn, rowB64Column], postRender: postRender, deleteRows: true, columns: columns, filter: filter});
}
function render_models_create() {
    var AppView = Backbone.View.extend({
        initialize: function() {
            _.bindAll(this, 'renderKind');
            _.bindAll(this, 'renderName');
            this.collection.bind('reset', this.renderKind);
            this.collection.bind('change', this.renderKind);
            this.collection.bind('add', this.renderKind);
            this.renderKind();
        },
        events: {'change #kind_select': 'renderName',
                 'change #name_select': 'renderParam'},
        renderParam: function () {
            $('#params').html('');
            $('#slices_select').html('');
            var model_kind = $('#kind_select option:selected').val();
            var name = $('#name_select option:selected').val();
            model_create_selector($('#slices_select'), $('#params'), model_kind, name);
        },
        renderKind: function() {
            var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};"
            var models_filt = _.uniq(_.map(this.collection.models, function (data) {return data.escape('kind')}));
            if (!models_filt.length)
                return;
            $('#kind_select').html(Mustache.render(select_template, {models: models_filt}));
            this.renderName();
        },
        renderName: function () {
            var model_kind = $('#kind_select option:selected').val();
            var cur_models = this.collection.filter(function (x) { return x.escape('kind') == model_kind});
            var select_template = "{{#models}}<option value='{{.}}'>{{.}}</option>{{/models}};"
            var models_filt = _.map(cur_models, function (data) {return data.escape('name')});
            $('#name_select').html(Mustache.render(select_template, {models: models_filt}));
            this.renderParam();
        }
    });
    av = new AppView({collection: PARAMETERS, el: $('#selects')});
    $('#runButton').click(function () {
        var params = model_create_selector_get($('#params'))
        function success(response) {
            var row = response.row;
            if (_.isUndefined(row))
                row = response.modelRow;
            var model = new PicarusRow({row: row}, {table: 'models', columns: ['meta:']});
            MODELS.add(model);
            model.fetch();
            $('#results').html(response.row);
            button_reset();
        }
        var model_kind = $('#kind_select option:selected').val();
        var name = $('#name_select option:selected').val();
        var model = PARAMETERS.filter(function (x) {
            if (x.escape('kind') == model_kind && x.escape('name') == name)
                return true;
        })[0];
        var path = model.get('row');
        params.path = path;
        if (model.escape('type') === 'factory') {
            params.table = 'images';
            params.slices = slices_selector_get().join(';');
            p = params;
            PICARUS.postTable('models', {success: _.partial(watchJob, {success: _.partial(updateJobStatus, $('#results')), done: success}), data: params});
        } else {
            PICARUS.postTable('models', {success: success, data: params});
        }
    });
}
function render_models_single() {
    function render_image(image_data, div, success) {
        var image_id = _.uniqueId('image_');
        var canvas_id = _.uniqueId('canvas_');
        var image_tag = $('<img>').css('visibility', 'hidden').css('display', 'none').attr('id', image_id);
        image_tag.load(function () {
            success(image_id, canvas_id);
        });
        div.append(image_tag.attr('src', image_data));
    }
    function render_image_boxes(image_data, boxes, num_boxes, div) {
        render_image(image_data, div, function (image_id, canvas_id) {
            var h = $('#' + image_id).height();
            var w = $('#' + image_id).width();
            div.append($('<canvas>').attr('id', canvas_id).attr('height', h + 'px').attr('width', w + 'px'));
            var c = document.getElementById(canvas_id);
            var ctx = c.getContext("2d");
            ctx.strokeStyle = 'blue';
            var img = document.getElementById(image_id);
            ctx.drawImage(img, 0, 0);
            _.each(_.range(num_boxes), function (x) {
                var x0 = boxes[x * 4 + 2] * w;
                var x1 = boxes[x * 4 + 3] * w;
                var y0 = boxes[x * 4] * h;
                var y1 = boxes[x * 4 + 1] * h;
                ctx.moveTo(x0, y0);ctx.lineTo(x0, y1);ctx.stroke(); // TL->BL
                ctx.moveTo(x0, y1);ctx.lineTo(x1, y1);ctx.stroke(); // BL->BR
                ctx.moveTo(x1, y1);ctx.lineTo(x1, y0);ctx.stroke(); // BR->TR
                ctx.moveTo(x1, y0);ctx.lineTo(x0, y0);ctx.stroke(); // TR->TL
            });
        });
    }
    function render_image_points(image_data, points, num_points, div) {
        render_image(image_data, div, function (image_id, canvas_id) {
            var h = $('#' + image_id).height();
            var w = $('#' + image_id).width();
            div.append($('<canvas>').attr('id', canvas_id).attr('height', h + 'px').attr('width', w + 'px'));
            var c = document.getElementById(canvas_id);
            var ctx = c.getContext("2d");
            ctx.strokeStyle = 'blue';
            var img = document.getElementById(image_id);
            ctx.drawImage(img, 0, 0);
            _.each(_.range(num_points), function (x) {
                var sz = Math.max(h, w) * points[x * 6 + 5] / 2;
                var y = points[x * 6 + 0] * h;
                var x = points[x * 6 + 1] * w;
                ctx.beginPath();
                ctx.arc(x, y,sz,0,2*Math.PI);
                ctx.stroke();
            })
                });
    }
    var models = model_dropdown({modelFilter: function (x) {return true},
                                 change: function() {},
                                 el: $('#model_select')});
    function handleFileSelect(func, evt) {
        var files = evt.target.files;
        for (var i = 0, f; f = files[i]; i++) {
            if (!f.type.match('image.*'))
                continue;
            var reader = new FileReader();
            reader.onload = (function(theFile) {
                return function(e) {
                    func(e.target.result);
                };
            })(f);
            reader.readAsDataURL(f);
        }
    }
    function fileChange(evt) {
        imageData = undefined;
        handleFileSelect(function (x) {imageData = x}, evt);
        $('#imagefile').wrap('<div />');
        if ($('#imagefile')[0].files.length != 1) {
            display_alert('You must specify an image!');
            return;
        }
        var modelKey = decode_id($('#model_select').find(":selected").val());
        function success_func(result) {
            $('#imagefile').parent().html($('#imagefile').parent().html());
            $('#imagefile').change(fileChange);
            var outputType = models.get(modelKey).escape('meta:output_type');
            if (outputType == 'binary_class_confidence') {
                $('#results').html($('<h3>').text('Classifier Confidence'));
                $('#results').append(msgpack.unpack(result[modelKey]));
            } else if (outputType == 'binary_prediction') {
                $('#results').html($('<h3>').text('Binary Prediction'));
                $('#results').append(String(msgpack.unpack(result[modelKey])));
            } else if (outputType == 'processed_image') {
                $('#results').html($('<h3>').text('Processed Image'));
                $('#results').append($('<img>').attr('src', 'data:image/jpeg;base64,' + base64.encode(result[modelKey])));
            } else if (outputType == 'image_detections') {
                $('#results').html($('<h3>').text('Detections'));
                v = msgpack.unpack(result[modelKey]);
                render_image_boxes(imageData, v[0], v[1][0], $('#results'));
            } else if (outputType == 'feature') {
                $('#results').html($('<h3>').text('Feature'));
                $('#results').append(_.escape(JSON.stringify(msgpack.unpack(result[modelKey])[0])));
            } else if (outputType == 'multi_class_distance') {
                $('#results').html($('<h3>').text('Multi Class Distance'));
                var data = msgpack.unpack(result[modelKey]);
                _.each(data, function (x) {
                    $('#results').append(x[1] + ' ' + x[0] + '<br>');
                });
            } else if (outputType == 'distance_image_rows') {
                $('#results').html($('<h3>').text('Image Search Results'));
                var data = msgpack.unpack(result[modelKey]);
                debug_data = msgpack.unpack(result[modelKey]);
                _.each(data, function (x) {
                    var image_id = _.uniqueId('image_');
                    $('#results').append('<img id="' + image_id + '">' + ' ' + x[0] + '<br>');
                    imageThumbnail(x[1], image_id);
                });
            } else if (outputType == 'feature2d_binary') {
                var data = msgpack.unpack(result[modelKey]);
                debug_data = data;
                render_image_points(imageData, data[1], data[2][0], $('#results'));
            } else {
                debug_result = result[modelKey];
                alert('Unrecognized output type');
            }
        }
        function upload_func(response) {
            PICARUS.postRow(table, response.row, {success: success_func, data: {model: modelKey, action: 'i/chain'}});
        }
        var table = 'images';
        var data = {};
        data['data:image'] = $('#imagefile')[0].files[0];
        PICARUS.postTable(table, {success: upload_func, data: data})
        $('#results').html('');
    }
    $('#imagefile').change(fileChange);
}
function render_models_slice() {
    model_dropdown({modelFilter: function (x) {return true},
                    el: $('#model_select')});
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var action = 'io/link';
        if ($('#chainCheck').is(':checked'))
            action = 'io/chain';
        var model = decode_id($('#model_select').find(":selected").val());
        PICARUS.postSlice('images', startRow, stopRow, {success:  _.partial(watchJob, {success: _.partial(updateJobStatus, $('#results')), done: button_reset}), fail: button_error, data: {action: action, model: model}});
    });
}
function render_process_thumbnail() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        PICARUS.postSlice('images', startRow, stopRow, {data: {action: 'io/thumbnail'},
                                                        success: _.partial(watchJob, {success: _.partial(updateJobStatus, $('#results')), done: button_reset}), fail: button_error})
    });
}
function render_process_delete() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        PICARUS.deleteSlice('images', startRow, stopRow, {success: button_reset, fail: button_error})
    });
}
function render_process_exif() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        PICARUS.postSlice('images', startRow, stopRow, {data: {action: 'io/exif'}, success:  _.partial(watchJob, {success: _.partial(updateJobStatus, $('#results')), done: button_reset}), fail: button_error})
    });
}
function render_process_modify() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var columnName = $('#columnName').val();
        var columnValue = $('#columnValue').val();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        var data = {};
        data[columnName] = columnValue;
        PICARUS.patchSlice('images', startRow, stopRow, {success: button_reset, fail: button_error, data: data})
    });
}
function render_process_copy() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    row_selector($('#rowPrefixDrop2'));
    $('#runButton').click(function () {
        button_running();
        var imageColumn = 'data:image';
        var columnName = $('#columnName').val();
        var columnValue = $('#columnValue').val();
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        var prefix = $('#rowPrefixDrop2 option:selected').val();
        var maxRows = Number($('#maxRows').val());
        function success(row, columns) {
            // Generate row key
            var cur_row = prefix + random_bytes(10);
            cur_data = {};
            cur_data[imageColumn] = columns[imageColumn];
            if (columnName.length)
                cur_data[columnName] = columnValue;
            PICARUS.patchRow("images", cur_row, {data: cur_data});
        }
        // Scan through rows, each one write back to the prefix
        PICARUS.scanner("images", startRow, stopRow, {success: success, done: button_reset, fail: button_error, maxRows: maxRows, maxRowsIter: 5, columns: [imageColumn]});
    });
}
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
                        _.each(slicesData, function (data) {
                            PICARUS.postSlice('images', data.startRow, data.stopRow, {data: {action: 'io/thumbnail'},
                                                                                      success: _.partial(watchJob, {done: function () {data.thumbnail = 'Done';r()}})});
                        })
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
}
function render_jobs_list() {
    var workerColumn = {header: "Worker", getFormatted: function() {
        if (JOBS.get(this.get('row')).get('type') != 'annotation')
            return '';
        return Mustache.render("<a href='/v0/annotation/{{task}}/index.html' target='_blank'>Worker</a>", {task: this.escape('row')});
    }};
    var syncColumn = {header: "Sync", getFormatted: function() {
        if (JOBS.get(this.get('row')).get('type') != 'annotation')
            return '';
        return '<span style="font-size:5px"><a class="tasks-sync" row="' + encode_id(this.get('row')) + '">sync</a></span>';
    }};

    function postRender() {
        $('.tasks-sync').click(function (data) {
            var row = decode_id(data.target.getAttribute('row'));
            var model = JOBS.get(row);
            PICARUS.postRow('jobs', row, {data: {'action': 'io/annotation/sync'}});
        });
    }
    // TODO: Filter based on type == annotation
    new RowsView({collection: JOBS, el: $('#results'), extraColumns: [workerColumn, syncColumn], postRender: postRender, deleteRows: true});
    var $clearCompletedButton = $('#clearCompletedButton');
    button_confirm_click_reset($clearCompletedButton);
    button_confirm_click($clearCompletedButton, function () {
        _.map(JOBS.filter(function (x) {return x.get('status') == 'completed'}), function (x) {x.destroy({wait: true})});
        button_confirm_click_reset($clearCompletedButton);
    });
}
function render_jobs_flickr() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        button_running();
        var demo_class = $('#democlass').val();
        var demo_query = $('#demoquery').val();
        var row_prefix = $('#rowPrefixDrop').val();
        if (demo_query.length == 0 && row_prefix.length == 0) {
            display_alert('Must specify query and prefix');
            return;
        }
        queries = _.shuffle(demo_query.split(';'));
        var iters = parseInt($('#demoiters').val())
        var simul = 10;
        if (isNaN(iters) || iters < 1 || iters > 20) {
            display_alert('Iters must be 0 < x <= 20');
            return;
        }
        $('#results').html('');
        /* Check input */
        //reset_state();
        var min_time = 1232170610;
        var latitude = Number($('#demolat').val());
        var longitude = Number($('#demolon').val());
        var done = 0;

        states = [];
        _.each(queries, function (query) {
            var state = {query: query, className: demo_class};
            _.each(_.range(iters), function () {states.push(state)});
        });
        states = _.shuffle(states);
        simul = Math.min(simul, states.length);
        function call_api(state) {
            var timeRadius = 60 * 60 * 24 * 30 * 6; // 6 months
            var minUploadDate = parseInt((new Date().getTime() / 1000 - min_time) * Math.random() + min_time - timeRadius);
            var maxUploadDate = parseInt(timeRadius * 2 + minUploadDate);
            var p = {action: 'o/crawl/flickr', hasGeo: Number($('#demogeo').is(':checked')), query: state.query, minUploadDate: minUploadDate, maxUploadDate: maxUploadDate};
            var apiKey = $('#demoapikey').val();
            var apiSecret = $('#demoapisecret').val();
            if (apiKey && apiSecret) {
                p.apiKey = apiKey;
                p.apiSecret = apiSecret;
            }
            if (state.className.length)
                p.className = state.className;
            if (latitude && longitude) {
                p.lat = String(latitude);
                p.lon = String(longitude);
            }
            function success() {          
                function etod(e) {
                    var d = new Date(0);
                    d.setUTCSeconds(e);
                    return d.toString();
                }
                var data = {minUploadDate: etod(minUploadDate), maxUploadDate: etod(maxUploadDate)};
                $('#results').append('Crawl Finished : ' + state.query + ' '+ JSON.stringify(data) + '<br>');
                if (!states.length) {
                    simul -= 1;
                    if (!simul)
                        button_reset();
                    return;
                }
                call_api(states.pop());
            }
            var graphDiv = $('<div>');
            $('#results').append(graphDiv);
            $('#results').append($('<br>'));
            PICARUS.postSlice('images', row_prefix, prefix_to_stop_row(row_prefix), {success: _.partial(watchJob, {success: _.partial(updateJobStatus, graphDiv), done: success}), data: p});
        }
        _.each(_.range(simul), function () {call_api(states.pop())});
    });
}
function render_jobs_class() {
    slices_selector();
    $('#runButton').click(function () {
        var startRow = $('#startRow').val();
        var stopRow = $('#stopRow').val();
        var imageColumn = 'thum:image_150sq';
        var numTasks = Number($('#num_tasks').val());
        var classColumn = $('#class').val();
        var mode = $('#modeSelect').val();
        function success(response) {
            JOBS.fetch();
            $('#results').append($('<a>').attr('href', '/v0/annotation/' + response.row + '/index.html').text('Worker').attr('target', '_blank'));
        }
        PICARUS.postTable('jobs', {success: success, data: {path: 'annotation/images/class', slices: slices_selector_get().join(';'), imageColumn: imageColumn, classColumn: classColumn, instructions: $('#instructions').val(), numTasks: numTasks, mode: mode}});
    });
}
function render_visualize_thumbnails() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        function uninstallScroll() {
            $(window).unbind("scroll");
            $(window).off('scroll.infinite resize.infinite');
        }
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var imageColumn = 'thum:image_150sq';
        var getMoreData = undefined;
        var hasMoreData = true;
        var gimmeMoreData = false; // 
        uninstallScroll();
        $('#results').html('');
        var $el = $('<div>');
        $('#results').append($el);
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        function success(row, columns) {
            c = columns;
            console.log(row);
            if (!_.has(columns, imageColumn))
                return;
            console.log(row);
            $el.append($('<img>').attr('src', 'data:image/jpeg;base64,' + base64.encode(columns[imageColumn])).attr('title', row));
        }
        function done() {
            hasMoreData = false;
        }
        function resume(callback) {
            console.log('Got resume');
            if (gimmeMoreData) {
                gimmeMoreData = false;
                callback();
            } else
                getMoreData = callback;
        }
        var params = {success: success, columns: [imageColumn], resume: resume};
        $el.infiniteScroll({threshold: 1024, onEnd: function () {
            console.log('No more results');
        }, onBottom: function (callback) {
            if (!jQuery.contains(document.documentElement, $el[0])) {
                uninstallScroll();
                return;
            }
            console.log('More data!');
            if (hasMoreData)
                if (!_.isUndefined(getMoreData)) {
                    var more = getMoreData;
                    getMoreData = undefined;
                    more();
                } else {
                    gimmeMoreData = true;
                }
            callback(hasMoreData);
        }});
        PICARUS.scanner("images", startRow, stopRow, params);
    });
}
function render_visualize_metadata() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var max_size = Number($('#maxSize').val());
        var metaCF = 'meta:';
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        button_confirm_click_reset($('#removeButton'));
        // Setup table
        images = new PicarusRows([], {'table': 'images'});
        function remove_rows() {
            // TODO: Since there is a maxRows setting, this won't remove all rows, just the ones we have available
            var rows = _.map(images.models, function (x) {return x.id});
            picarus_api_delete_rows(rows, progressModal());
        }
        function done() {
            $('#results').html('');
            if (!images.length)
                return;
            // TODO: Change to use RowsView
            var AppView = Backbone.View.extend({
                initialize: function() {
                    _.bindAll(this, 'render');
                    this.collection.bind('reset', this.render);
                    this.collection.bind('change', this.render);
                    this.collection.bind('add', this.render);
                    this.collection.bind('sync', this.render);
                },
                render: function() {
                    var columns = _.uniq(_.flatten(_.map(this.collection.models, function (x) {
                        return _.keys(x.attributes);
                    })));
                    picarus_table = new Backbone.Table({
                        collection: this.collection,
                        columns: _.map(columns, function (v) {
                            if (v === "row")
                                return [v, v];
                            return {header: v, getFormatted: function() {
                                var out = this.get(v);
                                if (typeof out !== 'undefined') {
                                    if (out.length <= max_size)
                                        return out;
                                    else
                                        return '<span style="color:red">' + out.slice(0, max_size) + '</span>'
                                }
                            }};
                        })
                    });
                    this.$el.html(picarus_table.render().el);
                }
            });
            av = new AppView({collection: images, el: $('#results')});
            av.render();
            $('#removeButton').removeAttr('disabled');
            button_confirm_click($('#removeButton'), remove_rows);
        }
        function success(row, columns) {
            columns.row = row;
            images.add(columns);
        }
        var params = {success: success, maxRows: 1000, done: done, columns: [metaCF]};
        PICARUS.scanner("images", startRow, stopRow, params)
    });
}
function render_visualize_exif() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    $('#runButton').click(function () {
        var startRow = unescape($('#startRow').val());
        var stopRow = unescape($('#stopRow').val());
        var max_size = Number($('#maxSize').val());
        var exif_column = 'meta:exif';
        if (startRow.length == 0 || stopRow.length == 0) {
            display_alert('Must specify rows');
            return;
        }
        images = new PicarusRows([], {'table': 'images'});
        function done() {
            $('#results').html('');
            if (!images.length)
                return;
            // TODO: Change to use RowsView
            var AppView = Backbone.View.extend({
                initialize: function() {
                    _.bindAll(this, 'render');
                    this.collection.bind('reset', this.render);
                    this.collection.bind('change', this.render);
                    this.collection.bind('add', this.render);
                },
                render: function() {
                    var cur_images = this.collection.filter(function (x) {return x.get(exif_column) != '{}' && !_.isUndefined(x.get(exif_column))});
                    columns = _.uniq(_.flatten(_.map(cur_images, function (x) {
                        return _.keys(JSON.parse(x.get(exif_column)));
                    }))).concat(['row']);
                    picarus_table = new Backbone.Table({
                        collection: this.collection,
                        columns: _.map(columns, function (v) {
                            if (v === "row")
                                return [v, v];
                            return {header: v, getFormatted: function() {
                                var cur_exif = JSON.parse(this.get(exif_column));
                                var out = cur_exif[v];
                                if (typeof out !== 'undefined') {
                                    if (!_.isString(out))
                                        return _.escape(JSON.stringify(out));
                                    out = base64.decode(out);
                                    if (typeof out.length <= max_size)
                                        return _.escape(out);
                                    else
                                        return '<span style="color:red">' + _.escape(out.slice(0, max_size)) + '</span>'
                                }
                            }};
                        })
                    });
                    this.$el.html(picarus_table.render().el);
                }
            });
            av = new AppView({collection: images, el: $('#results')});
            av.render();
        }
        function success(row, columns) {
            columns.row = row;
            if (columns[exif_column] != '{}')
                images.add(columns);
        }
        var params = {success: success, maxRows: 1000, done: done, columns: [exif_column]};
        PICARUS.scanner("images", startRow, stopRow, params)
    });
}
function render_visualize_locations() {
    var script = document.createElement("script");
    script.type = "text/javascript";
    script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyBBsKtzgLTIsaoxAFUvSNoJ8n3j4w9VZs0&sensor=false&callback=render_visualize_locations_loaded";
    document.body.appendChild(script);
}
function render_visualize_locations_loaded() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    function deg2rad(deg) {
        return deg * (Math.PI/180)
    }
    function getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2) {
        // From: http://stackoverflow.com/questions/27928/how-do-i-calculate-distance-between-two-latitude-longitude-points
        var R = 6371; // Radius of the earth in km
        var dLat = deg2rad(lat2-lat1);
        var dLon = deg2rad(lon2-lon1); 
        var a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * Math.sin(dLon/2) * Math.sin(dLon/2); 
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
        var d = R * c; // Distance in km
        return d;
    }
    function filter_lat_long(lat, lon) {
        var targetLat = Number($('#demolat').val());
        var targetLong = Number($('#demolong').val());
        var targetDist = Number($('#demodist').val());
        var checked = $('#filterInvert').is(':checked');
        if (!targetLat || !targetLong)
            return checked;
        if (getDistanceFromLatLonInKm(targetLat, targetLong, lat, lon) > targetDist)
            return !checked;
        return checked;
    }
    $('#runButton').click(function () {
        var latitude = 'meta:latitude';
        var longitude = 'meta:longitude';
        button_confirm_click_reset($('#removeButton'));
        images = new PicarusRows([], {'table': 'images'});
        function maps_success(row, columns) {
            columns.row = row;
            var curLat = columns[latitude];
            var curLong = columns[longitude];
            if (filter_lat_long(Number(curLat), Number(curLong))) {
                return;
            }
            images.add(new PicarusRow(columns));
        }
        function maps_done() {
            var centerLat = Number($('#demolat').val());
            var centerLong = Number($('#demolong').val());
            button_confirm_click($('#removeButton'), function () {
                var rows = _.map(images.models, function (x) {return x.get('row')});
                picarus_api_delete_rows(rows, progressModal());
            });
            $('#removeButton').removeAttr('disabled');
            if (!centerLat || !centerLat) {
                centerLat = Number(images.at(0).get(latitude));
                centerLong = Number(images.at(0).get(longitude));
            }
            var mapOptions = {
                zoom: 14,
                center: new google.maps.LatLng(centerLat, centerLong),
                mapTypeId: google.maps.MapTypeId.HYBRID
            };
            map = new google.maps.Map(document.getElementById("map_canvas"),
                                      mapOptions);
            google.maps.event.addListener(map, 'rightclick', function(event){
                $('#demolat').val(event.latLng.lat());
                $('#demolong').val(event.latLng.lng());
            });
            images.each(function (x) {
                var lat = Number(x.get(latitude));
                var lon = Number(x.get(longitude));
                new google.maps.Marker({position: new google.maps.LatLng(lat, lon), map: map});
            });
        }
        PICARUS.scanner("images", unescape($('#startRow').val()), unescape($('#stopRow').val()), {success: maps_success, done: maps_done, columns: [latitude, longitude]});
    })
}
function render_visualize_times() {
    google_visualization_load(render_visualize_times_loaded);
}

function render_visualize_times_loaded() {
    row_selector($('#rowPrefixDrop'), {startRow: $('#startRow'), stopRow: $('#stopRow')});
    function drawYears(hist) {
        var data = google.visualization.arrayToDataTable([['Year', 'Count']].concat(hist));
        new google.visualization.ColumnChart(document.getElementById('histYear')).draw(data, {title:"Histogram (Year)", width:600, height:400, vAxis: {title: "Count"}, hAxis: {title: "Year"}});
    }
    function drawMonths(hist) {
        var data = google.visualization.arrayToDataTable([['Month', 'Count']].concat(hist));
        new google.visualization.ColumnChart(document.getElementById('histMonth')).draw(data, {title:"Histogram (Month)", width:600, height:400, vAxis: {title: "Count"}, hAxis: {title: "Month"}});
    }
    function drawHours(hist) {
        var data = google.visualization.arrayToDataTable([['Hour', 'Count']].concat(hist));
        new google.visualization.ColumnChart(document.getElementById('histHour')).draw(data, {title:"Histogram (Hour)", width:600, height:400, vAxis: {title: "Count"}, hAxis: {title: "Hour"}});
    }
    function drawDays(hist) {
        var data = google.visualization.arrayToDataTable([['Day', 'Count']].concat(hist));
        new google.visualization.ColumnChart(document.getElementById('histDay')).draw(data, {title:"Histogram (Day)", width:600, height:400, vAxis: {title: "Count"}, hAxis: {title: "Day"}});
    }
    function dataToHist(data) {
        var hist = {};
        _.each(data, function (x) {
            var y = 0;
            if (_.has(hist, x)) {
                y = hist[x];
            }
            hist[x] = y + 1;
        });
        return hist;
    }
    function dataToListHist(data) {
        return _.map(_.pairs(dataToHist(data)), function (x) {return [Number(x[0]), x[1]]}).sort();
    }
    $('#runButton').click(function () {
        var timeColumn = 'meta:dateupload';
        images = new PicarusRows([], {'table': 'images'});
        function time_success(row, columns) {
            columns.row = row;
            images.add(new PicarusRow(columns));
        }
        function time_done() {
            years = [];
            months = [];
            hours = [];
            days = [];
            // TODO: FInish visual
            images.each(function (x) {
                var curTime = Number(x.get(timeColumn));
                var curDate = new Date(0);
                curDate.setUTCSeconds(curTime);
                years.push(curDate.getFullYear());
                months.push(curDate.getMonth());
                hours.push(curDate.getHours());
                days.push(curDate.getDay());
            });
            drawYears(dataToListHist(years));
            drawMonths(dataToListHist(months));
            drawHours(dataToListHist(hours));
            drawDays(dataToListHist(days));
        }
        PICARUS.scanner("images", unescape($('#startRow').val()), unescape($('#stopRow').val()), {success: time_success, done: time_done, columns: [timeColumn]});
    })
}
function render_visualize_annotations() {
    google_visualization_load(render_visualize_annotations_loaded);
}

function render_visualize_annotations_loaded() {
    function collect_users(users, results, onlyWorkers, onlyAnnotated) {
        var users_filtered = {};
        users.each(function(x) {
            if (x.escape('workerId') || !onlyWorkers)
                users_filtered[x.get('row')] = [];
        });
        results.each(function (x) {
            var i = x.escape('userId');
            if (_.has(users_filtered, i) && (!onlyAnnotated || x.escape('endTime'))) {
                users_filtered[i].push(x);
            }
        });
        _.each(users_filtered, function (x) {
            x.sort(function (a, b) {
                a = Number(a.escape('startTime'));
                b = Number(b.escape('startTime'));
                if (a < b)
                    return -1;
                if (a > b)
                    return 1;
                return 0;
            });
        });
        return users_filtered;
    }
    function image_class_score(results) {
        // Only count explicit marks
        var scores = {};

        _.each(results, function (x) {
            var annotation = x.get('userData');
            if (_.isUndefined(annotation))
                return;
            annotation = JSON.parse(annotation);
            var image = x.get('image');
            var cls = x.escape('class');
            if (!_.has(scores, cls)) {
                scores[cls] = {scoresPos: {}, scoresNeg: {}, scoresTotal: {}};
            }
            var scoresPos = scores[cls].scoresPos;
            var scoresNeg = scores[cls].scoresNeg;
            var scoresTotal = scores[cls].scoresTotal;
            if (_.has(scoresTotal, image))
                scoresTotal[image] += 1;
            else
                scoresTotal[image] = 1;
            if (annotation == 'true') {
                if (_.has(scoresPos, image))
                    scoresPos[image] += 1;
                else
                    scoresPos[image] = 1;
            }
            if (annotation == 'false') {
                if (_.has(scoresNeg, image))
                    scoresNeg[image] += 1;
                else
                    scoresNeg[image] = 1;
            }
        });
        return scores;
    }
    function display_annotation_task(task, get_classes, get_scores) {
        results = new PicarusRows([], {'table': 'annotation-results-' + task});
        users = new PicarusRows([], {'table': 'annotation-users-' + task});
        var imageColumn = 'thum:image_150sq';
        $('#negPct').change(data_change);
        $('#posPct').change(data_change);
        $('#posCnt').change(data_change);
        $('#negCnt').change(data_change);
        function data_change() {
            user_annotations = collect_users(users, results, true, true);
            clean_results = _.flatten(_.values(user_annotations), true);
            var classes = get_classes(clean_results);
            var select_template = "{{#classes}}<option value='{{.}}'>{{.}}</option>{{/classes}};"
            $('#class_select').html(Mustache.render(select_template, {classes: classes}));
            $('#class_select').unbind();
            $('#class_select').change(class_select_change);
            class_scores = get_scores(clean_results);
            class_select_change();
            var scores = _.map(class_scores, function (s, class_name) {
                var out = {pos: 0, neg: 0, total: 0, unique: _.size(s.scoresTotal)};
                _.each(s.scoresPos, function (x) {
                    out.pos += x;
                });
                _.each(s.scoresNeg, function (x) {
                    out.neg += x;
                });
                _.each(s.scoresTotal, function (x) {
                    out.total += x;
                });
                out.quality = (out.pos - out.neg) / (out.total + .0000001);
                out.class_name = class_name;
                return out;
            });
            // Update class annotations table
            scores.sort(function (x, y) {return y.quality - x.quality})
            var scores_template = "<table><tr><td>Name</td><td>Pos Annot.</td><td>Neg Annot.</td><td>Tot Annot.</td><td>Unique</td></tr>{{#scores}}<tr><td>{{class_name}}</td><td>{{pos}}</td><td>{{neg}}</td><td>{{total}}</td><td>{{unique}}</td></tr>{{/scores}}</table>";
            $('#annotation-stats').html(Mustache.render(scores_template, {scores: scores}));
            // Update user annotation time vs iteration
            annotation_times = {};
            _.each(user_annotations, function (z) {
                _.each(z, function(x, y) {
                    var t = Number(x.escape('endTime')) - Number(x.escape('startTime'));
                    if (_.has(annotation_times, y))
                        annotation_times[y].push(t)
                    else
                        annotation_times[y] = [t];
                });
            });
            var mean = function (x) { return _.reduce(x, function(memo, num){ return memo + num; }, 0) / x.length};
            median_rows = _.map(annotation_times, function (x, y) {
                x.sort(function (x, y) {return x - y});
                return [Number(y), _.min(x), x[Math.round(x.length / 2)], mean(x)]
            });
            var data0 = to_google_data(median_rows, ['Iteration', 'Min', 'Median', 'Mean']);
            var options = {title: 'Annotation Time vs Iteration #',
                           hAxis: {title: 'Iteration'}};
            var chart0 = new google.visualization.LineChart(document.getElementById('annotator_time_graph'));
            chart0.draw(data0, options);
        }
        function class_select_change() {
            var class_name = $('#class_select').find(":selected").val();
            negPct = Number($('#negPct').val());
            posPct = Number($('#posPct').val());
            negCnt = Math.max(1, Number($('#negCnt').val()));
            posCnt = Math.max(1, Number($('#posCnt').val()));
            scores = class_scores[class_name];
            if (_.isUndefined(scores))
                return;
            ts = scores.scoresTotal;
            posScores = _.sortBy(_.filter(_.pairs(scores.scoresPos), function (x) {return x[1] >= posCnt && (x[1] / ts[x[0]]) >= posPct}), function (x) { return -x[1] });
            negScores = _.sortBy(_.filter(_.pairs(scores.scoresNeg), function (x) {return x[1] >= negCnt && (x[1] / ts[x[0]]) >= negPct}), function (x) { return x[1] });
            os = _.omit(_.omit(ts, _.keys(scores.scoresPos)), _.keys(scores.scoresNeg));
            otherScores = _.shuffle(_.pairs(os));
            function display_samples(div, scores, title) {
                div.html('');
                div.append($('<h3>').text(title + ' ' + scores.length + ' / ' + _.size(ts)));
                
                _.each(scores.slice(0, 24), function (x) {
                    var id = _.uniqueId('image_');
                    div.append($('<img>').attr('id', id).attr('title', 'Row: ' + base64.encode(x[0]) + ' Score: ' + x[1]).addClass('hide'));
                    function success(response) {
                        if (_.isUndefined(response[imageColumn]))
                            return;
                        $('#' + id).attr('src', 'data:image/jpeg;base64,' + base64.encode(response[imageColumn])).attr('width', '150px').removeClass('hide');
                    }
                    PICARUS.getRow("images", x[0], {success: success, columns: [imageColumn]});
                });
            }
            display_samples($('#positive_samples'), posScores, 'Positive Samples');
            display_samples($('#negative_samples'), negScores, 'Negative Samples');
            display_samples($('#other_samples'), otherScores, 'Other Samples (not pos/neg)');
            
            // Hookup delete
            function delete_row() {
                action = $('#actionSplit').find(":selected").val();
                delKeys = _.keys(_.object({'positive': posScores, 'negative': negScores, 'other': otherScores}[action]));
                picarus_api_delete_rows(delKeys, progressModal());
                button_confirm_click_reset($('#removeButton'));
                button_confirm_click($('#removeButton'), delete_row);
            }
            button_confirm_click($('#removeButton'), delete_row);
            // Hookup modify
            function modify_row() {
                var action = $('#actionSplit').find(":selected").val();
                var modifyKeys = _.keys(_.object({'positive': posScores, 'negative': negScores, 'other': otherScores}[action]));
                picarus_api_modify_rows(modifyKeys, $('#colName').val(), $('#colValue').val(), progressModal());
                button_confirm_click_reset($('#modifyButton'));
                button_confirm_click($('#modifyButton'), modify_row);
            }
            button_confirm_click($('#modifyButton'), modify_row);
            $('#actionSplit').change(change_actions);
            function change_actions () {
                button_confirm_click_reset($('#removeButton'));
                button_confirm_click($('#removeButton'), delete_row);
                button_confirm_click_reset($('#modifyButton'));
                button_confirm_click($('#modifyButton'), modify_row);
            }
        }
        new RowsView({collection: results, el: $('#annotation-results'), postRender: _.debounce(data_change, 100)});
        results.fetch();
        
        new RowsView({collection: users, el: $('#annotation-users'), postRender: _.debounce(data_change, 100)});
        users.fetch();
        debug_dc = data_change;
    }
    function change() {
        var task = decode_id($('#annotator_select').find(":selected").val());
        if (_.isUndefined(task)) {
            return;
        }
        function success_annotation(annotation) {
            annotation_type = JSON.parse(annotation['params']).type;
            if (annotation_type == 'image_class') {
                get_classes = function (results) {
                    return _.unique(results.map(function (x, y) {return x.escape('class')})).sort()
                }
                get_scores = image_class_score;
            }
            display_annotation_task(task, get_classes, get_scores);
        }
        PICARUS.getRow("jobs", task, {success: success_annotation});
    }
    rows_dropdown(JOBS, {el: $('#annotator_select'), filter: function (x) {return x.get('type') == 'annotation'}, text: function (x) {
        var p = JSON.parse(x.get('params'));
        if (p.type == "image_class")
            return p.type + ' ' + p.num_tasks;
        return p.type;
    }, change: change});
}
function render_evaluate_classifier() {
    google_visualization_load(render_evaluate_classifier_loaded);
}

function render_evaluate_classifier_loaded() {
    model_dropdown({modelFilter: function (x) {return x.escape('meta:output_type') === 'binary_class_confidence'},
                    change: function() {
                        var row = decode_id(this.$el.find(":selected").val());
                        m = this.collection.get(row);
                        $('#gtColumn').val(JSON.parse(m.get('meta:factory_info')).inputs.meta);
                        $('#posClass').val(JSON.parse(m.get('meta:factory_info')).params.class_positive);
                        $('#modelKey').val(encode_id(row));
                    },
                    el: $('#model_select')});
    slices_selector();
    $('#runButton').click(function () {
        button_running();
        confs = {pos_confs: [], neg_confs: []};
        var gt_column = decode_id($('#gtColumn').val());
        var conf_column = decode_id($('#modelKey').val());
        var posClass = $('#posClass').val();
        
        sliceStats = {}; // [startRow/stopRow] = {# pos, # neg, # noconf, #nometa, #noconfmeta}
        var slices = slices_selector_get(true);
        _.each(slices, function (start_stop_row, index) {
            var curSlice = start_stop_row.join('/');
            sliceStats[curSlice] = {'numPos': 0, 'numNeg': 0, 'noConf': 0, 'noGT': 0, 'noConfGT': 0};
            function success(row, columns) {
                $('#progress').css('width', (100 * (confs.pos_confs.length + confs.neg_confs.length) / 19850.) + '%')
                c = columns;
                if (_.has(columns, conf_column) && _.has(columns, gt_column)) {
                    if (columns[gt_column] == posClass) {
                        sliceStats[curSlice].numPos += 1;
                        confs.pos_confs.push(msgpack.unpack(columns[conf_column]));
                    } else {
                        sliceStats[curSlice].numNeg += 1;
                        confs.neg_confs.push(msgpack.unpack(columns[conf_column]));
                    }
                } else {
                    if (!_.has(columns, conf_column))
                        sliceStats[curSlice].noConf += 1;
                    if (!_.has(columns, gt_column))
                        sliceStats[curSlice].noConfGT += 1;
                    if (!_.has(columns, gt_column))
                        sliceStats[curSlice].noGT += 1;
                }
            }
            var success_confs;
            if (index == (slices.length - 1))
                success_confs = function () {
                    confs.neg_confs.sort(function(a, b) {return a - b});
                    confs.pos_confs.sort(function(a, b) {return a - b});
                    plot_confs(confs);
                    render_slice_stats_table($('#slicesTable'), sliceStats);
                    button_reset();
                }
            else
                success_confs = function () {}
            PICARUS.scanner("images", decode_id(start_stop_row[0]), decode_id(start_stop_row[1]), {success: success, done: success_confs, columns: [gt_column, conf_column]});
        });
    })
}
function render_slice_stats_table(table, sliceStats) {
    //sliceStats[curSlice] = {'numPos': 0, 'numNeg': 0, 'noConf': 0, 'noGT': 0, 'noConfGT': 0};
    var select_template = "<table>{{#slices}}<tr><td>{{name}}</td><td>{{numPos}}</td><td>{{numNeg}}</td><td>{{noConf}}</td><td>{{noGT}}</td><td>{{noConfGT}}</td></tr>{{/slices}}</table>"
    function convert_name(k) {
        return _.map(k.split('/'), function (x) {
            return decode_id(x);
        }).join('/');
    }
    var slices = [{name: 'Slice', numPos: 'Pos', numNeg: 'Neg', noConf: 'No Conf', noGT: 'No GT', noConfGT: 'No ConfGT'}];
    slices = slices.concat(_.map(sliceStats, function (v, k) {v.name = convert_name(k); return v}));
    table.html(Mustache.render(select_template, {slices: slices}));
}
function confs_to_conf_hist(pos_confs, neg_confs, bins, normalize) {
    /* Takes in confs, produces a histogram capturing both pos/neg confs in each bin
       TODO: Check that each bin gets get an equal portion of the range
    */
    var min_conf = Math.min(pos_confs[0], neg_confs[0]);
    var max_conf = Math.min(pos_confs[pos_confs.length - 1], neg_confs[neg_confs.length - 1]);
    var shift = min_conf;
    var scale = bins / (max_conf - min_conf);
    var pos_buckets = [];
    var neg_buckets = [];
    var coords = [];
    var i, cur_bucket;
    for (i = 0; i < bins; i++) {
        pos_buckets[i] = 0;
        neg_buckets[i] = 0;
    }
    for (i = 0; i < pos_confs.length; i++) {
        pos_buckets[Math.min(bins - 1, Math.max(0, Math.floor((pos_confs[i] - shift) * scale)))] += 1;
    }
    for (i = 0; i < neg_confs.length; i++) {
        neg_buckets[Math.min(bins - 1, Math.max(0, Math.floor((neg_confs[i] - shift) * scale)))] += 1;
    }
    for (i = 0; i < bins; i++) {
        coords[i] = [(i + .5) / scale + shift, pos_buckets[i], neg_buckets[i]];
        if (normalize) {
            coords[i][1] /= pos_confs.length;
            coords[i][2] /= neg_confs.length;
        }
    }
    return coords;
}
function test_confs_to_confusion_matrix() {
    //var cms;
    cms = confs_to_confusion_matrix([], []);
    if (!_.isEqual(cms, []))
        return 1;
    
    cms = confs_to_confusion_matrix([0], []);
    if (!_.isEqual(cms, [[1, 0, 0, 0, 0]]))
        return 2;
    
    cms = confs_to_confusion_matrix([], [0]);
    if (!_.isEqual(cms, [[0, 0, 1, 0, Infinity]]))
        return 3;
    
    cms = confs_to_confusion_matrix([0], [0]);
    if (!_.isEqual(cms, [[1, 1, 0, 0, 0], [0, 0, 1, 1, Infinity]]))
        return 4;
    
    cms = confs_to_confusion_matrix([1], [0]);
    if (!_.isEqual(cms, [[1, 0, 1, 0, 1]]))
        return 5;
    
    cms = confs_to_confusion_matrix([0], [1]);
    if (!_.isEqual(cms, [[1, 1, 0, 0, 0], [0, 0, 1, 1, Infinity]]))
        return 6;
    
    cms = confs_to_confusion_matrix([0, 0], [0]);
    if (!_.isEqual(cms, [[2, 1, 0, 0, 0], [0, 0, 1, 2, Infinity]]))
        return 7;
    
    cms = confs_to_confusion_matrix([0, 1], [0]);
    if (!_.isEqual(cms, [[2, 1, 0, 0, 0], [1, 0, 1, 1, 1]]))
        return 8;
    
    cms = confs_to_confusion_matrix([0, 0], [1]);
    if (!_.isEqual(cms, [[2, 1, 0, 0, 0], [0, 0, 1, 2, Infinity]]))
        return 9;
    
    cms = confs_to_confusion_matrix([1, 2], [0]);
    if (!_.isEqual(cms, [[2, 0, 1, 0, 1]]))
        return 10;
    
    cms = confs_to_confusion_matrix([0, 2], [1]);
    if (!_.isEqual(cms, [[2, 1, 0, 0, 0], [1, 0, 1, 1, 2]]))
        return 11;
    
    cms = confs_to_confusion_matrix([0, 1], [2]);
    if (!_.isEqual(cms, [[2, 1, 0, 0, 0], [0, 0, 1, 2, Infinity]]))
        return 12;
    
    cms = confs_to_confusion_matrix([1, 2], [0, 3]);
    if (!_.isEqual(cms, [[2, 1, 1, 0, 1], [0, 0, 2, 2, Infinity]]))
        return 13;
    
    cms = confs_to_confusion_matrix([1, 2, 3], [0, 3]);
    if (!_.isEqual(cms, [[3, 1, 1, 0, 1], [0, 0, 2, 3, Infinity]]))
        return 14;
    
    cms = confs_to_confusion_matrix([1, 2, 3, 3], [0, 3]);
    if (!_.isEqual(cms, [[4, 1, 1, 0, 1], [0, 0, 2, 4, Infinity]]))
        return 15;
    return 0;
}
function confs_to_confusion_matrix(pos_confs, neg_confs) {
    /* Takes in confs, produces list of [tp, fp, tn, fn, thresh] */
    var cm_threshs = [];
    var fn = 0;
    var tn = 0;
    var i;
    var cur_thresh;
    while (pos_confs.length || neg_confs.length) {
        // Skip Negatives
        for (i = 0; i < neg_confs.length; i++) {
            if (neg_confs[i] >= pos_confs[0]) {
                break;
            }
        }
        neg_confs = neg_confs.slice(i, neg_confs.length);
        tn += i;
        // Add PR point (cur_thresh = pos_confs[0])
        if (pos_confs.length) {
            cur_thresh = pos_confs[0];
        } else {
            cur_thresh = Infinity;
        }
        cm_threshs.push([pos_confs.length, neg_confs.length, tn, fn, cur_thresh]);
        // Skip Positives
        for (i = 0; i < pos_confs.length; i++) {
            if (pos_confs[i] > neg_confs[0]) {
                break;
            }
        }
        pos_confs = pos_confs.slice(i, pos_confs.length);
        fn += i;
    }
    return cm_threshs;
}
function cms_to_rps(cms) {
    var rps = [];
    var i;
    for (i = 0; i < cms.length; i++) {
        rps.push([cms[i][0] / (cms[i][0] + cms[i][3]), cms[i][0] / (cms[i][0] + cms[i][1]), cms[i][4]])
    }
    return rps;
}
function cms_to_conf_accs(cms) {
    var conf_accs = [];
    var i;
    for (i = 0; i < cms.length; i++) {
        conf_accs.push([cms[i][4], (cms[i][0] + cms[i][2]) / (cms[i][0] + cms[i][1] + cms[i][2] + cms[i][3])])
    }
    return conf_accs;
}
function cms_to_fpr_tprs(cms) {
    var fpr_tprs = [];
    var i, fpr, tpr;
    var p = confs.pos_confs.length;
    var n = confs.neg_confs.length;
    for (i = 0; i < cms.length; i++) {
        fpr = cms[i][1] / n; // FP / N
        tpr = cms[i][0] / p; // TP / P
        fpr_tprs.push([fpr, tpr, cms[i][4]]);
    }
    return fpr_tprs;
}
function to_google_data(pts, labels, tooltip) {
    var i;
    var data = new google.visualization.DataTable();
    for (i = 0; i < labels.length; i++) {
        data.addColumn('number', labels[i]);
    }
    if (tooltip) {
        data.addColumn({type: 'number', role: 'tooltip'});
    }
    d = pts;
    data.addRows(pts);
    return data;
}
function plot_confs(confs) {
    var test_out = test_confs_to_confusion_matrix();
    if (test_out)
        alert(test_out);
    var data0 = to_google_data(confs_to_conf_hist(confs.pos_confs, confs.neg_confs, 100), ['Confidence', '+', '-']);
    var options = {title: 'Classifier Confidence',
                   hAxis: {title: 'Confidence'}};
    var chart0 = new google.visualization.LineChart(document.getElementById('graph_confidence_scatter'));
    chart0.draw(data0, options);
    
    var data1 = to_google_data(confs_to_conf_hist(confs.pos_confs, confs.neg_confs, 100, true), ['Confidence', '+', '-']);
    options = {title: 'Classifier Confidence (normalized)',
               hAxis: {title: 'Confidence'}};
    var chart1 = new google.visualization.LineChart(document.getElementById('graph_confidence_scatter_norm'));
    chart1.draw(data1, options);
    
    // PR Curve
    var cms = confs_to_confusion_matrix(confs.pos_confs, confs.neg_confs);
    // Confidence accuracy
    var data4 = to_google_data(cms_to_conf_accs(cms), ['Confidence', 'Accuracy']);
    options = {title: 'Classifier Confidence vs Accuracy',
               hAxis: {title: 'Confidence'}};
    var chart4 = new google.visualization.LineChart(document.getElementById('graph_confidence_accuracy'));
    chart4.draw(data4, options);
    var data2 = to_google_data(cms_to_rps(cms), ['recall', 'precision'], true);
    options = {title: 'PR Curve',
               hAxis: {title: 'Recall', minValue: 0, maxValue: 1},
               vAxis: {title: 'Precision', minValue: 0, maxValue: 1},
               chartArea: {width: 200, height: 200},
               legend: {position: 'none'}};
    var chart2 = new google.visualization.LineChart(document.getElementById('graph_rps'));
    chart2.draw(data2, options);
    
    var data3 = to_google_data(cms_to_fpr_tprs(cms), ['fpr', 'tpr'], true);
    options = {title: 'ROC Curve',
               hAxis: {title: 'FPR', minValue: 0, maxValue: 1},
               vAxis: {title: 'TPR', minValue: 0, maxValue: 1},
               chartArea: {width: 200, height: 200},
               legend: {position: 'none'}};
    var chart3 = new google.visualization.LineChart(document.getElementById('graph_roc'));
    chart3.draw(data3, options);
    
    
    // This connects all the charts together
    function setNearest(chart, data, column, select_columns, val) {
        var i, minVal = Infinity, minIndex, curVal;
        for (i = 0; i < data.getNumberOfRows(); i++) {
            curVal = Math.abs(val - data.getValue(i, column));
            if (curVal < minVal) {
                minVal = curVal;
                minIndex = i;
            }
        }
        
        chart.setSelection(_.map(select_columns, function (col) {return {row: minIndex, column: col}}));
    }
    function setSelections(thresh) {
        setNearest(chart0, data0, 0, [1, 2], thresh);
        setNearest(chart1, data1, 0, [1, 2], thresh);
        setNearest(chart2, data2, 2, [1], thresh);
        setNearest(chart3, data3, 2, [1], thresh);
        setNearest(chart4, data4, 0, [1], thresh);
    }
    var al = google.visualization.events.addListener;
    al(chart0, 'select', function () {var sel = chart0.getSelection(); if (sel[0] !== undefined) setSelections(data0.getValue(sel[0].row, 0))});
    al(chart1, 'select', function () {var sel = chart1.getSelection(); if (sel[0] !== undefined) setSelections(data1.getValue(sel[0].row, 0))});
    al(chart2, 'select', function () {var sel = chart2.getSelection(); if (sel[0] !== undefined) setSelections(data2.getValue(sel[0].row, 2))});
    al(chart3, 'select', function () {var sel = chart3.getSelection(); if (sel[0] !== undefined) setSelections(data3.getValue(sel[0].row, 2))});
    al(chart4, 'select', function () {var sel = chart4.getSelection(); if (sel[0] !== undefined) setSelections(data4.getValue(sel[0].row, 0))});
}