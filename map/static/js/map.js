//Coordinates : need to CONVERT the projections from ... to ... :
//EPSG:4326: is the WGS84 projection, commun use for the World (ex: GPS)
//EPSG:3857:Spherical Web Mercator projection used by Google and OpenStreetMap

// Globale Variablen
var map,
    view,
    layers = [],
    controls = [],
    interactions = [],
    olGM;

var countryThreshold = 4;
var clusterThreshold = 10;

var currentVariable = 'Deal Intention';
var markerSource = new ol.source.Vector();

var intendedAreaFeatures = new ol.Collection();
var productionAreaFeatures = new ol.Collection();
var contractAreaFeatures = new ol.Collection();

var intendedAreaSource = new ol.source.Vector({
    features: intendedAreaFeatures
});
var productionAreaSource = new ol.source.Vector({
    features: productionAreaFeatures
});
var contractAreaSource = new ol.source.Vector({
    features: contractAreaFeatures
});

var clusterSource = new ol.source.Cluster({
    distance: 30,
    source: markerSource
});

var countriesSource = new ol.source.Vector();

var fieldnames = {
    'Geospatial Accuracy': 'accuracy',
    'Negotiation Status': 'negotiation_status',
    'Deal Intention': 'intention'
};

var detailviews = {
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
            // FIXME: Subchoices probably can be removed by now
            'Biofuels': '#1D6914',
            'Food crops': '#1D6914',
            'Fodder': '#1D6914',
            'Livestock': '#1D6914',
            'Non-food agricultural commodities': '#1D6914',
            'Agriculture unspecified': '#1D6914',
        'Forestry': '#2A4BD7',
            // FIXME: Subchoices probably can be removed by now
             'For wood and fibre': '#2A4BD7',
             'For carbon sequestration/REDD': '#2A4BD7',
             'Forestry unspecified': '#2A4BD7',
        'Conservation': '#575757',
        'Industry': '#AD2323',
        'Renewable Energy': '#81C57A',
        'Tourism': '#9DAFFF',
        'Other': '#8126C0',
        'Resource extraction': '#814A19',
        'Undefined': '#FF0000'
    }
};

const GeoJSONColors = {  // Back, Border
    'Current area in operation (ha)': ['rgba(0, 0, 196, 0.4)', '#007'],
    'Contract area (ha)': ['rgba(128, 128, 128, 0.6)', '#575757'],
    'Intended area (ha)': ['rgba(0, 196, 0, 0.6)', '#0a0']
};

var geoJSONReader = new ol.format.GeoJSON(),
    PopupOverlay,
    container,
    content,
    closer,
    cluster,
    countries,
    image,
    styles;

//Map, Layers and Map Controls
$(document).ready(function () {
    /*
     var geojsonObject = {
     'type': 'FeatureCollection',
     'crs': {
     'type': 'name',
     'properties': {
     'name': 'EPSG:3857'
     }
     },
     'features': [{
     'type': 'Feature',
     'geometry': {
     'type': 'Point',
     'coordinates': [0, 0]
     }
     }, {
     'type': 'Feature',
     'geometry': {
     'type': 'LineString',
     'coordinates': [[4e6, -2e6], [8e6, 2e6]]
     }
     }, {
     'type': 'Feature',
     'geometry': {
     'type': 'LineString',
     'coordinates': [[4e6, 2e6], [8e6, -2e6]]
     }
     }, {
     'type': 'Feature',
     'geometry': {
     'type': 'Polygon',
     'coordinates': [[[-5e6, -1e6], [-4e6, 1e6], [-3e6, -1e6]]]
     }
     }, {
     'type': 'Feature',
     'geometry': {
     'type': 'MultiLineString',
     'coordinates': [
     [[-1e6, -7.5e5], [-1e6, 7.5e5]],
     [[1e6, -7.5e5], [1e6, 7.5e5]],
     [[-7.5e5, -1e6], [7.5e5, -1e6]],
     [[-7.5e5, 1e6], [7.5e5, 1e6]]
     ]
     }
     }, {
     'type': 'Feature',
     'geometry': {
     'type': 'MultiPolygon',
     'coordinates': [
     [[[-5e6, 6e6], [-5e6, 8e6], [-3e6, 8e6], [-3e6, 6e6]]],
     [[[-2e6, 6e6], [-2e6, 8e6], [0, 8e6], [0, 6e6]]],
     [[[1e6, 6e6], [1e6, 8e6], [3e6, 8e6], [3e6, 6e6]]]
     ]
     }
     }, {
     'type': 'Feature',
     'geometry': {
     'type': 'GeometryCollection',
     'geometries': [{
     'type': 'LineString',
     'coordinates': [[-5e6, -5e6], [0, -5e6]]
     }, {
     'type': 'Point',
     'coordinates': [4e6, -5e6]
     }, {
     'type': 'Polygon',
     'coordinates': [[[1e6, -6e6], [2e6, -4e6], [3e6, -6e6]]]
     }]
     }
     }]
     };
     */

    initMap('map');
});

