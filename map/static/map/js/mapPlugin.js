(function ($) {
    $.extend({
        setMap: function (options) {
            // Default settings.
            var settings = $.extend({
                target: "map",
                zoom: 2,
                centerTo: [30, 30]
            }, options);

            // initialize map
            var map = new ol.Map({
                target: settings.target,
                layers: [
                    new ol.layer.Tile({
                        source: new ol.source.OSM()
                    })
                ],
                view: new ol.View({
                    center: ol.proj.fromLonLat(settings.centerTo),
                    zoom: settings.zoom
                })
            });

            // Layer and source holding countries, including aggregated deals.
            // These deals are clustered and shown in the middle of each
            // country.
            var countrySource = new ol.source.Vector();
            var countryLayer = new ol.layer.Vector({
                source: countrySource,
                style: new ol.style.Style({
                    fill: new ol.style.Fill({
                        color: [252, 148, 31, 0.2]
                    }),
                    stroke: new ol.style.Stroke({
                        color: [252, 148, 31, 1],
                        width: 2,
                        lineCap: "round"
                    })
                })
            });
            map.addLayer(countryLayer);

            var drawCountryInformation = function (features, dealsSource) {
                $.each(features, function (key, country) {
                    // extent.getCenter() returns undefined with ol 4.0, so
                    // calculate it manually.
                    var definedCentre = country.get('centre_coordinates');
                    if (definedCentre) {
                        var lat = definedCentre[0];
                        var lon = definedCentre[1];
                    } else {
                        var extent = country.getGeometry().getExtent();
                        var lat = extent[0] + (extent[2] - extent[0]) / 2;
                        var lon = extent[1] + (extent[3] - extent[1]) / 2;
                    }
                    dealsSource.addFeature(
                        new ol.Feature(new ol.geom.Point(
                            ol.proj.fromLonLat([lat, lon], "EPSG:4326")
                            )
                        )
                    )
                });
            };

            // Load geojson from countries-api and display data.
            this.loadCountries = function() {
                $.ajax(settings.deals_url).then(function (response) {
                    var geojsonFormat = new ol.format.GeoJSON();
                    var features = geojsonFormat.readFeatures(response,
                        {featureProjection: "EPSG:3857"}
                    );
                    countrySource.addFeatures(features);
                    drawCountryInformation(features, dealsSource);
                });
            };

            // Layer and source for the deals per country. All deals are
            // clustered and displayed in the 'centre' of the country.
            var dealsSource = new ol.source.Vector();
            var dealsCluster = new ol.source.Cluster({
                source: dealsSource,
                distance: 50
            });
            var dealsLayer = new ol.layer.Vector({
                source: dealsCluster,
                style: function (feature) {
                    var size = feature.get('features').length;
                    var radius = size * 3;
                    // a simple example, but the svg is created depending on
                    // some properties from the features.
                    var svg = '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="30px" height="30px" viewBox="0 0 30 30" enable-background="new 0 0 30 30" xml:space="preserve">' +
                          '<circle class="donut-hole" cx="21" cy="21" r="' + radius + '" fill="#fff"></circle>' +
                          '<circle class="donut-ring" cx="21" cy="21" r="' + radius + '" fill="transparent" stroke="#d2d3d4" stroke-width="3"></circle>' +
                          '<circle class="donut-segment" cx="21" cy="21" r="' + radius + '" fill="transparent" stroke="#ce4b99" stroke-width="3" stroke-dasharray="85 15" stroke-dashoffset="0"></circle>' +
                        '</svg>';
                    var clusterSVG = new Image();
                    clusterSVG.src = 'data:image/svg+xml,' + escape(svg);

                    return new ol.style.Style({
                        image: new ol.style.Icon({
                            img: clusterSVG,
                            imgSize:[30,30]
                        }),
                        text: new ol.style.Text({
                            text: size.toString(),
                            fill: new ol.style.Fill({
                                color: '#000'
                            })
                        })
                    });
                }
            });
            map.addLayer(dealsLayer);

            return this;
        }
    });
})(jQuery);
