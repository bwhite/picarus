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