function initMap(target) {
    /**
     * Elements that make up the popup.
     */
    container = document.getElementById('popup');
    content = document.getElementById('popup-content');
    closer = document.getElementById('popup-closer');

    /**
     * Create an overlay to anchor the popup to the map.
     */
    PopupOverlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
        element: container,
        autoPan: true,
        autoPanAnimation: {
            duration: 250
        }
    }));

    /**
     * Add a click handler to hide the popup.
     * @return {boolean} Don't follow the href.
     */
    closer.onclick = closePopup;

    cluster = new ol.layer.Vector({
        title: 'Markers',
        source: clusterSource,
        style: function (feature, resolution) {
            var size;
            var features = feature.get('features');

            if (features) {
                size = features.length;
            }
            else {
                size = 1;
            }
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
                if (features) {
                    feature = feature.get('features')[0];
                }
                if (feature && feature.get('dealData')) {
                    var classifier = feature.get('dealData')[fieldnames[currentVariable]];
                    if (classifier in detailviews[currentVariable]) {
                        color = detailviews[currentVariable][classifier];
                    }
                }
                if (color === '') {
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
    });

    countries = new ol.layer.Vector({
        title: 'Countries',
        source: countriesSource,
        visible: true,
        style: function () {
            var color = '#fc941f';

            var image = new ol.style.Circle({
                radius: 10,
                stroke: new ol.style.Stroke({
                    color: '#fff'
                }),
                fill: new ol.style.Fill({
                    color: color
                })
            });

            var style = [new ol.style.Style({
                image: image,
            })];
            return style;
        }
    });


    /**
     * GeoJSON features
     *
     */

    image = new ol.style.Circle({
        radius: 5,
        fill: null,
        stroke: new ol.style.Stroke({color: 'red', width: 1})
    });

    styles = {
        'Point': [new ol.style.Style({
            image: image
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
            image: image
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

    var intendedAreaLayer = new ol.layer.Vector({
        title: 'Intended area (ha)',
        visible: true,
        source: intendedAreaSource,
        style: new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: GeoJSONColors['Intended area (ha)'][1],
                width: 1
            }),
            fill: new ol.style.Fill({
                color: GeoJSONColors['Intended area (ha)'][0]
            })
        })
    });

    var productionAreaLayer = new ol.layer.Vector({
        title: 'Current area in operation (ha)',
        visible: true,
        source: productionAreaSource,
        style: new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: GeoJSONColors['Current area in operation (ha)'][1],
                width: 1
            }),
            fill: new ol.style.Fill({
                color: GeoJSONColors['Current area in operation (ha)'][0]
            })
        })
    });

    var contractAreaLayer = new ol.layer.Vector({
        title: 'Contract area (ha)',
        visible: true,
        source: contractAreaSource,
        style: new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: GeoJSONColors['Contract area (ha)'][1],
                width: 1
            }),
            fill: new ol.style.Fill({
                color: GeoJSONColors['Contract area (ha)'][0]
            })
        })
    });


    layers = baseLayers;
    layers.push(
        // Context Layers from the Landobservatory Geoserver.
        new ol.layer.Group({
            title: 'Context Layers',
            layers: contextLayers
        }),
        new ol.layer.Group({
            title: 'Deals',
            layers: [
                intendedAreaLayer,
                productionAreaLayer,
                contractAreaLayer,
                cluster,
                countries
            ]
        })
    );

    var spiderInteraction = new ol.interaction.ClusterSpiderfier({
        minRadius: 40
    });
    interactions.push(
        // new ol.interaction.Select(),
        new ol.interaction.MouseWheelZoom(),
        new ol.interaction.PinchZoom(),
        new ol.interaction.DragZoom(),
        new ol.interaction.DoubleClickZoom(),
        new ol.interaction.DragPan(),
        spiderInteraction
    );
    controls = [];

    if (typeof mapDisableControls === 'undefined') {
        controls = [
            new ol.control.FullScreen(),
            new ol.control.Zoom(),
            new ol.control.ScaleLine(),
            new ol.control.MousePosition({
                projection: 'EPSG:4326',
                coordinateFormat: function (coordinate) {
                    return ol.coordinate.format(coordinate, '{y}, {x}', 4);
                }
            }),
            new ol.control.FullScreen(),
            new ol.control.Attribution,
            //new ol.control.ZoomToExtent({
            //             extent:undefined
            //}),
        ];
    }

    view = new ol.View({
        center: [0, 0],
        zoom: 2,
        maxZoom: 17,
        minZoom: 2
    });
    map = new ol.Map({
        target: target,
        layers: layers,
        controls: controls,
        interactions: interactions,
        overlays: [PopupOverlay],
        renderer: 'canvas',
        // Set the map view : here it's set to see the all world.
        view: view
    });

    olGM = new olgm.OLGoogleMaps({map: map});
    olGM.activate();

    // Set boundaries if given
    if (typeof mapBounds !== 'undefined') {
        var proj = map.getView().getProjection();
        var extent = ol.extent.boundingExtent(mapBounds);
        extent = ol.extent.applyTransform(
            extent, ol.proj.getTransform('EPSG:4326', proj));
        map.getView().fit(extent, map.getSize());
    }

    // LayerSwitcher Control by https://github.com/walkermatt/ol3-layerswitcher
    if (typeof mapDisableControls === 'undefined') {
        var layerSwitcher = new ol.control.LayerSwitcher({
            tipLabel: 'Legend'
        });
        map.addControl(layerSwitcher);
        $(".areaLabel").each(function (index) {
            const context = $(this).context.innerHTML;
            const colors = GeoJSONColors[context];

            var legendSpan = document.createElement('span');
            legendSpan.className = 'legend-symbol';
            legendSpan.setAttribute('style', 'color: ' + colors[0] + ';' +
                'background-color:' + colors[0] + ';' +
                'border-color: ' + colors[1] + ';' +
                'border: solid 3px ' + colors[1] + ';');
            legendSpan.innerHTML = " ";

            $(this).append(legendSpan);
        });
        layerSwitcher.showPanel();

        var variableLabel = document.getElementById('legendLabel');

        var innerHTML = '';
        for (key in detailviews) {
            innerHTML = innerHTML + '<option';
            if (key === currentVariable) {
                innerHTML = innerHTML + ' selected';
            }
            innerHTML = innerHTML + '>' + key + '</option>';
        }

        var dropdown = document.createElement('select');
        dropdown.id = 'mapVariableSelect';
        dropdown.value = currentVariable;
        dropdown.classname = 'form-control';

        function pickNewVariable() {
            currentVariable = dropdown.value;
            updateVariableSelection(currentVariable);
            typeof mapDisableDeals === 'undefined' && getApiData();
        }

        dropdown.onchange = pickNewVariable;

        dropdown.innerHTML = innerHTML;

        newlegendlabel = variableLabel.parentNode.replaceChild(dropdown, variableLabel);

        updateVariableSelection(currentVariable);

        if (typeof mapHideControls !== 'undefined') {
            $('#legendstuff').toggleClass('hidden');
        }

    }

    NProgress.configure(
        {
            trickleRate: 0.02,
            trickleSpeed: 800
        }
    );

    map.on('click', function (evt) {
        var popupFeature = map.forEachFeatureAtPixel(
            evt.pixel, handleFeatureClick);
        if (!popupFeature) {
            closePopup();
        }
    });

    // change Mouse Cursor when over Marker
    var target = map.getTarget();
    var jTarget = typeof target === "string" ? $("#" + target) : $(target);

    $(map.getViewport()).on('mousemove', function (e) {
        var pixel = map.getEventPixel(e.originalEvent);
        var hit = map.forEachFeatureAtPixel(pixel, function (feature, layer) {
            return true;
        });

        if (hit) {
            jTarget.css("cursor", "pointer");
        } else {
            jTarget.css("cursor", "");
        }
    });

    if (typeof mapDisableDeals === 'undefined') {
        // Set zoom and pan handlers
        // Check here if we are just zooming in on the same deals
        // if so, don't reload
        var lastExtent;
        var lastZoom;
        var updateMarkers = function(event) {
            var currentZoom = event.map.getView().getZoom();
            var currentExtent = event.frameState.extent;
            var isContained = lastExtent !== undefined &&
                ol.extent.containsExtent(lastExtent, currentExtent);
            var movedIntoDeals = lastZoom !== undefined &&
                currentZoom >= countryThreshold &&
                lastZoom < countryThreshold;
            var movedIntoCountries = lastZoom !== undefined &&
                currentZoom < countryThreshold &&
                lastZoom >= countryThreshold;
            var passedThreshold = movedIntoDeals || movedIntoCountries;
            var inDeals = currentZoom >= countryThreshold;

            if (passedThreshold) {
                getApiData();
            }
            // Only reload in deals if we pan, no need in countries or when
            // zooming
            else if (inDeals && !isContained) {
                getApiData();
            }

            lastExtent = currentExtent;
            lastZoom = currentZoom;
        };
        map.on("moveend", updateMarkers);
        // zoomend never seems to actually get fired.
        map.on("zoomend", updateMarkers);

        getApiData();
    }
};

