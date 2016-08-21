$(document).ready(function () {
    (function() {
        'use strict';

        var LEGEND_COLORS = {
            'Geospatial Accuracy': {
                'better than 100m': '#0f0',
                '100m to 1km': '#0a0',
                '1km to 10km': '#00f',
                '10km to 100km': '#b00',
                'worse than 100km': '#700'
            },
            'Negotiation Status': {
                'Contract canceled': '#0f0',
                'Negotiations failed': '#00f',
                'Contract signed': '#0a0',
                'Oral agreement': '#b00',
                'Expression of interest': '#500',
                'Under negotiation': '#700'
            },
            'Deal Intention': {
                'Agriculture': '#1D6914',
                'Forestry': '#2A4BD7',
                'Conservation': '#575757',
                'Industry': '#AD2323',
                'Renewable Energy': '#81C57A',
                'Tourism': '#9DAFFF',
                'Other': '#8126C0',
                'Resource extraction': '#814A19',
                'Undefined': '#FF0000'
            }
        };
        var AREA_COLORS = {  // Back, Border
            'Current area in operation (ha)': ['rgba(0, 0, 196, 0.4)', '#007'],
            'Contract area (ha)': ['rgba(128, 128, 128, 0.6)', '#575757'],
            'Intended area (ha)': ['rgba(0, 196, 0, 0.6)', '#0a0']
        };
        var DEAL_VARIABLES = {
            'accuracy': 'Geospatial Accuracy',
            'negotiation_status': 'Negotiation Status',
            'intention': 'Deal Intention'
        };

        var pointImage = new ol.style.Circle({
            radius: 5,
            fill: null,
            stroke: new ol.style.Stroke({
                color: 'red',
                width: 1
            })
        });

        var geometryStyles = {
            'Point': [new ol.style.Style({
                image: pointImage
            })],
            'LineString': [new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'green',
                    width: 1
                })
            })],
            'MultiLineString': [new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'green',
                    width: 1
                })
            })],
            'MultiPoint': [new ol.style.Style({
                image: pointImage
            })],
            'MultiPolygon': [new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'yellow',
                    width: 1
                }),
                fill: new ol.style.Fill({
                    color: 'rgba(255, 255, 0, 0.1)'
                })
            })],
            'Polygon': [new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'blue',
                    lineDash: [4],
                    width: 3
                }),
                fill: new ol.style.Fill({
                    color: 'rgba(0, 0, 255, 0.1)'
                })
            })],
            'GeometryCollection': [new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'magenta',
                    width: 2
                }),
                fill: new ol.style.Fill({
                    color: 'magenta'
                }),
                image: new ol.style.Circle({
                    radius: 10,
                    fill: null,
                    stroke: new ol.style.Stroke({
                        color: 'magenta'
                    })
                })
            })],
            'Circle': [new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'red',
                    width: 2
                }),
                fill: new ol.style.Fill({
                    color: 'rgba(255,0,0,0.2)'
                })
            })]
        };

        function GlobalMapWidget(options) {
            var superOptions = {
                disableDrawing: true,
                enableFullscreen: true,
                initialLayer: 'osm',
                geomName: 'Collection'
            }
            for (var opt in options) {
                superOptions[opt] = options[opt];
            }
            MapWidget.call(this, superOptions);

            this.countryThreshold = 4;
            this.currentDealVariable = 'intention';

            this.intendedAreaFeatures = new ol.Collection();
            this.productionAreaFeatures = new ol.Collection();

            this.markerSource = new ol.source.Vector();
            this.countriesSource = new ol.source.Vector();
            this.clusterSource = new ol.source.Cluster({
                distance: 50,
                source: this.markerSource
            });

            this.intendedAreaSource = new ol.source.Vector({
                features: this.intendedAreaFeatures
            });
            this.productionAreaSource = new ol.source.Vector({
                features: this.productionAreaFeatures
            });

            this.geoJSON = new ol.format.GeoJSON();
        }
        ol.inherits(GlobalMapWidget, MapWidget);

        GlobalMapWidget.prototype.initPopup = function() {
            var container = jQuery('#' + this.options.popupId);
            // TODO: make this a class to allow multiples
            var content = container.children('#popup-content');
            var closer = container.children('.popup-closer');

            var popupOverlay = new ol.Overlay({
                element: container.get(o),
                autoPan: true,
                autoPanAnimation: {
                    duration: 250
                }
            });
            var closePopup = function(event) {
                event.preventDefault();
                popupOverlay.setPosition(undefined);
                closer.blur();
            };
            closer.on('click', closePopup);
        };

        GlobalMapWidget.prototype.getLayers = function(baseLayers) {
            var layers = baseLayers || this.getBaseLayers();
            var contextGroup = new ol.layer.Group({
                title: 'Context Layers',
                layers: this.getContextLayers()
            });
            layers.push(contextGroup);

            var dealsGroup = new ol.layer.Group({
                title: 'Deals',
                layers: [
                    new ol.layer.Vector({
                        title: 'Intended area (ha)',
                        visible: true,
                        source: this.intendedAreaSource,
                        style: this.getFeatureStyle
                    }),
                    new ol.layer.Vector({
                        title: 'Current area in operation (ha)',
                        visible: true,
                        source: this.productionAreaSource,
                        style: this.getFeatureStyle
                    }),
                    new ol.layer.Vector({
                        title: 'Markers',
                        source: this.clusterSource,
                        style: this.getClusterStyle
                    }),
                    new ol.layer.Vector({
                        title: 'Countries',
                        source: this.countriesSource,
                        visible: true,
                        style: new ol.style.Style({
                            image: new ol.style.Circle({
                                radius: 10,
                                stroke: new ol.style.Stroke({
                                    color: '#fff'
                                }),
                                fill: new ol.style.Fill({
                                    color: '#fc941f'
                                })
                            })
                        })
                    })
                ]
            });
            layers.push(dealsGroup);

            return layers;
        }

        GlobalMapWidget.prototype.getFeatureStyle = function(feature, resolution) {
            var geometryType = feature.getGeometry().getType();
            var styles = [];

            if (geometryType in geometryStyles) {
                styles = geometryStyles[geometryType];
            }
            else {
                // assume a polygon
                styles = [new ol.style.Style({
                    stroke: new ol.style.Stroke({
                        color: 'blue',
                        lineDash: [4],
                        width: 3
                    }),
                    fill: new ol.style.Fill({
                        color: 'rgba(0, 0, 255, 0.1)'
                    })
                })];
            }
            return styles;
        };

        GlobalMapWidget.prototype.getClusterStyle = function (feature, resolution) {
            var size = feature.get('features').length;
            //Give a color to each Intention of Investment, only for single points
            // PROBLEM : how to clustered the points by color?

            var color = "";
            var legend_image = {};
            var legend_text = {};
            var style = {};

            if (size > 1) {
                color = '#fc941f';

                var radius = size + 10;

                if (radius > 30) {
                    radius = 30;
                }
                else if (radius < 10) {
                    radius = 10;
                }

                legend_image = new ol.style.Circle({
                    radius: radius,
                    stroke: new ol.style.Stroke({
                        color: '#fff'
                    }),
                    fill: new ol.style.Fill({
                        color: color
                    })
                });

                legend_text = new ol.style.Text({
                    text: size.toString(),
                    fill: new ol.style.Fill({
                        color: '#fff'
                    })
                });

                style = [new ol.style.Style({
                    image: legend_image,
                    text: legend_text
                })];

            } else {
                feature = feature.get('features')[0];
                var classifier = feature.attributes[fieldnames[currentVariable]];
                //console.log(classifier)

                if (classifier in detailviews[currentVariable]) {
                    color = detailviews[currentVariable][classifier];
                } else {
                    color = '#000';
                }

                legend_text = new ol.style.Text({
                    text: '\uf041',
                    font: 'normal 36px landmatrix',
                    textBaseline: 'Bottom',
                    fill: new ol.style.Fill({
                        color: color
                    })
                });

                style = [new ol.style.Style({
                    text: legend_text
                })];

            }

            return style;
        }

        window.GlobalMapWidget = GlobalMapWidget;
    })();
});