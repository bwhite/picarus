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
    var inputB64Column = {header: "InputB64", getFormatted: function() { return base64.encode(this.get('meta:input'))}};
    function postRender() {
        function process_takeout(row, model_chunks_column, model_column, model_type) {
            function takeoutSuccess(response) {
                 chunks = _.map(response, function (v, k) {
                    return [Number(k.split('-')[1]), v];
                 }).sort(function(a, b) {return a - b});
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
                if (!_.isUndefined(model.get('meta:projects-' + EMAIL_AUTH.email))) {
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
                    attributes['meta:projects-' + EMAIL_AUTH.email] = selectedProjects;
                    model.save(attributes, {patch: true});
                    $('#myModalProjects').modal('hide');
                });
                $('#myModalProjects').modal('show');
            })
        }
        setup_modal($('.modal_link_notes'), 'meta:notes');
        setup_modal($('.modal_link_tags'), 'meta:tags');
        setup_modal_projects($('.modal_link_projects'), 'meta:projects-' + EMAIL_AUTH.email);
    }
    function filter(x) {
        var curProject = $('#globalProjectDrop').val();
        var modelProjects = decode_projects(x);
        return curProject === '' || _.contains(modelProjects, curProject);
    }
    new RowsView({collection: MODELS, el: $('#results'), extraColumns: [takeoutColumn, notesColumn, tagsColumn, projectsColumn, rowB64Column, inputB64Column], postRender: postRender, deleteRows: true, columns: columns, filter: filter});
}