function getApiData() {
    NProgress.start();
    // TODO: (Later) initiate spinner before fetchin' stuff

    // If the zoom level is below the clustering threshold, show
    // country-based "clusters".
    if (view.getZoom() < countryThreshold) {
        var url = '/api/target_country_summaries.json';
        // append any querystring params
        if (window.location.search) {
            url = url + window.location.search;
        }
        $.get(url, addCountrySummariesData);
    // Otherwise fetch individual deals for the current map viewport.
    } else {
        var limit = 500;
        var query_params = 'limit=' + limit + '&attributes=' + fieldnames[currentVariable];
        if (typeof mapParams !== 'undefined') {
            query_params += mapParams;
        }
        // Window
        extent = map.getView().calculateExtent(map.getSize());
        extent = ol.extent.applyTransform(extent, ol.proj.getTransform("EPSG:3857", "EPSG:4326"));
        var url = "/api/deals.json?" + query_params + '&window=' + extent.join(',');
        // append any other querystring params
        if (window.location.search) {
            url = url + '&' + window.location.search.slice(1);
        }
        $.get(url, addData).fail(function () {
            NProgress.done();
        });
    }
    NProgress.set(0.2);
}

function updateVariableSelection(variableName) {
    var legend = document.getElementById('legend');

    var variableSet = detailviews[variableName];

    while (legend.hasChildNodes()) {
        legend.removeChild(legend.lastChild)
    }

    for (name in variableSet) {
        var varItem = document.createElement('li');
        varItem.className = 'legend-entry';

        var varName = name;
        var varColor = variableSet[name];

        var legendSpan = document.createElement('span');
        legendSpan.className = 'legend-symbol';
        legendSpan.setAttribute('style', 'color: ' + varColor + '; background-color:' + varColor + ";");
        legendSpan.innerHTML = ".";

        var legendLabel = document.createElement('div');
        legendLabel.innerHTML = varName;

        varItem.appendChild(legendSpan);
        varItem.appendChild(legendLabel);

        legend.appendChild(varItem);
    }

    // Init layer legend modal
    $('a[data-target="#map-legend"]').click(function () {
        var modal = $($(this).data('target'));
        // Set title
        modal.find('.modal-title').text($(this).parent().text());
        // Set legend
        var img = $('<img>');
        img.attr('src', 'http://sdi.cde.unibe.ch/geoserver/lo/wms?REQUEST=GetLegendGraphic&FORMAT=image/png&WIDTH=30&HEIGHT=20&LAYER=' + $(this).attr('href').substr(1));
        img.appendTo(modal.find('.modal-body').empty());

        modal.modal('show');
    });

}

