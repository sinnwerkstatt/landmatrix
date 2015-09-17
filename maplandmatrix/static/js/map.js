var map;
var cluster = new Array();

$(document).ready(function() {
	// GrundKarte Open Street Map + GeoJSON Countries Borders
	map = new ol.Map({
		layers: [
			/**new ol.layer.Tile({
				source: new ol.source.OSM()
			}),*/
			new ol.layer.Tile({
				source: new ol.source.Stamen({
					layer: 'toner'
				})
			}),
			new ol.layer.Vector({
				source : new ol.source.Vector({
					url :'/static/data/geodata/countries_simple.geojson',
					format: new ol.format.GeoJSON(),
				}),
				style : new ol.style.Style({
					stroke : new ol.style.Stroke({
						color :  '#319FD3',
						width : 0.5
					}),
					zIndex : 999
				}),
			}),
		],
		controls:[
							new ol.control.Zoom (),
							new ol.control.ScaleLine(),
							new ol.control.MousePosition(),
							new ol.control.FullScreen(),
							new ol.control.Attribution,
		],
		interactions : [
							new ol.interaction.Select(),
							new ol.interaction.MouseWheelZoom(),
							new ol.interaction.PinchZoom(),
							new ol.interaction.DragZoom (),
							new ol.interaction.DoubleClickZoom(),
							new ol.interaction.DragPan(), 
		],
		target: 'map',
		view: new ol.View({
			center: [0,0],
			zoom: 2
		}),
	});
 // var selectedFeatures = new ol.interaction.Select().getFeatures();
}); //gesamte document.ready.function Klammer

//longitude, Latitude, Intention im Index.html definieren
function clusteredMarkers (longitude, latitude, intention) {
	var feature = new ol.Feature({
		geometry: new ol.geom.Point(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857')),
	});
	cluster.push(feature);

	var source = new ol.source.Vector({
		features: cluster
	});
	var clusterSource = new ol.source.Cluster({
	  distance: 100,
	  source: source
	});

	var styleCache = {};

// Give a color to each Intention of Investment	
	var color = "";
	if (intention=='Agriculture'){
		color = 'green';
	}
	else if (intention=='Forestry'){
		color= 'yellow';
	}
	else if (intention=='Conservation'){
		color= 'orange';
	}
	else if (intention=='Industry'){
		color= 'black';
	}
	else if (intention=='Renewable Energy'){
		color= 'pink';
	}
	else if (intention=='Tourism'){
		color= 'red';
	}
	else if (intention=='Other'){
		color= 'grey';
	}
	else {
		color='blue';
	}
	
	var clusters = new ol.layer.Vector({
	  source: clusterSource,
	  style: function(feature, resolution) {
	    var size = feature.get('features').length;
	    var style = styleCache[size];
// Define a SIZE and RADIUS MIN-MAX
	  	var radius = size/2;
	    	if (radius > 75) {
	    		radius = 25;
	    	}
	    	else if (radius < 10) {
	    		radius = 7;
	    	}
	    if (!style) {
	      style = [new ol.style.Style({
	        image: new ol.style.Circle({
	        	radius: radius ,
	          stroke: new ol.style.Stroke({
	            color: '#fff'
	          }),
	          fill: new ol.style.Fill({
	          	color: color, 
	          })
	        }),
	        text: new ol.style.Text({
	          text: size.toString(),
	          fill: new ol.style.Fill({
	            color: '#fff'
	          })
	        })
	      })];
	      styleCache[size] = style;
	    }
	    return style;
	  }
	});
	map.addLayer(clusters);

	var popup = new ol.Overlay({
		element: document.getElementById('popup')
	});
	map.addOverlay(popup);

	map.on('click', function(evt){
		var element = popup.getElement(); 
		var coordinate = evt.coordinate; 
	
		$(element).popover('destroy');
		popup.setPosition(coordinate);
  // the keys are quoted to prevent renaming in ADVANCED mode.
  	$(element).popover({
	    'placement': 'top',
	    'animation': false,
	    'html': true,
	    'content': '<p>Latitude:</p><code>' + latitude + '</code>'+ '<p>Longitude:</p><code>' + longitude + '</code>'+ '<p>Intention of investment:</p><code>' + intention + '</code>'
  	});
 	 $(element).popover('show');	
	}); 
		

};



