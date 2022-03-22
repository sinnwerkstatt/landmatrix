import type { TileLayer } from "leaflet";

const HereApiKey = "OgyVd8v9JkEHQIjrK4Q4sEVY-a19xpJXUxWYkTdBQuo";

export interface BaseLayer {
  name: string;
  attribution: string;
  url: string;
}

export interface ContextLayer {
  name: string;
  layer: TileLayer;
  legendUrlFunction: () => string;
}

export const baseLayers: BaseLayer[] = [
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
];
