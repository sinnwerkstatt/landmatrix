var map;
var cluster = new Array();

$(document).ready(function() {
		// ALL Layers 
		map = new ol.Map({
			target: 'map',
			// Base Maps Layers
			layers: [
				new ol.layer.Group({
					'title':'Base Maps',
					layers: [
						new ol.layer.Tile({
							title:'OSM',
							type:'base',
							visible:false,
							source: new ol.source.OSM()
						}),
						new ol.layer.Tile({
							title:'Satellite',
							type:'base',
							visible:false,
							source: new ol.source.MapQuest({layer:'sat'})
						}),
						new ol.layer.Tile({
							title:'Toner',
							type:'base',
							visible:true,
							source: new ol.source.Stamen({
								layer:'toner'
							})
						}),
					]
				}),
				// Context Layers from the Landobservatory Geoserver
				new ol.layer.Group({
					title:'Context Layers',
					layers:[
						new ol.layer.Tile({
							title:'Global Cropland',
							source: new ol.source.TileWMS({
								url:'',
								params:{'LAYERS':''},
								serverType:'geoserver'
							})
						}),
						new ol.layer.Tile({
							title:'Global Landcover',
							source: new ol.source.TileWMS({
								url:'',
								params:{'LAYERS':''},
								serverType:'geoserver'
							})
						}),
					]
				})
			],
			controls:[
								new ol.control.Zoom (),
								new ol.control.ScaleLine(),
								new ol.control.MousePosition({
    								projection: 'EPSG:4326',
  			  						coordinateFormat: function(coordinate) {
      									return ol.coordinate.format(coordinate, '{y}, {x}', 4);
    								}
    							}),
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
			view: new ol.View({
				center: [0,0],
				zoom: 2
			}),
		});

// LayerSwitcher Control by https://github.com/walkermatt/ol3-layerswitcher
		var layerSwitcher = new ol.control.LayerSwitcher({
			tipLabel:'Legende'
		});
		map.addControl(layerSwitcher);

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

	var clusters = new ol.layer.Vector({
	  source: clusterSource,
	  style: function(feature, resolution) {
	    var size = feature.get('features').length;

	//Give a color to each Intention of Investment, only for single points
	// PROBLEM : how to clustered the points by color? 	
		var color = "";
			if (size > 1){
				color = '#4C76AB';
			}
			else if (intention=='Agriculture'){
				color = '#1D6914';
			}
			else if (intention=='Forestry'){
				color= '#2A4BD7';
			}
			else if (intention=='Conservation'){
				color= '#575757';
			}
			else if (intention=='Industry'){
				color= '#AD2323';
			}
			else if (intention=='Renewable Energy'){
				color= '#81C57A';
			}
			else if (intention=='Tourism'){
				color= '#9DAFFF';
			}
			else if (intention=='Other'){
				color= '#8126C0';
			}
			else if (intention=='Mining'){
				color='#814A19';
			}
			else {
				color='black';
			}

		var style = styleCache[size];

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
	        	radius: radius,
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
	  	$(element).popover({
		    'placement': 'top',
		    'animation': false,
		    'html': true,
		    'content': '<p>Latitude:</p><code>' + latitude + '</code>'+ '<p>Longitude:</p><code>' + longitude + '</code>'+ '<p>Intention of investment:</p><code>' + intention + '</code>'
	  	});
	 	 $(element).popover('show');	
		}); 
};



