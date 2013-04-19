function render_models_list() {
    var columns = ['meta:name', 'meta:input_type', 'meta:output_type', 'row', 'meta:creation_time', 'meta:input',
                   'meta:model_link_size', 'meta:model_chain_size', 'meta:factory_info'];
    var columns_model = ['meta:'];
    results = new Picarus2Rows([], {'table': 'models', columns: columns_model});
    var takeoutColumn = {header: "Takeout", getFormatted: function() {
        return Mustache.render("<a class='takeout_link' row='{{row}}'>Link</a>/<a class='takeout_chain' row='{{row}}'>Chain</a>", {row: encode_id(this.get('row'))});
    }};
    var tagsColumn = {header: "Tags", className: "models-tags", getFormatted: function() { return this.escape('meta:tags') + '<span style="font-size:5px"><a class="modal_link_tags" row="' + encode_id(this.get('row')) + '">edit</a></span>'}};
    var notesColumn = {header: "Notes", className: "models-notes", getFormatted: function() { return this.escape('meta:notes') + '<span style="font-size:5px"><a class="modal_link_notes" row="' + encode_id(this.get('row')) + '">edit</a></span>'}};
    function postRender() {
        function process_takeout(row, model_chunks_column, model_column, model_type) {
            function takeoutSuccess(response) {
                var chunks = _.map(response, function (v, k) {
                    return [Number(k.split('-')[1]), v];
                }).sort();
                var model = _.map(chunks, function (v, k) {
                    return v[1];
                }).join('');
                var curSha1 = CryptoJS.SHA1(CryptoJS.enc.Base64.parse(base64.encode(model))).toString();
                var trueSha1 = results.get(row).escape('meta:model_' + model_type + '_sha1');
                if (curSha1 === trueSha1) {
                    var modelByteArray = new Uint8Array(model.length);
                    for (var i = 0; i < model.length; i++) {
                        modelByteArray[i] = model.charCodeAt(i) & 0xff;
                    }
                    var blob = new Blob([modelByteArray]);
                    saveAs(blob, 'picarus-model-' + row + '.sha1-' +  trueSha1 + '.' + model_type + '.msgpack');
                } else {
                    alert("Model SHA1 doesn't match!");
                }
            }
            var num_chunks = Number(results.get(row).escape(model_chunks_column));
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
                var model = results.get(row);
                $('#modal_content').val(model.escape(col));
                $('#save_button').unbind();
                $('#save_button').click(function () {
                    var attributes = {};
                    attributes[col] = $('#modal_content').val();
                    model.save(attributes, {patch: true});
                    $('#myModal').modal('hide');
                });
                $('#myModal').modal('show')
            })
        }
        setup_modal($('.modal_link_notes'), 'meta:notes');
        setup_modal($('.modal_link_tags'), 'meta:tags');
    }
    new RowsView({collection: results, el: $('#results'), extraColumns: [takeoutColumn, notesColumn, tagsColumn], postRender: postRender, deleteRows: true, columns: columns});
    results.fetch();
}