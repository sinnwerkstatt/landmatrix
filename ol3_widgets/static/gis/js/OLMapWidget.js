/* global ol, jQuery */

var GeometryTypeControl = function(opt_options) {
    'use strict';
    // Map control to switch type when geometry type is unknown
    var options = opt_options || {};

    var element = document.createElement('div');
    element.className = 'switch-type type-' + options.type + ' ol-control ol-unselectable';
    if (options.active) {
        element.className += " type-active";
    }

    var self = this;
    var switchType = function(e) {
        e.preventDefault();
        if (options.widget.currentGeometryType !== self) {
            options.widget.map.removeInteraction(options.widget.interactions.draw);
            options.widget.interactions.draw = new ol.interaction.Draw({
                features: options.widget.featureCollection,
                type: options.type
            });
            options.widget.map.addInteraction(options.widget.interactions.draw);
            var className = options.widget.currentGeometryType.element.className.replace(/ type-active/g, '');
            options.widget.currentGeometryType.element.className = className;
            options.widget.currentGeometryType = self;
            element.className += " type-active";
        }
    };

    element.addEventListener('click', switchType, false);
    element.addEventListener('touchstart', switchType, false);

    ol.control.Control.call(this, {
        element: element
    });
};
$(document).ready(function () {
    ol.inherits(GeometryTypeControl, ol.control.Control);

    // TODO: allow deleting individual features (#8972)
    (function() {
        'use strict';
        var jsonFormat = new ol.format.GeoJSON();

        function MapWidget(options) {
            this.map = null;
            this.interactions = {draw: null, modify: null};
            this.typeChoices = false;
            this.ready = false;

            // Default options
            this.options = {
                default_lat: 0,
                default_lon: 0,
                default_zoom: 12,
                isCollection: options.geom_name.indexOf('Multi') >= 0 || options.geom_name.indexOf('Collection') >= 0,
                boundLatField: null,
                boundLonField: null,
                boundLocationField: null,
                boundTargetCountryField: null,
                boundLevelOfAccuracyField: null,
            };

            // Altering using user-provided options
            for (var property in options) {
                if (options.hasOwnProperty(property)) {
                    this.options[property] = options[property];
                }
            }
            if (!options.base_layers) {
                this.options.base_layers = this.getBaseLayers();
            }

            this.map = this.createMap();

            this.featureCollection = new ol.Collection();
            this.featureOverlay = new ol.layer.Vector({
                map: this.map,
                source: new ol.source.Vector({
                    features: this.featureCollection,
                    useSpatialIndex: false // improve performance
                }),
                style: this.getFeatureStyle,
                updateWhileAnimating: true, // optional, for instant visual feedback
                updateWhileInteracting: true // optional, for instant visual feedback
            });

            // Populate and set handlers for the feature container
            var self = this;
            this.featureCollection.on('add', function(event) {
                var feature = event.element;
                feature.on('change', function() {
                    self.serializeFeatures();
                });
                if (self.ready) {
                    self.serializeFeatures();
                    if (!self.options.isCollection) {
                        self.disableDrawing(); // Only allow one feature at a time
                    }
                }
            });

            var initial_features = null;
            if (this.options.boundLatField && this.options.boundLonField) {
                var lat = parseFloat(this.options.boundLatField.val());
                var lon = parseFloat(this.options.boundLonField.val());
                if (lat && lon && lat != NaN && lon != NaN) {
                    var coordinates = this.getCoordinates(lat, lon);
                    var feature = new ol.Feature({
                        geometry: new ol.geom.Point(coordinates)
                    });
                    initial_features = [feature];
                }
            }
            else {
                var initial_value = document.getElementById(this.options.id).value;
                if (initial_value) {
                    initial_features = jsonFormat.readFeatures('{"type": "Feature", "geometry": ' + initial_value + '}');
                }
            }

            if (initial_features) {
                var extent = ol.extent.createEmpty();
                initial_features.forEach(function(feature) {
                    this.featureOverlay.getSource().addFeature(feature);
                    ol.extent.extend(extent, feature.getGeometry().getExtent());
                }, this);
                // Centering/zooming the map
                this.map.getView().fit(extent, this.map.getSize(), {maxZoom: this.options.default_zoom});
            } else {
                this.map.getView().setCenter(this.defaultCenter());
            }
            this.createInteractions();
            if (initial_features && !this.options.isCollection) {
                this.disableDrawing();
            }
            if (this.options.boundLonField || this.options.boundLatField ||
                this.options.boundTargetCountryField || this.options.boundLocationField ||
                this.options.boundLevelOfAccuracyField) {
                    this.interactions.draw.on('drawend', this.updateBoundFields, this);
                    this.interactions.modify.on('modifyend', this.updateBoundFields, this);
            }
            this.initLinkHandlers();
            this.initLayerSwitcher(true);

            this.ready = true;
        }

        MapWidget.prototype.createMap = function() {
            var map = new ol.Map({
                target: this.options.map_id,
                layers: this.options.base_layers,
                view: new ol.View({
                    zoom: this.options.default_zoom
                })
            });
            var olGM = new olgm.OLGoogleMaps({map: map});
            olGM.activate();

            return map;
        };

        MapWidget.prototype.createInteractions = function() {
            // Initialize the modify interaction
            this.interactions.modify = new ol.interaction.Modify({
                features: this.featureCollection,
                deleteCondition: function(event) {
                    return ol.events.condition.shiftKeyOnly(event) &&
                        ol.events.condition.singleClick(event);
                }
            });

            // Initialize the draw interaction
            var geomType = this.options.geom_name;
            if (geomType === "Unknown" || geomType === "GeometryCollection") {
                // Default to Point, but create icons to switch type
                geomType = "Point";
                this.currentGeometryType = new GeometryTypeControl({widget: this, type: "Point", active: true});
                this.map.addControl(this.currentGeometryType);
                this.map.addControl(new GeometryTypeControl({widget: this, type: "LineString", active: false}));
                this.map.addControl(new GeometryTypeControl({widget: this, type: "Polygon", active: false}));
                this.typeChoices = true;
            }
            this.interactions.draw = new ol.interaction.Draw({
                features: this.featureCollection,
                type: geomType
            });

            this.map.addInteraction(this.interactions.draw);
            this.map.addInteraction(this.interactions.modify);
        };

        MapWidget.prototype.defaultCenter = function() {
            if (this.options.map_srid) {
                return this.getCoordinates(
                    this.options.default_lat, this.options.default_lon);
            }
            else {
                return [this.options.default_lon, this.options.default_lat];
            }
        };

        MapWidget.prototype.enableDrawing = function() {
            this.interactions.draw.setActive(true);
            if (this.typeChoices) {
                // Show geometry type icons
                var divs = document.getElementsByClassName("switch-type");
                for (var i = 0; i !== divs.length; i++) {
                    divs[i].style.visibility = "visible";
                }
            }
        };

        MapWidget.prototype.disableDrawing = function() {
            if (this.interactions.draw) {
                this.interactions.draw.setActive(false);
                if (this.typeChoices) {
                    // Hide geometry type icons
                    var divs = document.getElementsByClassName("switch-type");
                    for (var i = 0; i !== divs.length; i++) {
                        divs[i].style.visibility = "hidden";
                    }
                }
            }
        };

        MapWidget.prototype.clearFeatures = function() {
            this.featureCollection.clear();
            // Empty textarea widget
            document.getElementById(this.options.id).value = '';
            this.enableDrawing();
        };

        MapWidget.prototype.serializeFeatures = function() {
            // Three use cases: GeometryCollection, multigeometries, and single geometry
            var geometry = null;
            var features = this.featureOverlay.getSource().getFeatures();
            if (this.options.isCollection) {
                if (this.options.geom_name === "GeometryCollection") {
                    var geometries = [];
                    for (var i = 0; i < features.length; i++) {
                        geometries.push(features[i].getGeometry());
                    }
                    geometry = new ol.geom.GeometryCollection(geometries);
                } else {
                    geometry = features[0].getGeometry().clone();
                    for (var j = 1; j < features.length; j++) {
                        switch(geometry.getType()) {
                            case "MultiPoint":
                                geometry.appendPoint(features[j].getGeometry().getPoint(0));
                                break;
                            case "MultiLineString":
                                geometry.appendLineString(features[j].getGeometry().getLineString(0));
                                break;
                            case "MultiPolygon":
                                geometry.appendPolygon(features[j].getGeometry().getPolygon(0));
                        }
                    }
                }
            } else {
                if (features[0]) {
                    geometry = features[0].getGeometry();
                }
            }
            document.getElementById(this.options.id).value = jsonFormat.writeGeometry(geometry);
        };


        MapWidget.prototype.getBaseLayers = function() {
            var baseLayers = [
                new ol.layer.Tile({
                    title: 'OpenStreetMap',
                    type: 'base',
                    visible: true,
                    source: new ol.source.OSM(),
                }),
                new olgm.layer.Google({
                    title: 'Satellite',
                    type: 'base',
                    visible: false,
                    mapTypeId: google.maps.MapTypeId.SATELLITE
                }),
                new olgm.layer.Google({
                    title: 'Terrain',
                    type: 'base',
                    visible: false,
                    mapTypeId: google.maps.MapTypeId.TERRAIN
                })
            ];

            return baseLayers;
        };

        MapWidget.prototype.getContextLayers = function() {
            var contextLayers = [
                // Global layers
                new ol.layer.Tile({
                    title: 'Accessibility<a href="/maplayers#global_cropland" class="toggle-tooltip noul" title="LEGENDPOPUP"><i class="lm lm-question-circle"> </i></a>',
                    source: new ol.source.TileWMS({
                        url: "http://sdi.cde.unibe.ch/geoserver/lo/wms",
                        params: {
                            'srs': 'EPSG%3a900913',
                            'layers': 'accessability' // Typo needed!
                        }
                    }),
                    visible: false,
                    opacity: 0.6
                }),
                new ol.layer.Tile({
                    title: 'Global Land Cover 2009<a href="/maplayers#global_cropland" class="toggle-tooltip noul" title="LEGENDPOPUP"><i class="lm lm-question-circle"> </i></a>',
                    source: new ol.source.TileWMS({
                        url: "http://sdi.cde.unibe.ch/geoserver/lo/wms",
                        params: {
                            'srs': 'EPSG%3a900913',
                            'layers': 'globcover_2009'
                        }
                    }),
                    visible: false,
                    opacity: 0.6
                }),
                new ol.layer.Tile({
                    title: 'Global Cropland<a href="/maplayers#global_cropland" class="toggle-tooltip noul" title="LEGENDPOPUP"><i class="lm lm-question-circle"> </i></a>',
                    source: new ol.source.TileWMS({
                        url: "http://sdi.cde.unibe.ch/geoserver/lo/wms",
                        params: {
                            'srs': 'EPSG%3a900913',
                            'layers': 'gl_cropland'
                        }
                    }),
                    visible: false,
                    opacity: 0.6
                }),
                new ol.layer.Tile({
                    title: 'Global Pasture Land<a href="/maplayers#global_cropland" class="toggle-tooltip noul" title="LEGENDPOPUP"><i class="lm lm-question-circle"> </i></a>',
                    source: new ol.source.TileWMS({
                        url: "http://sdi.cde.unibe.ch/geoserver/lo/wms",
                        params: {
                            'srs': 'EPSG%3a900913',
                            'layers': 'gl_pasture'
                        }
                    }),
                    visible: false,
                    opacity: 0.6
                }),
                // LAOS LOCAL LAYER! TODO!
                new ol.layer.Tile({
                    title: 'Incidence of poverty<a href="/maplayers#global_cropland" class="toggle-tooltip noul" title="LEGENDPOPUP"><i class="lm lm-question-circle"> </i></a>',
                    source: new ol.source.TileWMS({
                        url: "http://sdi.cde.unibe.ch/geoserver/gwc/service/wms",
                        params: {
                            "layers": "lo:laos_poverty_incidence",
                            "srs": "EPSG%3A900913"
                        }
                    }),
                    extent: [10018755, 181, 12801601, 3482189],
                    visible: false,
                    opacity: 0.7
                })
            ];

            return contextLayers;
        };

        MapWidget.prototype.getFeatureStyle = function(feature, resolution) {
            if (feature.getGeometry().getType() === 'Point') {
                var style = new ol.style.Style({
                    text: new ol.style.Text({
                        text: '\uf041',
                        font: 'normal 36px FontAwesome',
                        textBaseline: 'Bottom',
                        fill: new ol.style.Fill({
                          color: '#4bbb87'
                        })
                     })
                });
            }
            else {
                // assume a polygon
                var style = new ol.style.Style({
                    stroke: new ol.style.Stroke({
                        color: 'blue',
                        lineDash: [4],
                        width: 3
                    }),
                    fill: new ol.style.Fill({
                        color: 'rgba(0, 0, 255, 0.1)'
                    })
                });
            }
            return [style];
        };

        MapWidget.prototype.initLayerSwitcher = function(showByDefault) {
            var layerSwitcher = new ol.control.LayerSwitcher({
                tipLabel: 'Legend'
            });
            this.map.addControl(layerSwitcher);
            layerSwitcher.renderPanel();
            if (showByDefault) {
                layerSwitcher.showPanel();
            }
        };

        MapWidget.prototype.updateLocationField = function(results, status) {
            var address = results[0].formatted_address;
            if (address) {
                this.options.boundLocationField.val(address);
            };
        };

        MapWidget.prototype.updateTargetCountryField = function(results) {
            for (var i = 0; i < results[0].address_components.length; i++) {
                if (results[0].address_components[i].types.indexOf("country") != -1) {
                    var country = results[0].address_components[i].short_name;
                    // TODO: better way to do this.
                    this.options.boundTargetCountryField
                        .find('option')
                        .removeAttr("selected")
                        .filter("option[title='" + country + "']")
                        .attr('selected', 'selected');
                }
            }
        };

        MapWidget.prototype.updateLevelOfAccuracyField = function(results) {
            // TODO: implement? Not sure if we actually need this.
        };

        MapWidget.prototype.updateLatLongFields = function(coordinates) {
            this.options.boundLatField.val(coordinates[1]);
            this.options.boundLonField.val(coordinates[0]);
        };

        MapWidget.prototype.geocodeCoordinates = function(coordinates) {
            if (!this.hasOwnProperty('geocoder')) {
                this.geocoder = new google.maps.Geocoder();
            }
            var latLng = new google.maps.LatLng(coordinates[1], coordinates[0]);

            var self = this;
            var callback = function(results, status) {
                if (results.length) {
                    // update all bound fields
                    if (self.options.boundLocationField) {
                        self.updateLocationField(results);
                    }
                    if (self.options.boundTargetCountryField) {
                        self.updateTargetCountryField(results);
                    }
                    if (self.options.boundLevelOfAccuracyField) {
                        self.updateLevelOfAccuracyField(results);
                    }
                }
            };
            this.geocoder.geocode({"latLng" : latLng, "language": "en"}, callback);
        };

        // Given a google autocomplete place, update the map
        MapWidget.prototype.updateFromPlaceData = function(place) {
            if (this.options.boundLatField && this.options.boundLonField) {
                var lng = place.geometry.location.lng();
                var lat = place.geometry.location.lat();
                this.updateLatLongFields([lat, lng]);
                this.movePointToLatLong(lat, lng);
            }
            // update all bound fields
            if (this.options.boundLocationField) {
                this.updateLocationField([place]);
            }
            if (this.options.boundTargetCountryField) {
                this.updateTargetCountryField([place]);
            }
            if (this.options.boundLevelOfAccuracyField) {
                this.updateLevelOfAccuracyField([place]);
            }

        };

        MapWidget.prototype.updateBoundFields = function(event) {
            // Check that we don't trigger for non points
            var point = null;
            if (event.hasOwnProperty('feature')) {
                var point = event.feature.getGeometry();
            }
            else if (event.hasOwnProperty('features')) {
                var point = event.features.item(0).getGeometry();
            }

            if (point != null && point.getType() !== 'Point') {
                return;
            }

            var latLon = ol.proj.transform(
                point.getCoordinates(), this.map.getView().getProjection(), 'EPSG:4326');
            this.geocodeCoordinates(latLon);
            if (this.options.boundLatField && this.options.boundLonField) {
                this.updateLatLongFields(latLon);                
            }

        };

        MapWidget.prototype.getCoordinates = function(lat, lon) {
            // Get web projection coordinates
            var proj = this.map.getView().getProjection();
            return ol.proj.transform([lon, lat], 'EPSG:4326', proj);
        };

        MapWidget.prototype.movePointToLatLong = function(lat, lon) {
            var coordinates = this.getCoordinates(lat, lon);
            this.map.getView().setCenter(coordinates);
            this.map.getView().setZoom(this.options.default_zoom);

            // We shouldn't have multiple features here. If so, just move them.
            this.featureOverlay.getSource().forEachFeature(function (feature) {
                feature.getGeometry().setCoordinates(coordinates);
            });
        };

        MapWidget.prototype.initLinkHandlers = function () {
            var mapWidget = this;
            var divMapId = this.options.id + '-div-map';
            var divMap = jQuery('#' + divMapId);
            var showLink = divMap.next('a.show-hide-map');
            showLink.on('click', function (event) {
                event.preventDefault();
                var mapElement = jQuery('#' + divMapId);
                mapElement.toggle();

                var oldText = jQuery(this).text();
                jQuery(this).text(jQuery(this).data('alternate'));
                jQuery(this).data('alternate', oldText);

                if (mapElement.is(':visible')) {
                    mapWidget.map.updateSize();
                }

            });

            var map = jQuery('#' + this.options.map_id);
            var clearFeatures = map.next('.clear_features').children('a');
            clearFeatures.on('click', function(event) {
                event.preventDefault();
                mapWidget.clearFeatures();
            });
        }

        window.MapWidget = MapWidget;
    })();
});