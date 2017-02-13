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

            var drawCountryInformation = function (features, clusterSource) {
                $.each(features, function (key, country) {
                    // extent.getCenter() returns undefined with ol 3.20, so
                    // calculate it manually.
                    var extent = country.getGeometry().getExtent();
                    var lat = extent[0] + (extent[2] - extent[0]) / 2;
                    var lon = extent[1] + (extent[3] - extent[1]) / 2;
                    clusterSource.addFeature(
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

            // Layer and source for the detailed deals - all deals are clustered
            // and represented as a Point.
            var dealsSource = new ol.source.Vector();
            var dealsLayer = new ol.layer.Vector({
                source: dealsSource,
                style: new ol.style.Style({
                    image: new ol.style.Circle({
                        fill: new ol.style.Fill({
                            color: 'rgba(55, 200, 150, 0.5)'
                        }),
                        stroke: new ol.style.Stroke({
                            width: 1,
                            color: 'rgba(55, 200, 150, 0.8)'
                        }),
                        radius: 7
                    })
                })
            });
            map.addLayer(dealsLayer);

            return this;
        }
    });
})(jQuery);
