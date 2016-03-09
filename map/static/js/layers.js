var baseLayers = [
    new ol.layer.Tile({
        title: 'OpenStreetMap',
        type: 'base',
        visible: true,
        source: new ol.source.OSM()
    }),
    new ol.layer.Tile({
        title: 'Satellite',
        type: 'base',
        visible: false,
        source: new ol.source.MapQuest({layer: 'sat'})
    }),
    new ol.layer.Tile({
        title: 'Watercolor',
        type: 'base',
        visible: false,
        source: new ol.source.Stamen({layer: 'watercolor'})
    })
];

var contextLayers = [

    // Global layers

    new ol.layer.Tile({
        title: "Accessibility",
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
        title: "Global Land Cover 2009",
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
        title: "Global Cropland",
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
        title: "Global Pasture Land",
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
    new ol.layer.Tile({
        title: "Population Density 2008",
        source: new ol.source.TileWMS({
            url: "http://sdi.cde.unibe.ch/geoserver/lo/wms",
            params: {
                'srs': 'EPSG%3a900913',
                'layers': 'lspop_2008'
            }
        }),
        visible: false,
        opacity: 0.6
    }),

    // LAOS LOCAL LAYER! TODO!

    new ol.layer.Tile({
        title: "Incidence of poverty",
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
/*
 new ol.Layer.WMS("Accessibility to province capital","http://sdi.cde.unibe.ch/geoserver/gwc/service/wms",{
 epsg: 900913,
 format: "image/png8",
 layers: "lo:laos_t_to_prov_capital_mean_min",
 transparent: true,
 },{
 visibility: false,
 isBaseLayer: false,
 sphericalMercator: true,
 maxExtent: new ol.Bounds(10018755, 181, 12801601, 3482189),
 opacity: 0.7,
 })

 /*,
 new ol.Layer.WMS("Seasonal road accessibility","http://sdi.cde.unibe.ch/geoserver/gwc/service/wms",{
 epsg: 900913,
 format: "image/png8",
 layers: "lo:laos_w_road_access",
 transparent: true,
 },{
 visibility: false,
 isBaseLayer: false,
 sphericalMercator: true,
 maxExtent: new ol.Bounds(10018755, 181, 12801601, 3482189),
 opacity: 0.7,
 }),
 new ol.Layer.WMS("Population density","http://sdi.cde.unibe.ch/geoserver/gwc/service/wms",{
 epsg: 900913,
 format: "image/png8",
 layers: "lo:laos_pop_density",
 transparent: true,
 },{
 visibility: false,
 isBaseLayer: false,
 sphericalMercator: true,
 maxExtent: new ol.Bounds(10018755, 181, 12801601, 3482189),
 opacity: 0.7,
 }),
 new ol.Layer.WMS("Share of households being farm household","http://sdi.cde.unibe.ch/geoserver/gwc/service/wms",{
 epsg: 900913,
 format: "image/png8",
 layers: "lo:laos_w_pct_farmhh",
 transparent: true,
 },{
 visibility: false,
 isBaseLayer: false,
 sphericalMercator: true,
 maxExtent: new ol.Bounds(10018755, 181, 12801601, 3482189),
 opacity: 0.7,
 }),
 new ol.Layer.WMS("Protected areas","http://sdi.cde.unibe.ch/geoserver/gwc/service/wms",{
 epsg: 900913,
 format: "image/png8",
 layers: "lo:laos_protected_area",
 transparent: true,
 },{
 visibility: false,
 isBaseLayer: false,
 sphericalMercator: true,
 maxExtent: new ol.Bounds(10018755, 181, 12801601, 3482189),
 opacity: 0.7,
 }),
 new ol.Layer.WMS("Percentage of economically active population","http://sdi.cde.unibe.ch/geoserver/gwc/service/wms",{
 epsg: 900913,
 format: "image/png8",
 layers: "lo:laos_pop_econ_active_pct",
 transparent: true,
 },{
 visibility: false,
 isBaseLayer: false,
 sphericalMercator: true,
 maxExtent: new ol.Bounds(10018755, 181, 12801601, 3482189),
 opacity: 0.7,
 }),

 ]

 */