function handleFeatureClick (feature, layer) {
    // A country feature was clicked.
    if (feature && feature.get('countryData')) {
        handleCountryClick(feature);
        return;
    }

    var features = feature.get('features');

    if (features && features.length > 1) {
        // Skip clusters, as they are handled elsewhere
        return;
    }

    if (features) {
        var feat = features[0];
    }
    else {
        var feat = feature;
    }

    var dealData = feat.get('dealData');
    var id = dealData.deal_id;
    var lat = dealData.lat.toFixed(4);
    var lon = dealData.lon.toFixed(4);
    var intention = dealData.intention;
    var intended_size = dealData.intended_size;
    var production_size = dealData.production_size;
    var contract_size = dealData.contract_size;
    var investor = dealData.investor;
    var status = dealData.negotiation_status;
    var accuracy = dealData.geospatial_accuracy;

    // TODO: Here, some javascript should be called to get the deal details from the API
    // and render it inside the actual content popup, instead of getting this from the db for every marker!
    content.innerHTML = '<div><span><a href="/deal/' + id + '"><strong>Deal #' + id + '</strong></a></span>';
    //content.innerHTML += '<p>Coordinates:</p><code>' + lat + ' ' + lon + '</code>';
    if (intended_size !== null) {
        content.innerHTML += '<span>Intended area (ha):</span><span class="pull-right">' + parseInt(intended_size).toLocaleString(options = {useGrouping: true}) + '</span><br/>';
    }
    if (production_size !== null) {
        content.innerHTML += '<span>Production size (ha):</span><span class="pull-right">' + parseInt(production_size).toLocaleString(options = {useGrouping: true}) + '</span><br/>';
    }
    if (contract_size !== null) {
        content.innerHTML += '<span>Contract size (ha):</span><span class="pull-right">' + parseInt(contract_size).toLocaleString(options = {useGrouping: true}) + '</span><br/>';
    }
    content.innerHTML += '<span>Intention:</span><span class="pull-right">' + intention + '</span><br/>';
    content.innerHTML += '<span>Operational company:</span><span class="pull-right">' + investor + '</span><br />';
    // TODO: Handle other possibly already known attributes from currentVariable
    if (status) {
        content.innerHTML += '<span>Negotiation Status:</span><span class="pull-right">' + status + '</span><br />';
    }
    if (accuracy) {
        content.innerHTML += '<span>Geospatial Accuracy:</span><span class="pull-right">' + accuracy + '</span><br />';
    }
    content.innerHTML += '<span><a href="/deal/' + id + '">More details</a></span></div>';

    PopupOverlay.setPosition(feat.getGeometry().getCoordinates());

    return feat;
};

