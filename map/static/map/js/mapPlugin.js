(function ($) {
    $.extend({
        setMap: function (options) {

            // Default settings.
            var settings = $.extend({
                target: "map",
                zoom: 2,
                centerTo: [30, 30],
                legendKey: 'intention'
            }, options);

            var mapInstance = this;

            // use this.setLegendKey() to switch currently active legend.
            mapInstance.legendKey = options.legendKey;
            mapInstance.countryLayer = null;

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

            // Layer and source holding countries.
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

            // Draw deals per country with all properties in the geojson.
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

                    // Copy the properties of the country, except the geometry
                    var properties = country.getProperties();
                    delete properties.geometry;

                    var countryInfoPoint = new ol.Feature(new ol.geom.Point(
                            ol.proj.fromLonLat([lat, lon], "EPSG:4326")));
                    countryInfoPoint.setProperties(properties);

                    dealsSource.addFeature(countryInfoPoint);
                });
            };

            /**
             * Prepare a data array based on the feature properties.
             *
             * @param features: A list of features (in the current cluster)
             * @returns {Array}
             */
            var prepareData = function(features) {

                // Collect all possible values
                var data = [];
                $.each(options.legend[mapInstance.legendKey].attributes, function(i, d) {
                    data.push({
                        color: d.color,
                        id: d.id,
                        count: 0
                    });
                });

                // Update "count" of each value based on the feature's values.
                $.each(features, function(index, feature) {
                    var properties = feature.getProperties()[mapInstance.legendKey];
                    if (!properties) return;

                    for (var prop in properties) {
                        if (properties.hasOwnProperty(prop)) {
                            var searchProp = $.grep(data, function(e) { return e.id == prop; });
                            if (searchProp.length != 1) {
                                break;
                            }
                            searchProp[0].count += properties[prop];
                        }
                    }
                });
                return data;
            };

            // Layer and source for the deals per country. All deals are
            // clustered and displayed in the 'centre' of the country.
            var dealsPerCountrySource = new ol.source.Vector();
            var dealsPerCountryCluster = new ol.source.Cluster({
                source: dealsPerCountrySource,
                distance: 50
            });

            // Draw a clustered layer with the properties from the current
            // legend as 'svg-doghnut' surrounding the cluster point.
            function getCountryClusterLayer() {
                return new ol.layer.Vector({
                    source: dealsPerCountryCluster,
                    style: function (feature) {

                        var data = prepareData(feature.get('features'));

                        // Calculate total
                        var total = 0;
                        $.each(data, function (i, d) {
                            total += d.count;
                        });

                        var size = feature.get('features').length;

                        // TODO: Using a fix radius for now
                        var radius = 3;

                        // SVG and basic circle
                        var svg = [
                            '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="30px" height="30px" viewBox="0 0 42 42" enable-background="new 0 0 30 30" xml:space="preserve">',
                            // Basic circle
                            '<circle class="donut-hole" cx="21" cy="21" r="15.91549430918954" fill="#fff"></circle>',
                            '<circle class="donut-ring" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#d2d3d4" stroke-width="3"></circle>'
                        ];

                        var defaultOffset = 25; // To make chart start at top (12:00), not right (3:00).
                        var totalOffsets = 0;
                        $.each(data, function (index, data) {
                            var offset = 100 - totalOffsets + defaultOffset;
                            var currValue = data.count / total * 100;
                            var currRemainder = 100 - currValue;
                            var currAttr = $.grep(options.legend[mapInstance.legendKey].attributes, function (e) {
                                return e.id == data.id;
                            });
                            var currColor = 'silver';
                            if (currAttr.length == 1) {
                                currColor = currAttr[0].color;
                            }
                            totalOffsets += currValue;

                            svg.push('<circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="' + currColor + '" stroke-width="5" stroke-dasharray="' + currValue + ' ' + currRemainder + '" stroke-dashoffset="' + offset + '"></circle>');
                        });
                        svg.push('</svg>');
                        var clusterSVG = new Image();
                        clusterSVG.src = 'data:image/svg+xml,' + escape(svg.join(''));

                        return new ol.style.Style({
                            image: new ol.style.Icon({
                                img: clusterSVG,
                                imgSize: [30, 30]
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
            }

            // Redraw the layer with the deals per country, with the current
            // legend as properties.
            this.setDealsPerCountryLayer = function() {
                if (this.countryLayer) {
                    map.removeLayer(this.countryLayer);
                }
                this.countryLayer = getCountryClusterLayer();
                map.addLayer(this.countryLayer);
            };

            // Load geojson from countries-api and display data.
            this.loadCountries = function() {
                $.ajax(settings.deals_url).then(function (response) {
                    var geojsonFormat = new ol.format.GeoJSON();
                    var features = geojsonFormat.readFeatures(response,
                        {featureProjection: "EPSG:3857"}
                    );
                    countrySource.addFeatures(features);
                    drawCountryInformation(features, dealsPerCountrySource);
                });
            };

            // change the legend and reload the layer with deals.
            this.setLegendKey = function(legendKey) {
                this.legendKey = legendKey;
                // maybe: cache layers in an object.
                this.setDealsPerCountryLayer();
            };

            return this;
        }
    });
})(jQuery);
