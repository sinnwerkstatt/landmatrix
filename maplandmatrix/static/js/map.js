//Coordinates : need to CONVERT the projections from ... to ... :
	//EPSG:4326: is the WGS84 projection, commun use for the World (ex: GPS)
	//EPSG:3857:Spherical Mercator projection used by Google and OpenStreetMap

// Globale Variablen 
var map;
var clusters = new Array();

//Map, Layers and Map Controls
$(document).ready(function() {
	// ALL Layers 
	map = new ol.Map({
		target: 'map',
		// Base Maps Layers. To change the default Layer : "visible: true or false". 
		// ol.layer.Group defines the LayerSwitcher organisation
		layers: [
			// new ol.layer.Group({
			// 	'title': 'Deals', 
			// 	layers : [cluster],
			// }),
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
						source: new ol.source.Stamen({layer:'toner'})
					}),
				]
			}),
			// Context Layers from the Landobservatory Geoserver. 
			new ol.layer.Group({
				title:'Context Layers',
				layers:[
					new ol.layer.Tile({
						title:'Global Cropland',
						visible:false,
						source: new ol.source.TileWMS({
							url:'',
							params:{'LAYERS':''},
							serverType:'geoserver'
						})
					}),
					new ol.layer.Tile({
						title:'Global Landcover',
						visible:false,
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
							// new ol.control.ZoomToExtent({
    			// 				extent:undefined
							// }),
		],
		interactions : [
							new ol.interaction.Select(),
							new ol.interaction.MouseWheelZoom(),
							new ol.interaction.PinchZoom(),
							new ol.interaction.DragZoom (),
							new ol.interaction.DoubleClickZoom(),
							new ol.interaction.DragPan(), 
		],
		// Set the map view : here it's set to see the all world. 
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
//debugger;
	
	map.on('click', function (evt){
	 	map.forEachFeatureAtPixel(evt.pixel, function (feature, layer){
	 		// With Click on the markers, shows a popup the markers features
	 		console.log("feature clicked: " + evt.feature);

			var element = document.getElementById('popup');
		
			var popup = new ol.Overlay({
				element: element,
				position:'center',
				stopEvent: false,
			});
			map.addOverlay(popup);
			if (feature){
		 		popup.setPosition(evt.coordinate);
		 		$(element).popover({
				    'placement': 'top',
				    'html': true,
				    'content': '<p>Latitude:</p><code>' + feature.get('latitude') + '</code>'+ '<p>Longitude:</p><code>' + feature.get('longitude') + '</code>'+ '<p>Intention of investment:</p><code>' + feature.get('intention') + '</code>'
		   		});
		   		$(element).popover('show');
		   	} else {
		   		$(element).popover('destroy');
	   		}
	 		return feature;
	 	});
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

}); //gesamte document.ready.function Klammer

// MARKERS in clusters. ONE MARKER = ONE DEAL
//longitude, latitude, intention im Index.html definiert
function addClusteredMarker (longitude, latitude, intention) {
	var styleCache = {};
	var feature = new ol.Feature({
		geometry: new ol.geom.Point(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857')),
	});
	clusters.push(feature);

	// var source = new ol.source.Vector({
	// 	features: cluster
	// });
	var clusterSource = new ol.source.Cluster({
	  distance: 100,
	  source: new ol.source.Vector({
		features: clusters
		})
	});
	var cluster = //new ol.layer.Group({
		//'title':'Deals', 
		//visible: true,
		//layers: [
			new ol.layer.Vector({
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
			})
		//],
	//});
	map.addLayer(cluster);	
};