function handleCountryClick (feature) {
    var a = feature.get('countryData');
    var countryBounds = [a.lat_min, a.lon_min, a.lat_max, a.lon_max];
    var extent = ol.extent.applyTransform(countryBounds, ol.proj.getTransform("EPSG:4326", "EPSG:3857"));
    map.getView().fit(extent, map.getSize());
};

function addData (data) {
    var lats = {};
    var duplicates = 0;

    NProgress.set(0.8);
    countriesSource.clear();
    markerSource.clear();

    if (data.length < 1) {
        $('#alert_placeholder').html('<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><span>There are no deals in the currently displayed region.</span></div>')
    } else {
        $('#alert_placeholder').empty();
        for (var i = 0; i < data.length; i++) {
            NProgress.inc();
            var marker = data[i];
            if (marker.locations.length == 0) {
                // No locations, can't have markers
                continue;
            }
            var location = marker.locations[0];
            marker.lat = parseFloat(location.point_lat);
            marker.lon = parseFloat(location.point_lon);

            addClusteredMarker(marker);
            //addClusteredMarkerNew(marker);
            lats[marker.lat] = marker;

            if (location.hasOwnProperty('intended_area') && location.intended_area != null) {
                var geometry = geoJSONReader.readGeometry(location.intended_area, {
                    dataProjection: 'EPSG:4326',
                    featureProjection: 'EPSG:3857'
                });
                intendedAreaFeatures.push(new ol.Feature({'geometry': geometry}));
            }
            if (location.hasOwnProperty('production_area') && location.production_area != null) {
                var geometry = geoJSONReader.readGeometry(location.production_area, {
                    dataProjection: 'EPSG:4326',
                    featureProjection: 'EPSG:3857'
                });
                productionAreaFeatures.push(new ol.Feature({'geometry': geometry}));
            }
            if (location.hasOwnProperty('contract_area') && location.contract_area != null) {
                var geometry = geoJSONReader.readGeometry(location.contract_area, {
                    dataProjection: 'EPSG:4326',
                    featureProjection: 'EPSG:3857'
                });
                contractAreaFeatures.push(new ol.Feature({'geometry': geometry}));
            }
        }
    }
    NProgress.done(true);
};

