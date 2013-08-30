function render_jobs_crawlFlickr() {
    row_selector($('#rowPrefixDrop'));
    $('#runButton').click(function () {
        button_running();
        var demo_class = $('#democlass').val();
        var demo_query = $('#demoquery').val();
        var row_start_stop = _.map($('#rowPrefixDrop').val().split(','), function (x) {
            return base64.decode(x);
        });
        if (demo_query.length == 0 && row_start_stop.length == 0) {
            display_alert('Must specify query and prefix');
            return;
        }
        var iters = parseInt($('#demoiters').val())
        if (isNaN(iters) || iters < 1 || iters > 10000) {
            display_alert('Iters must be 0 < x <= 10000');
            return;
        }
        $('#results').html('');
        /* Check input */
        var latitude = Number($('#demolat').val());
        var longitude = Number($('#demolon').val());
        var done = 0;


        function call_api(state) {
            var timeRadius = 60 * 60 * 24 * 30 * 12; // 12 months
            var p = {action: 'o/crawl/flickr', hasGeo: Number($('#demogeo').is(':checked')), query: state.query, uploadDateRadius: timeRadius, iterations: iters};
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
                $('#results').append('Crawl Finished : ' + state.query + '<br>');
                button_reset();
            }
            var graphDiv = $('<div>');
            $('#results').append(graphDiv);
            $('#results').append($('<br>'));
            PICARUS.postSlice('images', row_start_stop[0], row_start_stop[1], {success: _.partial(watchJob, {success: _.partial(updateJobStatus, graphDiv), done: success}), data: p});
        }
        call_api({className: demo_class, query: demo_query});
    });
}