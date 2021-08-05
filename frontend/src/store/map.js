import { TileLayer } from "leaflet";

const HereApiKey = "OgyVd8v9JkEHQIjrK4Q4sEVY-a19xpJXUxWYkTdBQuo";

function SDILegend(layer, folder = "lm") {
  const sparams = new URLSearchParams([
    ["request", "GetLegendGraphic"],
    ["service", "WMS"],
    ["layer", layer],
    ["format", "image/png"],
    ["width", 25],
    ["height", 25],
    [
      "legend_options",
      "forceLabels:1;fontAntiAliasing:1;fontName:Nimbus Sans L Regular;",
    ],
  ]);
  return `https://sdi.cde.unibe.ch/geoserver/${folder}/wms?${sparams.toString()}`;
}

function isMobile() {
  return window.innerWidth < 768;
}


export const mapModule = {
  state: () => ({
    showFilterBar: !isMobile(),
    showContextBar: !isMobile(),
    displayDealsCount: true,
    visibleLayer: "Map",
    layers: [
      {
        name: "Satellite",
        attribution: `Map Tiles &copy; ${new Date().getFullYear()} <a href="https://developer.here.com">HERE</a>`,
        url: `https://2.aerial.maps.ls.hereapi.com/maptile/2.1/maptile/newest/satellite.day/{z}/{x}/{y}/512/png8?apiKey=${HereApiKey}`,
      },
      {
        name: "Map",
        attribution:
          'Maps &copy; <a href="https://www.thunderforest.com">Thunderforest</a>, Data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
        url: "https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=a00f8fb036334c4b8a3618263738846a",
      },
    ],
    contextLayers: [
      {
        name: "Land Cover",
        layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lo/wms", {
          layers: "globcover_2009",
          format: "image/png",
          transparent: true,
          opacity: 0.7,
          attribution:
            'Source: <a href="https://due.esrin.esa.int/page_globcover.php" target="_blank">ESA</a>',
        }),
        legendUrlFunction() {
          return SDILegend("globcover_2009", "lo");
        },
      },
      {
        name: "Global Cropland",
        layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lo/wms", {
          layers: "gl_cropland",
          format: "image/png",
          transparent: true,
          opacity: 0.7,
          attribution:
            'Source: <a href="https://sedac.ciesin.columbia.edu/data/set/aglands-croplands-2000" target="_blank">Socioeconomic Data and Applications Center (SEDAC)</a>',
        }),
        legendUrlFunction() {
          return SDILegend("gl_cropland", "lo");
        },
      },
      {
        name: "Oil palm concessions Indonesia",
        layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lm/wms", {
          layers: "ind_oil_palm_concessions",
          format: "image/png",
          transparent: true,
          opacity: 0.7,
          attribution:
            'Source: <a href="https://data.globalforestwatch.org/datasets/f82b539b9b2f495e853670ddc3f0ce68_2" target="_blank">Global Forest Watch, October 2019</a>',
        }),
        legendUrlFunction() {
          return SDILegend("ind_oil_palm_concessions");
        },
      },
      {
        name: "Key biodiversity areas, Philippines",
        layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lm/wms", {
          layers: "ph_key_biodiversity_areas",
          format: "image/png",
          transparent: true,
          opacity: 0.7,
          attribution:
            'Source: <a href="https://www.bmb.gov.ph" target="_blank">Biodiversity Management Bureau, Department of Environment and Natural Ressources, Philippines, October 2019</a>',
        }),
        legendUrlFunction: function () {
          return SDILegend("ph_key_biodiversity_areas");
        },
      },
      {
        name: "Protected areas, Philippines",
        layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lm/wms", {
          layers: "ph_protected_areas",
          format: "image/png",
          transparent: true,
          opacity: 0.7,
          attribution:
            'Source: <a href="https://www.bmb.gov.ph" target="_blank">Biodiversity Management Bureau, Department of Environment and Natural Ressources, Philippines, October 2019</a>',
        }),
        legendUrlFunction() {
          return SDILegend("ph_protected_areas");
        },
      },
      {
        name: "Indigenous and community conserved area, Philippines",
        layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lm/wms", {
          layers: "ph_icca_areas_2020",
          format: "image/png",
          transparent: true,
          opacity: 0.7,
          attribution:
            'Source: <a href="https://www.bmb.gov.ph" target="_blank">Biodiversity Management Bureau, Department of Environment and Natural Ressources, Philippines, December 2020</a>',
        }),
        legendUrlFunction() {
          return SDILegend("ph_icca_areas_2020");
        },
      },
    ],
  }),
  mutations: {
    setCurrentLayer: (state, layer) => (state.visibleLayer = layer),
    showFilterBar: (state, payload) => (state.showFilterBar = payload),
    showContextBar: (state, payload) => {
      if (payload === "!isMobile") {
        state.showContextBar = !isMobile();
      } else {
        state.showContextBar = payload;
      }
    },
    setDisplayDealsCount: (state, payload) => (state.displayDealsCount = payload),
  },
  actions: {
    setCurrentLayer: (context, layer) => context.commit("setCurrentLayer", layer),
    showFilterBar: (context, payload) => context.commit("showFilterBar", payload),
    showContextBar: (context, payload) => context.commit("showContextBar", payload),
  },
};
