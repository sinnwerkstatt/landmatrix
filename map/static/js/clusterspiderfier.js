// OpenLayers 3 Cluster spiderfier.
// See https://github.com/CandoImage/OL3ClusterSpiderfier
// Version: v1.0
// Modified to work with out deals map

/**
 * @constructor
 * @extends {ol.interaction.Pointer}
 */
ol.interaction.ClusterSpiderfier = function(options) {
  ol.interaction.Interaction.call(this, {
    handleEvent: ol.interaction.ClusterSpiderfier.prototype.handleEvent.bind(this)
  });

  options = options || {};
  this._map = options.map;
  this.minRadius = options.minRadius || 50;
  this.displayGeometry = options.displayGeometry || 'circle';
  this.style = options.style;
  this.ns = 'ClusterSpiderfier.';
  this.selectedClusters = [];
};

ol.inherits(ol.interaction.ClusterSpiderfier, ol.interaction.Interaction);

ol.interaction.ClusterSpiderfier.prototype.getFeatures = function() {
  return []; //this.featureOverlay_.getSource().getFeatures();
};

/**
 * Remove the interaction from its current map, if any,  and attach it to a new
 * map, if any. Pass `null` to just remove the interaction from the current map.
 * @param {ol.Map} map Map.
 * @api stable
 */
ol.interaction.ClusterSpiderfier.prototype.setMap = function(map) {
  var self = this;
  this._map = map;

  if (map && map.getView()) {
    map.getView().on('change:resolution', function(evt) {
      var i, j, features;
      for (i = 0; i < self.selectedClusters.length; i++) {
        // close spider when zoom level changes
        self.close(self.selectedClusters[i].getSource().getFeatures()[0]);
      }
      self.selectedClusters = [];
    })
  }
};

/**
 * Handles the {@link ol.MapBrowserEvent map browser event} and may change the
 * selected state of features.
 * @param {ol.MapBrowserEvent} mapBrowserEvent Map browser event.
 * @return {boolean} `false` to stop event propagation.
 * @this {ol.interaction.Select}
 * @api
 */
ol.interaction.ClusterSpiderfier.prototype.handleEvent = function(mapBrowserEvent) {
  var map = mapBrowserEvent.map;
  var self = this;

  if (!ol.events.condition.click(mapBrowserEvent)) {
    return true;
  }

  map.forEachFeatureAtPixel(mapBrowserEvent.pixel, function(feature, layer) {
    if (layer) {
      // check if feature is coming from cluster source
      var source = layer.getSource();
      if (source instanceof ol.source.Cluster) {
        feature.set(self.ns + 'originLayer', layer);
        self.open(feature);
      }
      else if (layer.get(self.ns + 'selected') === true) {
        self.close(feature);
      }
    }
    // if we don't get a layer, just use feature attributes
    else if (feature && feature.get(self.ns + 'selectedLayer')) {
      var selectedLayer = feature.get(self.ns + 'selectedLayer');
      if (selectedLayer.get(self.ns + 'selected') === true) {
        self.close(feature);
      }
    }
  });
};

/**
 * Calculate a sensible radius based on the number of features in the cluster
 *
 */
ol.interaction.ClusterSpiderfier.prototype.getRadius = function(feature) {
  var radius, size;
  var features = feature.get('features');
  if (features) {
    size = features.length;
    radius = 30 + (size * 2);
    if (radius < this.minRadius) {
      radius = this.minRadius;
    }
  }
  else {
    radius = this.minRadius; 
  }

  return radius;
};