// Taken from the OL example here
// http://openlayers.org/en/v3.9.0/examples/feature-animation.html
function bounceFeature(feature, startRadius, maxRadius, endRadius, duration) {
    var start = new Date().getTime();
    var listenerKey;

    function animate(event) {
        var vectorContext = event.vectorContext;
        var frameState = event.frameState;
        var flashGeom = feature.getGeometry().clone();
        var elapsed = frameState.time - start;
        var elapsedRatio = elapsed / duration;
        var radius;

        if (elapsedRatio < 0.5) {
            var easing = ol.easing.easeOut(elapsedRatio * 2)
            radius = (easing * (maxRadius - startRadius)) + startRadius;
        }
        else {
            if (elapsedRatio > 1) {
                elapsedRatio = 1;
            }
            var easing = ol.easing.easeOut(1 - elapsedRatio);
            radius = (easing * (maxRadius - endRadius)) + endRadius;
        }

        var flashStyle = new ol.style.Circle({
            snapToPixel: false,
            radius: radius,
            // Stroke looks janky after animation finishes
            // stroke: new ol.style.Stroke({
            //     color: '#fff'
            // }),
            fill: new ol.style.Fill({
                color: '#fc941f'
            })
        });
        vectorContext.setImageStyle(flashStyle);
        // According to the API docs should be drawPointGeometry...
        vectorContext.drawPoint(flashGeom, null);
        if (elapsed > duration) {
            ol.Observable.unByKey(listenerKey);
            return;
        }
        // tell OL3 to continue postcompose animation
        frameState.animate = true;
    }

  listenerKey = map.on('postcompose', animate);
}

