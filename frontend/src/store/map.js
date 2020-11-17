const HereApiKey = "OgyVd8v9JkEHQIjrK4Q4sEVY-a19xpJXUxWYkTdBQuo";

export const mapModule = {
  state: () => ({
    showFilterOverlay: true,
    showScopeOverlay: true,
    displayDealsCount: true,
    visibleLayer: "ThunderForest",
    layers: [
      {
        name: "Here",
        attribution: `Map Tiles &copy; ${new Date().getFullYear()} <a href="http://developer.here.com">HERE</a>`,
        url: `https://2.aerial.maps.ls.hereapi.com/maptile/2.1/maptile/newest/satellite.day/{z}/{x}/{y}/512/png8?apiKey=${HereApiKey}`,
      },
      {
        name: "ThunderForest",
        attribution:
          'Maps &copy; <a href="http://www.thunderforest.com">Thunderforest</a>, Data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
        url:
          "https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=a00f8fb036334c4b8a3618263738846a",
      },
      {
        name: "OpenStreetMap",
        attribution:
          '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
        url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      },
      {
        name: "CartoDB Positron",
        url: "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      },
      {
        name: "ESRI Satellite",
        url:
          "http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attribution:
          "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
      },
      {
        name: "ESRI Topology",
        url:
          "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attribution:
          "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community",
      },
      {
        name: "OpenTopoMap",
        maxZoom: 17,
        url: "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        attribution:
          'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
      },
    ],
    contextLayers: [
      {
        name: "Land Cover",
        url: "http://sdi.cde.unibe.ch/geoserver/lo/wms",
        params: {
          layers: "globcover_2009",
          format: "image/png",
          transparent: true,
          attribution:
            'Source: <a href="http://due.esrin.esa.int/page_globcover.php" target="_blank">ESA</a>',
        },
        legendUrlFunction() {
          let imgParams = {
            request: "GetLegendGraphic",
            service: "WMS",
            layer: "globcover_2009",
            format: "image/png",
            width: 25,
            height: 25,
            legend_options:
              "forceLabels:1;fontAntiAliasing:1;fontName:Nimbus Sans L Regular;",
          };
          let sparams = new URLSearchParams(imgParams).toString();
          return `http://sdi.cde.unibe.ch/geoserver/lo/wms?${sparams}`;
        },
      },
      {
        name: "Global Cropland",
        url: "http://sdi.cde.unibe.ch/geoserver/lo/wms",
        params: {
          layers: "gl_cropland",
          format: "image/png",
          transparent: true,
          attribution:
            'Source: <a href="http://sedac.ciesin.columbia.edu/data/set/aglands-croplands-2000" target="_blank">Socioeconomic Data and Applications Center (SEDAC)</a>',
        },
        legendUrlFunction() {
          let imgParams = {
            request: "GetLegendGraphic",
            service: "WMS",
            layer: "gl_cropland",
            format: "image/png",
            width: 25,
            height: 25,
            legend_options:
              "forceLabels:1;fontAntiAliasing:1;fontName:Nimbus Sans L Regular;",
          };
          let sparams = new URLSearchParams(imgParams).toString();
          return `http://sdi.cde.unibe.ch/geoserver/lo/wms?${sparams}`;
        },
      },
      {
        name: "Oil palm concessions Indonesia",
        url: "http://sdi.cde.unibe.ch/geoserver/lm/wms",
        params: {
          layers: "ind_oil_palm_concessions",
          format: "image/png",
          transparent: true,
          attribution:
            'Source: <a href="http://data.globalforestwatch.org/datasets/f82b539b9b2f495e853670ddc3f0ce68_2" target="_blank">Global Forest Watch, October 2019</a>',
        },
        legendUrlFunction() {
          let imgParams = {
            request: "GetLegendGraphic",
            service: "WMS",
            layer: "ind_oil_palm_concessions",
            format: "image/png",
            width: 25,
            height: 25,
            legend_options:
              "forceLabels:1;fontAntiAliasing:1;fontName:Nimbus Sans L Regular;",
          };
          let sparams = new URLSearchParams(imgParams).toString();
          return `http://sdi.cde.unibe.ch/geoserver/lm/wms?${sparams}`;
        },
      },
      {
        name: "Key biodiversity areas, Philippines",
        url: "http://sdi.cde.unibe.ch/geoserver/lm/wms",
        params: {
          layers: "ph_key_biodiversity_areas",
          format: "image/png",
          transparent: true,
          attribution:
            'Source: <a href="https://www.bmb.gov.ph" target="_blank">Biodiversity Management Bureau, Department of Environment and Natural Ressources, Philippines, October 2019</a>',
        },
        legendUrlFunction() {
          let imgParams = {
            request: "GetLegendGraphic",
            service: "WMS",
            layer: "ph_key_biodiversity_areas",
            format: "image/png",
            width: 25,
            height: 25,
            legend_options:
              "forceLabels:1;fontAntiAliasing:1;fontName:Nimbus Sans L Regular;",
          };
          let sparams = new URLSearchParams(imgParams).toString();
          return `http://sdi.cde.unibe.ch/geoserver/lm/wms?${sparams}`;
        },
      },
      {
        name: "Protected areas, Philippines",
        url: "http://sdi.cde.unibe.ch/geoserver/lm/wms",
        params: {
          layers: "ph_protected_areas",
          format: "image/png",
          transparent: true,
          attribution:
            'Source: <a href="https://www.bmb.gov.ph" target="_blank">Biodiversity Management Bureau, Department of Environment and Natural Ressources, Philippines, October 2019</a>',
        },
        legendUrlFunction() {
          let imgParams = {
            request: "GetLegendGraphic",
            service: "WMS",
            layer: "ph_protected_areas",
            format: "image/png",
            width: 25,
            height: 25,
            legend_options:
              "forceLabels:1;fontAntiAliasing:1;fontName:Nimbus Sans L Regular;",
          };
          let sparams = new URLSearchParams(imgParams).toString();
          return `http://sdi.cde.unibe.ch/geoserver/lm/wms?${sparams}`;
        },
      },
    ],
  }),
  mutations: {
    setCurrentLayer(state, layer) {
      state.visibleLayer = layer;
    },
    showFilterOverlay(state, payload) {
      state.showFilterOverlay = payload;
    },
    showScopeOverlay(state, payload) {
      state.showScopeOverlay = payload;
    },
    setDisplayDealsCount(state, payload) {
      state.displayDealsCount = payload;
    },
  },
  actions: {
    setCurrentLayer(context, layer) {
      context.commit("setCurrentLayer", layer);
    },
    showFilterOverlay(context, payload) {
      context.commit("showFilterOverlay", payload);
    },
    showScopeOverlay(context, payload) {
      context.commit("showScopeOverlay", payload);
    },
  },
};