ol.interaction.ClusterSpiderfier.prototype.open = function(feature) {
  var clusterFeatures = feature.get('features');
  // Lists with one feature shouldn't trigger the opening.
  if (clusterFeatures.length == 1) {
    return;
  }

  // Create a new layer for the selected item
  var selectedLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
      opacity: 0.5
    }),
    updateWhileAnimating: true,
    updateWhileInteracting: true
  });
  selectedLayer.set(this.ns + 'selected', true);
  selectedLayer.setMap(this._map);
  this.selectedClusters.push(selectedLayer);

  // Create a new overlay layer
  var overlayLayer = new ol.layer.Vector({
    source: new ol.source.Vector({
      useSpatialIndex: true
    }),
    updateWhileAnimating: true,
    updateWhileInteracting: true
  });
  overlayLayer.setMap(this._map);

  // Add cluster feature to selected layer
  var selectedFeature = feature.clone();
  selectedFeature.set(this.ns + 'originFeature', feature);

  // Keep a reference to the layers
  selectedFeature.set(this.ns + 'overlayLayer', overlayLayer);
  selectedFeature.set(this.ns + 'selectedLayer', selectedLayer);

  var source = overlayLayer.getSource();
  var originLayer = feature.get(this.ns + 'originLayer');
  if (!selectedLayer.get('hasOwnStyle') && originLayer.getStyle()) {
    selectedLayer.setStyle(originLayer.getStyle());
    selectedLayer.setOpacity(0.5);
  }

  // Add selected feature to layer
  selectedLayer.getSource().addFeature(selectedFeature);

  // TODO: merge these lines together
  // Set default style for overlay items (if available)
  if (typeof this.style !== 'undefined') {
    overlayLayer.set('hasOwnStyle', true);
    overlayLayer.setStyle(this.style);
  }

  // If our layer hasn't explicitly set a style inherit the one from the origin
  // layer.
  if (!overlayLayer.get('hasOwnStyle') && originLayer.getStyle()) {
    overlayLayer.setStyle(originLayer.getStyle());
  }

  // add individual features of the cluster
  var self = this;
  clusterFeatures.forEach(function(f) {
    var cf = f.clone();
    cf.set(self.ns + 'originLayer', originLayer);
    cf.set(self.ns + 'originFeature', feature);
    source.addFeature(cf);
  });

  // hide cluster feature in origin layer (transparency won't work nicely otherwise)
  feature.setStyle(new ol.style.Style());

  switch (this.displayGeometry) {
    case 'spiral':
      this.arrangeSpiral(feature, source.getFeatures());
      break;

    case 'circle':
    default:
      this.arrangeCircle(feature, source.getFeatures());
      break;
  }

};

ol.interaction.ClusterSpiderfier.prototype.close = function(selectedFeature) {
  var selectedLayer = selectedFeature.get(this.ns + 'selectedLayer');
  var overlayLayer = selectedFeature.get(this.ns + 'overlayLayer');
  var selectedSource = selectedLayer.getSource();
  var overlaySource = overlayLayer.getSource();

  // clear overlay
  overlaySource.clear();

  // unhide original cluster feature
  var originFeature = selectedFeature.get(this.ns + 'originFeature');
  var originLayer = originFeature.get(this.ns + 'originLayer');
  originFeature.setStyle(null);
  selectedSource.clear();

  this._map.removeLayer(selectedLayer);
  this._map.removeLayer(overlayLayer);

  var index = this.selectedClusters.indexOf(selectedLayer);
  this.selectedClusters.splice(index, 1);
};

ol.interaction.ClusterSpiderfier.prototype.getGeometryCenterCoordinates = function(geometry) {
  if (geometry instanceof ol.geom.Point) {
    return geometry.getCoordinates();
  }
};

ol.interaction.ClusterSpiderfier.prototype.arrangeSpiral = function(centerFeature, features) {
  var geometry, point, radius, step, center, t;
  var self = this;
  var map = this._map;

  step = 0.5;
  center = map.getPixelFromCoordinate(this.getGeometryCenterCoordinates(centerFeature.getGeometry()));
  t = 0;

  features.forEach(function(f) {
    radius = Math.exp(0.30635*t) * self.getRadius(centerFeature);
    f.setGeometry(new ol.geom.Point(map.getCoordinateFromPixel([ center[0] + Math.sin(t)*radius, center[1] + Math.cos(t)*radius ])));
    t += step;
  });
};

ol.interaction.ClusterSpiderfier.prototype.arrangeCircle = function(centerFeature, features) {
  var geometry, point, radius, step, center, angle;
  var self = this;
  var map = this._map;
  //var extent = this.featureOverlay_.getSource().getExtent();

  step = 2*Math.PI / features.length;
  center = map.getPixelFromCoordinate(this.getGeometryCenterCoordinates(centerFeature.getGeometry()));
  radius = this.getRadius(centerFeature);
  angle = 0.0;

  features.forEach(function(f) {
    f.setGeometry(new ol.geom.Point(map.getCoordinateFromPixel([ center[0] + Math.sin(angle)*radius, center[1] + Math.cos(angle)*radius ])));
    angle += step;
  });
};
