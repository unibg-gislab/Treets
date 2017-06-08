mapboxgl.accessToken = 'pk.eyJ1Ijoibmljb2xhOTMiLCJhIjoiY2l2Y2ozYnZ5MDBocTJ5bzZiM284NGkyMiJ9.4VUvTxBv0zqgjY7t3JTFOQ';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/dark-v9',
    center: [9.13734351262877, 45.137451890638886],
    zoom: 6
});

map.on('dblclick', function (e) {
    //document.getElementById('current-coordinates').innerHTML =
        // e.point is the x, y coordinates of the mousemove event relative
        // to the top-left corner of the map
        //JSON.stringify(e.point) + "<br>" +
        // e.lngLat is the longitude, latitude geographical position of the event
    //   JSON.stringify(e.lngLat);
    document.getElementById("lat").value = JSON.parse(JSON.stringify(e.lngLat)).lat;
    document.getElementById("lon").value = JSON.parse(JSON.stringify(e.lngLat)).lng;
    document.getElementById("current-lat").value = JSON.parse(JSON.stringify(e.lngLat)).lat;
    document.getElementById("current-lon").value = JSON.parse(JSON.stringify(e.lngLat)).lng;
});

map.on('mousemove', function (e) {
    document.getElementById("current-lat").value = JSON.parse(JSON.stringify(e.lngLat)).lat;
    document.getElementById("current-lon").value = JSON.parse(JSON.stringify(e.lngLat)).lng;
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



// When a click event occurs near a place, open a popup at the location of
// the feature, with description HTML from its properties.
map.on('click', function (e) {
    if(map.popup){
        map.popup._closeButton.click()
    }
    var features = map.queryRenderedFeatures(e.point, { layers: ['tweets']});

    if (!features.length) {
        return;
    }

    feature = undefined;
    for (var i = features.length - 1; i >= 0; i--) {
        if (features[i].properties !== undefined){
            feature = features[i];
            break;
        }
    }

    // var feature = features[features.length - 1];

    // Populate the popup and set its coordinates
    // based on the feature found.
    map.popup = new mapboxgl.Popup()
        .setLngLat(e.lngLat)
        .setHTML('<div class="popup-title"><center><h4>' + feature.properties.userName+ '</h4></ center></div><div>' + feature.properties.textMessage + '</div>')
        .addTo(map);
});

// Use the same approach as above to indicate that the symbols are clickable
// by changing the cursor style to 'pointer'.
map.on('mousemove', function (e) {
    var features = map.queryRenderedFeatures(e.point, { layers: ['tweets']});
    if (features.length){
	    map.getCanvas().style.cursor = (features.length) ? 'pointer' : '';
	}
});