countriesSource.on('addfeature', function(event) {
    var feature = event.feature;
    bounceFeature(feature, 10, 30, 10, 1200);
});

function addCountrySummariesData (data) {
    countriesSource.clear();
    markerSource.clear();
    $('#alert_placeholder').empty();
    $(data).each(function (index, country) {
        var feature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform(
                [country.lon, country.lat],
                'EPSG:4326', 'EPSG:3857')
            )
        });
        feature.set('countryData', country);
        countriesSource.addFeature(feature);
    });
    NProgress.done(true);
};

// MARKERS in clusters. ONE MARKER = ONE DEAL
//longitude, latitude, intention im Index.html definiert
function addClusteredMarker(marker) { // dealid, longitude, latitude, intention, marker) {
    // .deal_id, parseFloat(marker.point_lon), parseFloat(marker.point_lat), marker.intention, marker

    var lat = marker.lat;
    var lon = marker.lon;

    if ((typeof lat == 'number') && (typeof lon == 'number')) {
        var feature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.transform([lon, lat], 'EPSG:4326', 'EPSG:3857'))
        });

        if (('intention' in marker) && (marker.intention) && (marker.intention.indexOf(',') > -1)) {
            marker.intention = marker.intention.split(',', 1)[0];
        }
        feature.set('dealData', marker);

        markerSource.addFeature(feature);
    } else {
        console.log("Faulty object: ", marker);
    }
}


function fitBounds(geom) {
    var bounds = new ol.extent.boundingExtent([[geom.j.j, geom.R.R], [geom.j.R, geom.R.j]]);

    bounds = ol.proj.transformExtent(bounds, ol.proj.get('EPSG:4326'), ol.proj.get('EPSG:3857'));

    map.getView().fit(bounds, map.getSize());
}

function initGeocoder(el) {

    try {
        autocomplete = new google.maps.places.Autocomplete(el);

        autocomplete.addListener('place_changed', function () {
            var place = autocomplete.getPlace();
            if (!place.geometry) {
                $('#alert_placeholder').html('<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><span>Sorry, that place cannot be found.</span></div>')

                //window.alert("Autocomplete's returned place contains no geometry");
                return;
            }


            // If the place has a geometry, then present it on a map.
            /*if (place.geometry.viewport) {
                console.log(place.geometry);

                if (typeof mapShowPerspective !== 'undefined') {
                    drawCircleInMeter(map, mapShowPerspective, {0: place.geometry.location.lng(), 1:place.geometry.location.lat()});
                }

                fitBounds(place.geometry.viewport);
            } else*/ {
                var target = [place.geometry.location.lng(), place.geometry.location.lat()]
                target = ol.proj.transform(target, ol.proj.get('EPSG:4326'), ol.proj.get('EPSG:3857'));
                map.getView().setCenter(target);
                //map.getView().setZoom(16);
            }

            var address = '';
            if (place.address_components) {
                address = [
                    (place.address_components[0] && place.address_components[0].short_name || ''),
                    (place.address_components[1] && place.address_components[1].short_name || ''),
                    (place.address_components[2] && place.address_components[2].short_name || '')
                ].join(' ');
            }

            //infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
            //infowindow.open(map, marker);
        });
    }
    catch (err) {
        console.log('No google libs loaded, replacing with a hint.');

        var hint = '<a title="If you allow Google javascript, a geolocation search field would appear here." href="#" class="toggle-tooltip noul">';
        hint = hint + '<i class="lm lm-question-circle"></i></a>';

        $(el).replaceWith(hint);

    }

}

function unlockMaps() {
    lock = false;
}

function closePopup () {
    PopupOverlay.setPosition(undefined);
    closer.blur();
    return false;
};
