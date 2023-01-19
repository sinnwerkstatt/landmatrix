import { TileLayer } from "leaflet?client"
import { writable } from "svelte/store"

const HereApiKey = "OgyVd8v9JkEHQIjrK4Q4sEVY-a19xpJXUxWYkTdBQuo"

function SDILegend(layer: string, folder = "lm"): string {
  return (
    `https://sdi.cde.unibe.ch/geoserver/${folder}/wms?` +
    "request=GetLegendGraphic&" +
    "service=WMS&" +
    "format=image%2Fpng&" +
    "width=25&height=25&" +
    "legend_options=forceLabels%3A1%3BfontAntiAliasing%3A1%3BfontName%3ANimbus+Sans+L+Regular%3B&" +
    `layer=${layer}`
  )
}

export interface BaseLayer {
  id: string
  name: string
  layer: TileLayer
}

export interface ContextLayer extends BaseLayer {
  legendUrlFunction: () => string
}

export const getBaseLayers = ($_: (t: string) => string): BaseLayer[] => {
  if (import.meta.env.SSR) return []
  return [
    {
      id: "satellite",
      name: $_("Satellite"),
      layer: new TileLayer(
        `https://2.aerial.maps.ls.hereapi.com/maptile/2.1/maptile/newest/satellite.day/{z}/{x}/{y}/512/png8?apiKey=${HereApiKey}`,
        {
          attribution: `Map Tiles &copy; ${new Date().getFullYear()} <a href="https://developer.here.com">HERE</a>`,
        },
      ),
    },
    {
      id: "map",
      name: $_("Map"),
      layer: new TileLayer(
        "https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png?apikey=a00f8fb036334c4b8a3618263738846a",
        {
          attribution:
            'Maps &copy; <a href="https://www.thunderforest.com">Thunderforest</a>, Data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
        },
      ),
    },
  ]
}

export const visibleLayer = writable("map")

export const getContextLayers = ($_: (t: string) => string): ContextLayer[] => {
  if (import.meta.env.SSR) return []
  return [
    {
      id: "land_cover",
      name: $_("Land Cover"),
      layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lo/wms", {
        layers: "globcover_2009",
        format: "image/png",
        transparent: true,
        opacity: 0.7,
        attribution:
          'Source: <a href="https://due.esrin.esa.int/page_globcover.php" target="_blank">ESA</a>',
      }),
      legendUrlFunction(): string {
        return SDILegend("globcover_2009", "lo")
      },
    },
    {
      id: "global_cropland",
      name: $_("Global Cropland"),
      layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lo/wms", {
        layers: "gl_cropland",
        format: "image/png",
        transparent: true,
        opacity: 0.7,
        attribution:
          'Source: <a href="https://sedac.ciesin.columbia.edu/data/set/aglands-croplands-2000" target="_blank">Socioeconomic Data and Applications Center (SEDAC)</a>',
      }),
      legendUrlFunction(): string {
        return SDILegend("gl_cropland", "lo")
      },
    },
    {
      id: "oil_palm_concessions_indonesia",
      name: $_("Oil palm concessions Indonesia"),
      layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lm/wms", {
        layers: "ind_oil_palm_concessions",
        format: "image/png",
        transparent: true,
        opacity: 0.7,
        attribution:
          'Source: <a href="https://data.globalforestwatch.org/datasets/f82b539b9b2f495e853670ddc3f0ce68_2" target="_blank">Global Forest Watch, October 2019</a>',
      }),
      legendUrlFunction(): string {
        return SDILegend("ind_oil_palm_concessions")
      },
    },
    {
      id: "key_biodiversity_areas_philippines",
      name: $_("Key biodiversity areas, Philippines"),
      layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lm/wms", {
        layers: "ph_key_biodiversity_areas",
        format: "image/png",
        transparent: true,
        opacity: 0.7,
        attribution:
          'Source: <a href="https://www.bmb.gov.ph" target="_blank">Biodiversity Management Bureau, Department of Environment and Natural Ressources, Philippines, October 2019</a>',
      }),
      legendUrlFunction(): string {
        return SDILegend("ph_key_biodiversity_areas")
      },
    },
    {
      id: "protected_areas_philippines",
      name: $_("Protected areas, Philippines"),
      layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lm/wms", {
        layers: "ph_protected_areas",
        format: "image/png",
        transparent: true,
        opacity: 0.7,
        attribution:
          'Source: <a href="https://www.bmb.gov.ph" target="_blank">Biodiversity Management Bureau, Department of Environment and Natural Ressources, Philippines, October 2019</a>',
      }),
      legendUrlFunction(): string {
        return SDILegend("ph_protected_areas")
      },
    },
    {
      id: "indigenous_and_community_philippines",
      name: $_("Indigenous and community conserved area, Philippines"),
      layer: new TileLayer.WMS("https://sdi.cde.unibe.ch/geoserver/lm/wms", {
        layers: "ph_icca_areas_2020",
        format: "image/png",
        transparent: true,
        opacity: 0.7,
        attribution:
          'Source: <a href="https://www.bmb.gov.ph" target="_blank">Biodiversity Management Bureau, Department of Environment and Natural Ressources, Philippines, December 2020</a>',
      }),
      legendUrlFunction(): string {
        return SDILegend("ph_icca_areas_2020")
      },
    },
  ]
}

export const visibleContextLayers = writable<string[]>([])
