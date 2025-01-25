import { env } from "$env/dynamic/public"
import { type Map } from "ol"
import { extend, type Extent } from "ol/extent"
import { Tile as TileLayer, Vector } from "ol/layer"
import { TileWMS, XYZ } from "ol/source"

function getWMSTilesCDEUniBern(folder: string, LAYERS: string, attributions: string) {
  const qParams = new URLSearchParams({
    request: "GetLegendGraphic",
    service: "WMS",
    format: "image/png",
    width: "25",
    height: "25",
    legend_options: "forceLabels:1;fontAntiAliasing:1;fontName:Nimbus Sans L Regular;",
    layer: LAYERS,
  })
  return {
    layer: new TileLayer({
      source: new TileWMS({
        url: `https://sdi.cde.unibe.ch/geoserver/${folder}/wms`,
        params: { LAYERS: LAYERS, FORMAT: "image/png", TRANSPARENT: true },
        attributions: attributions,
      }),
      opacity: 0.7,
      visible: false,
    }),
    legend: `https://sdi.cde.unibe.ch/geoserver/${folder}/wms?${qParams.toString()}`,
  }
}

export const baseLayers = [
  {
    id: "satellite",
    name: "Satellite",
    layer: new TileLayer({
      source: new XYZ({
        url: `https://2.aerial.maps.ls.hereapi.com/maptile/2.1/maptile/newest/satellite.day/{z}/{x}/{y}/512/png8?apiKey=${env.PUBLIC_HERE_API_KEY}`,
        attributions: `Map Tiles © ${new Date().getFullYear()} <a href="https://developer.here.com">HERE</a>`,
      }),
    }),
  },
  {
    id: "map",
    name: "Map",
    layer: new TileLayer({
      source: new XYZ({
        url: `https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=${env.PUBLIC_THUNDERFOREST_API_KEY}`,
        attributions:
          'Maps © <a href="https://www.thunderforest.com">Thunderforest</a>, Data © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
      }),
      visible: false,
      maxZoom: 22,
    }),
  },
  // {
  //   id: "osm",
  //   name: "OSM",
  //   layer: new TileLayer({ source: new OSM(), visible: false }),
  // },
]

export const contextLayers = [
  {
    id: "land_cover",
    name: "Land Cover",
    ...getWMSTilesCDEUniBern(
      "lo",
      "globcover_2009",
      'Source: <a href="https://due.esrin.esa.int/page_globcover.php" target="_blank">ESA</a>',
    ),
  },
  {
    id: "global_cropland",
    name: "Global Cropland",
    ...getWMSTilesCDEUniBern(
      "lo",
      "gl_cropland",
      'Source: <a href="https://sedac.ciesin.columbia.edu/data/set/aglands-croplands-2000" target="_blank">Socioeconomic Data and Applications Center (SEDAC)</a>',
    ),
  },
  {
    id: "oil_palm_concessions_indonesia",
    name: "Oil palm concessions Indonesia",
    ...getWMSTilesCDEUniBern(
      "lm",
      "ind_oil_palm_concessions",
      'Source: <a href="https://data.globalforestwatch.org/datasets/f82b539b9b2f495e853670ddc3f0ce68_2" target="_blank">Global Forest Watch, October 2019</a>',
    ),
  },
  {
    id: "key_biodiversity_areas_philippines",
    name: "Key biodiversity areas, Philippines",
    ...getWMSTilesCDEUniBern(
      "lm",
      "ph_key_biodiversity_areas",
      'Source: <a href="https://www.bmb.gov.ph" target="_blank">Biodiversity Management Bureau, Department of Environment and Natural Ressources, Philippines, October 2019</a>',
    ),
  },
  {
    id: "protected_areas_philippines",
    name: "Protected areas, Philippines",
    ...getWMSTilesCDEUniBern(
      "lm",
      "ph_protected_areas",
      'Source: <a href="https://www.bmb.gov.ph" target="_blank">Biodiversity Management Bureau, Department of Environment and Natural Ressources, Philippines, October 2019</a>',
    ),
  },

  {
    id: "indigenous_and_community_philippines",
    name: "Indigenous and community conserved area, Philippines",
    ...getWMSTilesCDEUniBern(
      "lm",
      "ph_icca_areas_2020",
      'Source: <a href="https://www.bmb.gov.ph" target="_blank">Biodiversity Management Bureau, Department of Environment and Natural Ressources, Philippines, December 2020</a>',
    ),
  },

  {
    id: "landmark_indigenous_lands_acknowledged_by_government_documented",
    name: "Indigenous lands acknowledged by government (documented)",
    layer: new TileLayer({
      source: new TileWMS({
        url: `https://gis.wri.org:443/server/services/LandMark/comm_ind_Documented/MapServer/WMSServer?`,
        params: {
          LAYERS: "0",
          FORMAT: "image/png",
          TRANSPARENT: true,
        },
        attributions:
          'Source: <a href="http://www.landmarkmap.org/" target="_blank">LandMark. 2020. LandMark: The Global Platform of Indigenous and Community Land.</a>',
      }),
      opacity: 0.7,
      visible: false,
    }),
    legend:
      `https://gis.wri.org/server/services/LandMark/comm_ind_Documented/MapServer/WMSServer?` +
      "request=GetLegendGraphic&" +
      "version=1.3.0&" +
      "format=image%2Fpng&" +
      "width=25&height=25&" +
      "legend_options=forceLabels%3A1%3BfontAntiAliasing%3A1%3BfontName%3ANimbus+Sans+L+Regular%3B&" +
      `layer=0`,
  },
]

export const selectedLayers = $state({
  baseLayer: "map",
  contextLayers: [] as string[],
})

export function fitMapToFeatures(map: Map) {
  let extent: Extent | null = null

  map.getLayers().forEach(layer => {
    if (!(layer instanceof Vector)) return

    const sourceExtent = layer.getSource().getExtent()
    if (!sourceExtent) return
    if (!extent) extent = sourceExtent.slice()
    else extent = extend(extent, sourceExtent)
  })

  if (extent) {
    map.getView().fit(extent, {
      padding: [150, 150, 150, 150],
      maxZoom: 13,
      // duration: 500, // Optional: Add animation with a duration of 500ms
    })
  }
}
