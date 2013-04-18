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
                console.log(sz);
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
        var modelKey = $('#model_select').find(":selected").val();
        function success_func(result) {
            console.log('Blah');
            $('#imagefile').parent().html($('#imagefile').parent().html());
            $('#imagefile').change(fileChange);
            var outputType = models.get(modelKey).pescape('meta:output_type');
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
            console.log('Blah3');
            debug_response = response;
            PICARUS.postRow(table, response.row, 'i/chain', modelKey, {success: success_func})
        }
        var table = 'images';
        var data = {};
        data['data:image'] = $('#imagefile')[0].files[0];
        PICARUS.postTable(table, data, {success: upload_func})
        $('#results').html('');
    }
    $('#imagefile').change(fileChange);
}