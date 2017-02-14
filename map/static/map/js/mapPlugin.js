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

                    // Copy the properties of the country, except the geometry
                    var properties = country.getProperties();
                    delete properties.geometry;

                    var countryInfoPoint = new ol.Feature(new ol.geom.Point(
                            ol.proj.fromLonLat([lat, lon], "EPSG:4326")));
                    countryInfoPoint.setProperties(properties);

                    dealsSource.addFeature(countryInfoPoint);
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

            var currentProperty = 'implementation';

            /**
             * Prepare a data array based on the feature properties.
             *
             * @param features: A list of features (in the current cluster)
             * @returns {Array}
             */
            var prepareData = function(features) {

                var data = [];
                $.each(features, function(index, f) {
                    var properties = f.getProperties();
                    var dataProperties = properties[currentProperty];
                    if (!dataProperties) return;
                    
                    var entriesWithProperties = 0;
                    for (var k in dataProperties) {
                        if (dataProperties.hasOwnProperty(k)) {
                            var searchProp = $.grep(data, function(e){ return e.keyword == k; });
                            var propEl = {keyword: k, count: 0};
                            if (searchProp.length == 0) {
                                data.push(propEl);
                            } else {
                                propEl = searchProp[0];
                            }
                            propEl.count += dataProperties[k];
                        
                            entriesWithProperties += dataProperties[k];
                        }
                    }
                });
                return data;
            };

            // Layer and source for the deals per country. All deals are
            // clustered and displayed in the 'centre' of the country.
            var dealsSource = new ol.source.Vector();
            var dealsCluster = new ol.source.Cluster({
                source: dealsSource,
                distance: 50
            });

            var mapCategories = {
                'implementation': {
                    'startup': {},
                    'not_started': {},
                    'abandoned': {
                        // It is possible to overwrite colors
                        'color': 'yellow'
                    },
                    'in_operation': {},
                    'unknown': {}
                },
                'intention': {
                    'agriculture': {},
                    'renewable': {},
                    'forestry': {},
                    'conservation': {},
                    'tourism': {},
                    'other': {}
                }
            };
            
            var dealsLayer = new ol.layer.Vector({
                source: dealsCluster,
                style: function (feature) {
                    
                    var data = prepareData(feature.get('features'));

                    // Calculate total
                    var total = 0;
                    $.each(data, function(i, d) {
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
                    $.each(data, function(i, d) {
                        var offset = 100 - totalOffsets + defaultOffset;
                        var currValue = d.count / total * 100;

                        var currRemainder = 100 - currValue;

                        totalOffsets += currValue;

                        var currColor = mapCategories[currentProperty][d.keyword].color;

                        svg.push('<circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="' + currColor + '" stroke-width="3" stroke-dasharray="' + currValue + ' ' + currRemainder + '" stroke-dashoffset="' + offset + '"></circle>');
                    });
                    svg.push('</svg>');
                    var clusterSVG = new Image();
                    clusterSVG.src = 'data:image/svg+xml,' + escape(svg.join(''));

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
