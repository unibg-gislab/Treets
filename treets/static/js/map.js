mapboxgl.accessToken = 'pk.eyJ1Ijoibmljb2xhOTMiLCJhIjoiY2l2Y2ozYnZ5MDBocTJ5bzZiM284NGkyMiJ9.4VUvTxBv0zqgjY7t3JTFOQ';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v9',
    center: [9.13734351262877, 45.137451890638886],
    zoom: 6
});

map.addControl(new mapboxgl.NavigationControl());

map.on('dblclick', function (e) {
    //document.getElementById('current-coordinates').innerHTML =
        // e.point is the x, y coordinates of the mousemove event relative
        // to the top-left corner of the map
        //JSON.stringify(e.point) + "<br>" +
        // e.lngLat is the longitude, latitude geographical position of the event
    //   JSON.stringify(e.lngLat);
    lat = JSON.parse(JSON.stringify(e.lngLat)).lat.toFixed(6);
    lng = JSON.parse(JSON.stringify(e.lngLat)).lng.toFixed(6);
    document.getElementById("lat").value = lat;
    document.getElementById("lon").value = lng;
    document.getElementById("lat2").value = lat;
    document.getElementById("lon2").value = lng;
});

map.on('mousemove', function (e) {
    lat = JSON.parse(JSON.stringify(e.lngLat)).lat.toFixed(6);
    lng = JSON.parse(JSON.stringify(e.lngLat)).lng.toFixed(6);
    document.getElementById("current-coords").innerHTML = lat.toString() + ', ' + lng.toString();
});

function showCircle(){
    var lat = document.getElementById("lat").value;
    var lon = document.getElementById("lon").value;
    var radius = document.getElementById("radius").value;

    if(typeof(map.getSource("polygon")) == "undefined")
        map.addSource("polygon", createGeoJSONCircle([parseFloat(lon), parseFloat(lat)], parseFloat(radius)));
    else
        map.getSource("polygon").setData(createGeoJSONCircle([parseFloat(lon), parseFloat(lat)], parseFloat(radius)).data);

    map.addLayer({
        "id": "polygon",
        "type": "fill",
        "source": "polygon",
        "layout": {},
        "paint": {
            "fill-color": "blue",
            "fill-opacity": 0.6
        }
    });
}

var createGeoJSONCircle = function(center, radiusInKm, points) {
    if(!points) points = 64;

    var coords = {
        latitude: center[1],
        longitude: center[0]
    };
    var km = radiusInKm;

    var ret = [];
    var distanceX = km/(111.320*Math.cos(coords.latitude*Math.PI/180));
    var distanceY = km/110.574;

    var theta, x, y;
    for(var i=0; i<points; i++) {
        theta = (i/points)*(2*Math.PI);
        x = distanceX*Math.cos(theta);
        y = distanceY*Math.sin(theta);

        ret.push([coords.longitude+x, coords.latitude+y]);
    }
    ret.push(ret[0]);

    return {
        "type": "geojson",
        "data": {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [ret]
                }
            }]
        }
    };
};


function getJSON(url, callback) {
    $.ajax({
      url: url,
      type: 'GET',
      cache: "false",
      dataType: 'jsonp',
      success: function(data){
            $.getScript ( '//platform.twitter.com/widgets.js', callback(data));
        },
      error: callback
    });
}

function hashCode(str) { // java String#hashCode
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
       hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
} 

function intToRGB(i){
    var c = (i & 0x00FFFFFF)
        .toString(16)
        .toUpperCase();

    return "00000".substring(0, 6 - c.length) + c;
}

// When a click event occurs near a place, open a popup at the location of
// the feature, with description HTML from its properties.
map.on('click', function (e) {
    if(map.popup){
        map.popup._closeButton.click()
    }
    var features = map.queryRenderedFeatures(e.point, { layers: ['tweets', 'traces']});

    if (!features.length) {
        return;
    }
    feature = undefined
    for (var i = features.length - 1; i >= 0; i--) {
        if (features[i].properties !== undefined){
            feature = features[i];
            break;
        }
    }

    if (feature.layer.id == 'traces')
    {
        popupHTML = '<div class="popup-title"><center><h4>' + feature.properties.userName + '</h4></ center></div><div># of Tweets: ' + feature.properties.count + '</div>'
        popupHTML += '</br><form action="/treets/export" method="post">\
                                <button type="submit" class="btn btn-default" name="export" value="'+ feature.properties.userName +'">Export</button>\
                            </form>'
        map.popup = new mapboxgl.Popup()
            .setLngLat(e.lngLat)
            .setHTML(popupHTML)
            .addTo(map);
        return;

    }
    //try to retrieve and show original tweet
    res = {};
    twurl = 'https://publish.twitter.com/oembed?url=https://twitter.com/' + feature.properties.userName + '/status/' + feature.properties._id

    res = getJSON(twurl, function(data){
        if (data.html != undefined) {
            popupHTML = data.html
        }
        else{
            popupHTML = '<div class="popup-title"><center><h4>' + feature.properties.userName + '</h4></ center></div><blockquote class="twitter-tweet" data-lang="it">' + feature.properties.textMessage + '</blockquote>'
        }
        map.popup = new mapboxgl.Popup()
            .setLngLat(e.lngLat)
            .setHTML(popupHTML)
            .addTo(map);
    });
});

// Use the same approach as above to indicate that the symbols are clickable
// by changing the cursor style to 'pointer'.
map.on('mousemove', function (e) {
    // FIXME
    var features = map.queryRenderedFeatures(e.point, { layers: ['tweets', 'traces']});
    if (features.length){
	    map.getCanvas().style.cursor = (features.length) ? 'pointer' : '';
	}
});
