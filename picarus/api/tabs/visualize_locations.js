function render_visualize_locations() {
    row_selector($('#rowPrefixDrop'), $('#startRow'), $('#stopRow'));
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
        var latitude = encode_id('meta:latitude');
        var longitude = encode_id('meta:longitude');
        button_confirm_click_reset($('#removeButton'));
        images = new PicarusImages();
        function maps_success(row, columns) {
            columns.row = row;
            var curLat = base64.decode(columns[latitude]);
            var curLong = base64.decode(columns[longitude]);
            if (filter_lat_long(Number(curLat), Number(curLong))) {
                return;
            }
            images.add(new PicarusImage(columns));
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
                centerLat = Number(base64.decode(images.at(0).get(latitude)));
                centerLong = Number(base64.decode(images.at(0).get(longitude)));
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
                var lat = Number(base64.decode(x.get(latitude)));
                var log = Number(base64.decode(x.get(longitude)));
                new google.maps.Marker({position: new google.maps.LatLng(lat, lon), map: map});
            });
        }
        picarus_api_data_scanner("images", encode_id(unescape($('#startRow').val())), encode_id(unescape($('#stopRow').val())), [latitude, longitude], {success: maps_success, done: maps_done});
    })
}