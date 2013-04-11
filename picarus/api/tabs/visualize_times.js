function render_visualize_times() {
    google_visualization_load(render_visualize_times_loaded);
}

function render_visualize_times_loaded() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
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
        var timeColumn = encode_id('meta:dateupload');
        images = new PicarusImages();
        function time_success(row, columns) {
            columns.row = row;
            images.add(new PicarusImage(columns));
        }
        function time_done() {
            years = [];
            months = [];
            hours = [];
            days = [];
            // TODO: FInish visual
            images.each(function (x) {
                var curTime = Number(base64.decode(x.get(timeColumn)));
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
        picarus_api_data_scanner("images", encode_id(unescape($('#startRow').val())), encode_id(unescape($('#stopRow').val())), [timeColumn], {success: time_success, done: time_done});
    })
}