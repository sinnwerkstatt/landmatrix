(function ($) {
    $.extend({
        setMap: function (options) {

            // Default settings.
            var settings = $.extend({
                target: "map",
                zoom: 6,
                centerTo: [-5, 20],
                legendKey: 'intention',
                visibleLayer: 'countries'
            }, options);

            // Chart settings. Also needed to adjust clustering sensibility.
            var chartSize = 100;
            var donutWidth = 7;
            var fontSize = 1.25;

            var mapInstance = this;

            // use this.setLegendKey() to switch currently active legend.
            mapInstance.legendKey = options.legendKey;
            mapInstance.dealsPerCountryLayer = null;

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
                }),
                visible: settings.visibleLayer == 'countries'
            });
            map.addLayer(countryLayer);

            // Layer and source for the deals per country. All deals are
            // clustered and displayed in the 'centre' of the country.
            var dealsPerCountrySource = new ol.source.Vector();
            var dealsPerCountryCluster = new ol.source.Cluster({
                source: dealsPerCountrySource,
                distance: chartSize / 2
            });

            // Layer and source for the deals. All deals are clustered.
            var dealsSource = new ol.source.Vector();
            var dealsCluster = new ol.source.Cluster({
                source: dealsSource,
                distance: chartSize / 2
            });
            
            // Overly for the container with detailed information after a click
            var featureDetailsElement = $("#" + settings.featureDetailsElement);

            // Draw deals per country with all properties in the geojson.
            var drawCountryInformation = function (features, countryDealsSource) {
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

                    countryDealsSource.addFeature(countryInfoPoint);
                });
            };

            /**
             * Prepare a data array based on the country feature properties.
             *
             * @param features: A list of country features (in the current cluster)
             * @returns {Array}
             */
            function prepareCountryClusterData(features) {

                var data = getBasicClusterData();

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
            }

            /**
             * Prepare a data array based on the deal feature properties.
             *
             * @param features: A list of deal features (in the current cluster)
             * @returns {Array}
             */
            function prepareDealClusterData(features) {

                var data = getBasicClusterData();
                
                // Update "count" of each value based on the feature's values.
                $.each(features, function(index, feature) {
                    var properties = feature.getProperties()[mapInstance.legendKey];
                    if (!properties) return;
                    
                    if (typeof properties === 'string') {
                        properties = [properties];
                    }

                    $.each(properties, function(i, prop) {
                        var searchProp = $.grep(data, function(e) { return e.id == prop; });
                        if (searchProp.length != 1) {
                            return;
                        }
                        searchProp[0].count += 1;
                    });
                });
                return data;
            }

            /**
             * Return an array with an object for each of the current legend
             * attributes. Count is set to 0.
             *
             * @returns {Array}
             */
            function getBasicClusterData() {
                // Collect all possible values
                var data = [];
                $.each(options.legend[mapInstance.legendKey].attributes, function(i, d) {
                    data.push({
                        color: d.color,
                        id: d.id,
                        count: 0
                    });
                });
                return data;
            }

            // Draw a clustered layer with the properties from the current
            // legend as 'svg-doghnut' surrounding the cluster point.
            function getCountryClusterLayer() {
                return new ol.layer.Vector({
                    source: dealsPerCountryCluster,
                    style: function (feature) {
                        var clusteredFeatures = feature.get('features');

                        var clusterSVG = new Image();
                        var clusterData = prepareCountryClusterData(clusteredFeatures);
                        clusterSVG.src = 'data:image/svg+xml,' + escape(getSvgChart(clusterData, 'countries'));

                        return getChartStyle(clusterSVG, clusteredFeatures);
                    },
                    visible: settings.visibleLayer == 'countries'
                });
            }

            // Draw a clustered layer with the properties from the current
            // legend as donut surrounding the cluster point.
            function getDealsClusterLayer() {
                return new ol.layer.Vector({
                    source: dealsCluster,
                    style: function(feature) {
                        var clusteredFeatures = feature.get('features');

                        var clusterSVG = new Image();
                        var clusterData = prepareDealClusterData(clusteredFeatures);
                        clusterSVG.src = 'data:image/svg+xml,' + escape(getSvgChart(clusterData, 'deals'));

                        return getChartStyle(clusterSVG, clusteredFeatures);
                    },
                    visible: settings.visibleLayer == 'deals'
                })
            }

            // Return the basic chart style for cluster: Use a SVG image icon 
            // and display number of features as text.
            function getChartStyle(clusterSVG, clusteredFeatures) {
                return new ol.style.Style({
                    image: new ol.style.Icon({
                        img: clusterSVG,
                        imgSize: [chartSize, chartSize]
                    }),
                    text: new ol.style.Text({
                        text: clusteredFeatures.length.toString(),
                        scale: fontSize,
                        fill: new ol.style.Fill({
                            color: '#222'
                        })
                    })
                });
            }

            // Return a SVG donut chart based on the feature's data.
            function getSvgChart(data, clusterType) {
                // Calculate total
                var total = 0;
                $.each(data, function (i, d) {
                    total += d.count;
                });

                var backgroundColor = clusterType == 'countries' ? '#f9de98' : '#fff';

                // SVG and basic circle
                var radius = chartSize / (2 * Math.PI);
                var svg = [
                    '<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="' + chartSize + 'px" height="' + chartSize + 'px" viewBox="0 0 ' + chartSize + ' ' + chartSize + '" enable-background="new 0 0 ' + chartSize + ' ' + chartSize + '" xml:space="preserve">',
                    // Basic circle
                    '<circle class="donut-hole" cx="' + chartSize/2 + '" cy="' + chartSize/2 + '" r="' + radius + '" fill="' + backgroundColor + '"></circle>',
                    '<circle class="donut-ring" cx="' + chartSize/2 + '" cy="' + chartSize/2 + '" r="' + radius + '" fill="transparent" stroke="#d2d3d4" stroke-width="' + donutWidth + '"></circle>'
                ];

                var defaultOffset = chartSize / 4; // To make chart start at top (12:00), not right (3:00).
                var totalOffsets = 0;
                $.each(data, function (index, data) {
                    var offset = chartSize - totalOffsets + defaultOffset;
                    var currValue = data.count / total * chartSize;
                    var currRemainder = chartSize - currValue;
                    var currAttr = $.grep(options.legend[mapInstance.legendKey].attributes, function (e) {
                        return e.id == data.id;
                    });
                    var currColor = "silver";
                    if (currAttr.length == 1) {
                        currColor = currAttr[0].color;
                    }
                    totalOffsets += currValue;

                    svg.push('<circle class="donut-segment" cx="' + chartSize/2 + '" cy="' + chartSize/2 + '" r="' + radius + '" fill="transparent" stroke="' + currColor + '" stroke-width="' + donutWidth + '" stroke-dasharray="' + currValue + ' ' + currRemainder + '" stroke-dashoffset="' + offset + '"></circle>');
                });
                svg.push('</svg>');
                return svg.join('');
            }

            function showFeatureDetails(event, features) {
                // load data from MapInfoDetailView
                $.ajax(settings.featureDetailsUrl, {
                    type: "POST",
                    data: JSON.stringify({
                        "features": new ol.format.GeoJSON().writeFeaturesObject(features),
                        "legendKey": mapInstance.legendKey
                    }),
                    contentType: "application/json; charset=utf-8"
                }).then(function(data) {
                    featureDetailsElement.html(data);
                    // update tabbed menu
                    settings.featureDetailsCallback(
                        featureDetailsElement.parent()
                    );
                });
            }

            // Display popover on click. Doubleclick should still zoom in.
            map.on("singleclick", function (event) {
                var feature = map.forEachFeatureAtPixel(event.pixel, function (feature, layer) {
                    // use 'active' layer (dealsPerCountry or allDeals) only.
                    // todo: get currently active layer.
                    if (layer == mapInstance.dealsPerCountryLayer) {
                        return feature;
                    }
                });
                if (feature) {
                    var features = feature.get("features");
                    showFeatureDetails(event, features[0])
                }
            });

            // Redraw the layer with the deals per country, with the current
            // legend as properties.
            this.setDealsPerCountryLayer = function() {
                if (this.dealsPerCountryLayer) {
                    map.removeLayer(this.dealsPerCountryLayer);
                }
                this.dealsPerCountryLayer = getCountryClusterLayer();
                map.addLayer(this.dealsPerCountryLayer);
            };

            // Redraw the layer with the deals, with the current legend as
            // properties.
            this.setDealsLayer = function() {
                if (this.dealsLayer) {
                    map.removeLayer(this.dealsLayer);
                }
                this.dealsLayer = getDealsClusterLayer();
                map.addLayer(this.dealsLayer);
            };

            // Load geojson from countries-api and display data.
            this.loadCountries = function() {
                $.ajax(settings.countriesUrl).then(function (response) {
                    var geojsonFormat = new ol.format.GeoJSON();
                    var features = geojsonFormat.readFeatures(response,
                        {featureProjection: "EPSG:3857"}
                    );
                    countrySource.addFeatures(features);
                    drawCountryInformation(features, dealsPerCountrySource);
                });
            };

            this.loadDeals = function() {
                $.ajax(settings.dealsUrl).then(function(response) {
                    var geojsonFormat = new ol.format.GeoJSON();
                    var features = geojsonFormat.readFeatures(response,
                        {featureProjection: "EPSG:3857"}
                    );
                    dealsSource.addFeatures(features);
                });
            };

            // change the legend and reload the layer with deals.
            this.setLegendKey = function(legendKey) {
                this.legendKey = legendKey;
                // maybe: cache layers in an object.
                this.setDealsPerCountryLayer();
                this.setDealsLayer();
            };

            /**
             * Change the currently visible layer.
             *
             * @param visibleLayer: str. Either "countries" or "deals".
             */
            this.toggleVisibleLayer = function(visibleLayer) {
                settings.visibleLayer = visibleLayer;
                var countriesVisible = visibleLayer == 'countries';
                this.dealsLayer.setVisible(!countriesVisible);
                countryLayer.setVisible(countriesVisible);
                this.dealsPerCountryLayer.setVisible(countriesVisible);
            };

            return this;
        }
    });
})(jQuery);
